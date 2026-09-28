import asyncio
import json
import logging
import os

from app.handler.acs_event_handler import AcsEventHandler
from app.handler.acs_media_handler import ACSMediaHandler
from dotenv import load_dotenv
from quart import Quart, Response, request, websocket

load_dotenv()

app = Quart(__name__)
app.config["AZURE_VOICE_LIVE_API_KEY"] = os.getenv("AZURE_VOICE_LIVE_API_KEY", "")
app.config["AZURE_VOICE_LIVE_ENDPOINT"] = os.getenv("AZURE_VOICE_LIVE_ENDPOINT")
app.config["VOICE_LIVE_MODEL"] = os.getenv("VOICE_LIVE_MODEL", "gpt-4o-mini")
app.config["ACS_CONNECTION_STRING"] = os.getenv("ACS_CONNECTION_STRING")
app.config["ACS_DEV_TUNNEL"] = os.getenv("ACS_DEV_TUNNEL", "")
app.config["AZURE_USER_ASSIGNED_IDENTITY_CLIENT_ID"] = os.getenv(
    "AZURE_USER_ASSIGNED_IDENTITY_CLIENT_ID", ""
)

# Ambient Scenes Configuration
# Options: none, office, call_center (or custom presets)
app.config["AMBIENT_PRESET"] = os.getenv("AMBIENT_PRESET", "none")

# IVR Demo Routing Configuration
app.config["DEMO_MODE"] = os.getenv("DEMO_MODE", "false").lower() == "true"
app.config["DEMO_TRANSFER_NUMBER"] = os.getenv("DEMO_TRANSFER_NUMBER", "+19453821555")
app.config["DEMO_WEB_SIMULATE_TRANSFER"] = (
    os.getenv("DEMO_WEB_SIMULATE_TRANSFER", "true").lower() == "true"
)

# Shared call state for bridging call_connection_id to media handler (single-call demo)
demo_call_state: dict = {}
app.config["DEMO_CALL_STATE"] = demo_call_state

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s: %(message)s"
)
logger = logging.getLogger(__name__)

# App Insights telemetry configuration
try:
    from azure.monitor.opentelemetry import configure_azure_monitor
    ai_cs = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
    if ai_cs and ai_cs.strip():
        configure_azure_monitor(connection_string=ai_cs)
        logger.info("Application Insights telemetry configured successfully")
except Exception as e:
    logger.warning(f"Could not initialize Application Insights telemetry: {e}")

# Log ambient configuration on startup
ambient_preset = app.config["AMBIENT_PRESET"]
if ambient_preset and ambient_preset != "none":
    logger.info(f"Ambient scenes ENABLED: preset='{ambient_preset}'")
else:
    logger.info("Ambient scenes DISABLED (preset=none)")

# Log demo configuration on startup
if app.config["DEMO_MODE"]:
    logger.info(
        "IVR Demo Mode ENABLED: transfer_number=%s web_simulate=%s",
        app.config["DEMO_TRANSFER_NUMBER"],
        app.config["DEMO_WEB_SIMULATE_TRANSFER"],
    )
else:
    logger.info("IVR Demo Mode DISABLED")

acs_handler = AcsEventHandler(app.config)


@app.route("/acs/incomingcall", methods=["POST"])
async def incoming_call_handler():
    """Handles initial incoming call event from EventGrid."""
    events = await request.get_json()
    host_url = request.host_url.replace("http://", "https://", 1).rstrip("/")
    return await acs_handler.process_incoming_call(events, host_url, app.config)


@app.route("/acs/callbacks/<context_id>", methods=["POST"])
async def acs_event_callbacks(context_id):
    """Handles ACS event callbacks for call connection and streaming events."""
    raw_events = await request.get_json()
    return await acs_handler.process_callback_events(context_id, raw_events, app.config)


@app.websocket("/acs/ws")
async def acs_ws():
    """WebSocket endpoint for ACS to send audio to Voice Live."""
    logger = logging.getLogger("acs_ws")
    logger.info("Incoming ACS WebSocket connection")
    handler = ACSMediaHandler(app.config)
    await handler.init_incoming_websocket(websocket, is_raw_audio=False)
    connect_task = asyncio.create_task(handler.connect())
    try:
        while True:
            msg = await websocket.receive()
            await handler.acs_to_voicelive(msg)
    except asyncio.CancelledError:
        logger.info("ACS WebSocket cancelled")
    except Exception:
        logger.exception("ACS WebSocket connection closed")
    finally:
        if connect_task and not connect_task.done():
            connect_task.cancel()
        try:
            await handler.stop_audio()
        except Exception:
            pass
        if hasattr(handler, "send_task") and handler.send_task and not handler.send_task.done():
            handler.send_task.cancel()
        if getattr(handler, "ws", None) and not handler.ws.closed:
            try:
                await handler.ws.close()
            except Exception:
                pass


@app.websocket("/web/ws")
async def web_ws():
    """WebSocket endpoint for web clients to send audio to Voice Live."""
    logger = logging.getLogger("web_ws")
    logger.info("Incoming Web WebSocket connection")
    handler = ACSMediaHandler(app.config)
    await handler.init_incoming_websocket(websocket, is_raw_audio=True)
    connect_task = asyncio.create_task(handler.connect())
    try:
        while True:
            msg = await websocket.receive()
            if isinstance(msg, (bytes, bytearray, memoryview)):
                await handler.web_to_voicelive(bytes(msg))
    except asyncio.CancelledError:
        logger.info("Web WebSocket cancelled")
    except Exception:
        logger.exception("Web WebSocket connection closed")
    finally:
        if connect_task and not connect_task.done():
            connect_task.cancel()
        try:
            await handler.stop_audio()
        except Exception:
            pass
        if hasattr(handler, "send_task") and handler.send_task and not handler.send_task.done():
            handler.send_task.cancel()
        if getattr(handler, "ws", None) and not handler.ws.closed:
            try:
                await handler.ws.close()
            except Exception:
                pass


@app.route("/demo/state")
async def demo_state():
    """Debug endpoint to inspect current demo call state (only active in DEMO_MODE)."""
    if not app.config.get("DEMO_MODE"):
        return Response(status=404)
    safe_state = {k: str(v) for k, v in demo_call_state.items()}
    return Response(
        response=json.dumps(safe_state), status=200, content_type="application/json"
    )


@app.route("/")
async def index():
    """Serves the static index page."""
    return await app.send_static_file("index.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
