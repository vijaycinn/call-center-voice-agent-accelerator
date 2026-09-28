"""Handles media streaming to Azure Voice Live API via WebSocket."""

import asyncio
import base64
import json
import logging
import re
import uuid
from typing import Optional

import numpy as np
from azure.identity.aio import ManagedIdentityCredential
from websockets.asyncio.client import connect as ws_connect
from websockets.typing import Data

from .ambient_mixer import AmbientMixer

logger = logging.getLogger(__name__)

# Default chunk size in bytes (100ms of audio at 24kHz, 16-bit mono)
DEFAULT_CHUNK_SIZE = 4800  # 24000 samples/sec * 0.1 sec * 2 bytes

# Transfer detection: match the AI's spoken phrase "I will transfer you to <Dept> now."
TRANSFER_PATTERN = re.compile(r"i will transfer you to (.+?) now", re.IGNORECASE)


def session_config():
    """Returns the default session configuration for Voice Live."""
    return {
        "type": "session.update",
        "session": {
            "instructions": (
                "You are the County Services IVR assistant. Your job is to greet callers, "
                "understand who or what department they need, confirm the correct department "
                "with them, and transfer them.\n\n"
                "Follow this exact flow:\n"
                "1. Greet: \"Thank you for calling County Services. I can help direct your call. "
                "Who or what department are you trying to reach today?\"\n"
                "2. Listen to the caller and identify the best matching department from this list:\n"
                "   - Administration (official county records and administrative processes only "
                "\u2014 NOT a general information line)\n"
                "   - County Executive Office (matters specifically for the County Executive "
                "\u2014 NOT a general county information line)\n"
                "   - Public Works (roads, potholes, utilities, sanitation, permits)\n"
                "   - Health Services (clinics, public health, medical assistance)\n"
                "   - Human Services (social services, benefits, financial assistance)\n"
                "   - Clerk / Recorder (official records, filing, marriage/birth certificates)\n"
                "   - Sheriff / Public Safety (law enforcement, non-emergency safety)\n"
                "3. If the caller's need is unclear, ask one clarifying question: "
                "\"Can you tell me a little more about what you need help with?\"\n"
                "4. Confirm: \"I can connect you to [Department Name]. Does that sound right?\"\n"
                "5. When the caller confirms, say exactly: "
                "\"I will transfer you to [Department Name] now.\" then stop speaking.\n\n"
                "Important rules:\n"
                "- Never route to Administration for general questions or complaints. If a caller "
                "says \"Administration\" without a clear administrative reason, ask what the issue "
                "is about before routing there.\n"
                "- Never route to the County Executive Office for general inquiries. That office "
                "handles matters specifically directed at the County Executive. If the caller "
                "sounds like they want general county information, ask what the issue is about.\n"
                "- If truly ambiguous after one clarification, say: "
                "\"I will transfer you to the General Operator now.\"\n"
                "- Always end a confirmed transfer with the exact phrase: "
                "\"I will transfer you to [Department Name] now.\" "
                "This phrase triggers the transfer action \u2014 do not vary the wording."
            ),
            "turn_detection": {
                "type": "azure_semantic_vad",
                "threshold": 0.3,
                "prefix_padding_ms": 200,
                "silence_duration_ms": 200,
                "remove_filler_words": False,
                "end_of_utterance_detection": {
                    "model": "semantic_detection_v1",
                    "threshold": 0.01,
                    "timeout": 2,
                },
            },
            "input_audio_noise_reduction": {"type": "azure_deep_noise_suppression"},
            "input_audio_echo_cancellation": {"type": "server_echo_cancellation"},
            "voice": {
                "name": "en-US-Aria:DragonHDLatestNeural",
                "type": "azure-standard",
                "temperature": 0.8,
            },
        },
    }


class ACSMediaHandler:
    """Manages audio streaming between client and Azure Voice Live API."""

    def __init__(self, config):
        self.endpoint = config["AZURE_VOICE_LIVE_ENDPOINT"]
        self.model = config["VOICE_LIVE_MODEL"]
        self.api_key = config["AZURE_VOICE_LIVE_API_KEY"]
        self.client_id = config["AZURE_USER_ASSIGNED_IDENTITY_CLIENT_ID"]
        self.send_queue = asyncio.Queue()
        self.ws = None
        self.send_task = None
        self.incoming_websocket = None
        self.is_raw_audio = True

        # TTS output buffering for continuous ambient mixing
        self._tts_output_buffer = bytearray()
        self._tts_buffer_lock = asyncio.Lock()
        self._max_buffer_size = 480000  # 10 seconds of audio - large enough for long responses
        self._buffer_warning_logged = False
        self._tts_playback_started = False  # Track if we've started playing TTS
        self._min_buffer_to_start = 9600  # 200ms buffer before starting TTS playback
        
        # Ambient mixer initialization
        self._ambient_mixer: Optional[AmbientMixer] = None
        ambient_preset = config.get("AMBIENT_PRESET", "none")
        if ambient_preset and ambient_preset != "none":
            try:
                self._ambient_mixer = AmbientMixer(preset=ambient_preset)
            except Exception as e:
                logger.error(f"Failed to initialize AmbientMixer: {e}")

        # IVR demo call state (shared dict bridged from server.py)
        self.call_state = config.get("DEMO_CALL_STATE", {})
        self.demo_mode = config.get("DEMO_MODE", False)
        self.demo_transfer_number = config.get("DEMO_TRANSFER_NUMBER", "")
        self.demo_web_simulate = config.get("DEMO_WEB_SIMULATE_TRANSFER", True)
        self.acs_connection_string = config.get("ACS_CONNECTION_STRING", "")

    def _generate_guid(self):
        return str(uuid.uuid4())

    async def connect(self):
        """Connects to Azure Voice Live API via WebSocket."""
        endpoint = self.endpoint.rstrip("/")
        model = self.model.strip()
        url = f"{endpoint}/voice-live/realtime?api-version=2025-05-01-preview&model={model}"
        url = url.replace("https://", "wss://")

        headers = {"x-ms-client-request-id": self._generate_guid()}

        if self.client_id:
            # Use async context manager to auto-close the credential
            async with ManagedIdentityCredential(client_id=self.client_id) as credential:
                token = await credential.get_token(
                    "https://cognitiveservices.azure.com/.default"
                )
                headers["Authorization"] = f"Bearer {token.token}"
                logger.info("[VoiceLiveACSHandler] Connected to Voice Live API by managed identity")
        else:
            headers["api-key"] = self.api_key

        self.ws = await ws_connect(url, additional_headers=headers)
        logger.info("[VoiceLiveACSHandler] Connected to Voice Live API")

        await self._send_json(session_config())
        await self._send_json({"type": "response.create"})

        asyncio.create_task(self._receiver_loop())
        self.send_task = asyncio.create_task(self._sender_loop())

    async def init_incoming_websocket(self, socket, is_raw_audio=True):
        """Sets up incoming ACS WebSocket."""
        self.incoming_websocket = socket
        self.is_raw_audio = is_raw_audio

    async def audio_to_voicelive(self, audio_b64: str):
        """Queues audio data to be sent to Voice Live API."""
        await self.send_queue.put(
            json.dumps({"type": "input_audio_buffer.append", "audio": audio_b64})
        )

    async def _send_json(self, obj):
        """Sends a JSON object over WebSocket."""
        if self.ws:
            await self.ws.send(json.dumps(obj))

    async def _sender_loop(self):
        """Continuously sends messages from the queue to the Voice Live WebSocket."""
        try:
            while True:
                msg = await self.send_queue.get()
                if self.ws:
                    await self.ws.send(msg)
        except Exception:
            logger.exception("[VoiceLiveACSHandler] Sender loop error")

    async def _receiver_loop(self):
        """Handles incoming events from the Voice Live WebSocket."""
        try:
            async for message in self.ws:
                event = json.loads(message)
                event_type = event.get("type")

                match event_type:
                    case "session.created":
                        session_id = event.get("session", {}).get("id")
                        logger.info("[VoiceLiveACSHandler] Session ID: %s", session_id)

                    case "input_audio_buffer.cleared":
                        logger.info("Input Audio Buffer Cleared Message")

                    case "input_audio_buffer.speech_started":
                        logger.info(
                            "Voice activity detection started at %s ms",
                            event.get("audio_start_ms"),
                        )
                        await self.stop_audio()

                    case "input_audio_buffer.speech_stopped":
                        logger.info("Speech stopped")

                    case "conversation.item.input_audio_transcription.completed":
                        transcript = event.get("transcript")
                        logger.info("User: %s", transcript)

                    case "conversation.item.input_audio_transcription.failed":
                        error_msg = event.get("error")
                        logger.warning("Transcription Error: %s", error_msg)

                    case "response.done":
                        response = event.get("response", {})
                        logger.info("Response Done: Id=%s", response.get("id"))
                        if response.get("status_details"):
                            logger.info(
                                "Status Details: %s",
                                json.dumps(response["status_details"], indent=2),
                            )

                    case "response.audio_transcript.done":
                        transcript = event.get("transcript")
                        logger.info("AI: %s", transcript)
                        await self.send_message(
                            json.dumps({"Kind": "Transcription", "Text": transcript})
                        )

                        # IVR transfer detection
                        if self.demo_mode and transcript:
                            match = TRANSFER_PATTERN.search(transcript)
                            if match:
                                department = match.group(1).strip()
                                await self._handle_transfer(department)

                    case "response.audio.delta":
                        delta = event.get("delta")
                        audio_bytes = base64.b64decode(delta)
                        
                        # Check if ambient mixing is enabled
                        if self._ambient_mixer is not None and self._ambient_mixer.is_enabled():
                            # Buffer TTS for continuous output mixing
                            async with self._tts_buffer_lock:
                                self._tts_output_buffer.extend(audio_bytes)
                                # Warn if buffer is getting large, but NEVER drop audio
                                if len(self._tts_output_buffer) > self._max_buffer_size:
                                    if not self._buffer_warning_logged:
                                        logger.warning(
                                            f"TTS buffer large: {len(self._tts_output_buffer)} bytes. "
                                            "Speech may be delayed but will not be cut."
                                        )
                                        self._buffer_warning_logged = True
                                elif self._buffer_warning_logged and len(self._tts_output_buffer) < self._max_buffer_size // 2:
                                    self._buffer_warning_logged = False  # Reset warning flag
                        else:
                            # No ambient - send immediately (original behavior)
                            if self.is_raw_audio:
                                await self.send_message(audio_bytes)
                            else:
                                await self.voicelive_to_acs(delta)

                    case "error":
                        logger.error("Voice Live Error: %s", event)

                    case _:
                        logger.debug(
                            "[VoiceLiveACSHandler] Other event: %s", event_type
                        )
        except Exception:
            logger.exception("[VoiceLiveACSHandler] Receiver loop error")

    async def _handle_transfer(self, department: str):
        """Handles transfer after the AI announces a department routing."""
        if self.is_raw_audio and self.demo_web_simulate:
            # Web client path: send simulated transfer event
            logger.info("ROUTING: department=%s mode=simulated", department)
            self.call_state["intent"] = department
            self.call_state["transfer_status"] = "simulated"
            await self.send_message(
                json.dumps({
                    "Kind": "TransferSimulated",
                    "Department": department,
                    "Status": "success",
                })
            )
        elif not self.is_raw_audio:
            # ACS phone path: execute real transfer
            call_connection_id = self.call_state.get("call_connection_id")
            if not call_connection_id:
                logger.error("ROUTING: No call_connection_id available for transfer")
                return
            target = self.demo_transfer_number
            logger.info(
                "ROUTING: department=%s mode=live target=%s", department, target
            )
            self.call_state["intent"] = department
            result = await self._transfer_call(call_connection_id, target)
            self.call_state["transfer_status"] = result.get("status", "unknown")

    async def _transfer_call(self, call_connection_id: str, target: str) -> dict:
        """Executes an ACS call transfer to the target phone number."""
        try:
            from azure.communication.callautomation import PhoneNumberIdentifier
            from azure.communication.callautomation.aio import CallAutomationClient

            acs_client = CallAutomationClient.from_connection_string(
                self.acs_connection_string
            )
            call_connection = acs_client.get_call_connection(call_connection_id)
            await call_connection.transfer_call_to_participant(
                target_participant=PhoneNumberIdentifier(target)
            )
            logger.info(
                "Transfer initiated: call_connection_id=%s target=%s",
                call_connection_id, target,
            )
            return {"status": "initiated", "target": target}
        except Exception as e:
            logger.error("Transfer failed: %s", e)
            return {"status": "failed", "reason": str(e)}

    async def send_message(self, message: Data):
        """Sends data back to client WebSocket."""
        try:
            await self.incoming_websocket.send(message)
        except Exception:
            logger.exception("[VoiceLiveACSHandler] Failed to send message")

    async def voicelive_to_acs(self, base64_data):
        """Converts Voice Live audio delta to ACS audio message."""
        try:
            data = {
                "Kind": "AudioData",
                "AudioData": {"Data": base64_data},
                "StopAudio": None,
            }
            await self.send_message(json.dumps(data))
        except Exception:
            logger.exception("[VoiceLiveACSHandler] Error in voicelive_to_acs")

    async def stop_audio(self):
        """Sends a StopAudio signal to ACS."""
        stop_audio_data = {"Kind": "StopAudio", "AudioData": None, "StopAudio": {}}
        await self.send_message(json.dumps(stop_audio_data))
        
        # Clear TTS buffer when user starts speaking
        if self._ambient_mixer is not None:
            async with self._tts_buffer_lock:
                self._tts_output_buffer.clear()
                self._tts_playback_started = False

    async def _send_continuous_audio(self, chunk_size: int) -> None:
        """
        Send continuous audio (ambient + TTS if available) back to client.
        
        Called for every incoming audio frame, ensuring continuous output.
        Uses buffered TTS with minimum buffer threshold to prevent mid-word cuts.
        
        Args:
            chunk_size: Size of audio chunk to send (matches incoming frame size)
        """
        if self._ambient_mixer is None or not self._ambient_mixer.is_enabled():
            return  # Ambient disabled, skip
            
        try:
            async with self._tts_buffer_lock:
                buffer_len = len(self._tts_output_buffer)
                
                # Always get a consistent ambient chunk first
                ambient_bytes = self._ambient_mixer.get_ambient_only_chunk(chunk_size)
                
                # Determine if we should play TTS
                should_play_tts = False
                if self._tts_playback_started:
                    # Already playing - continue until buffer empty
                    if buffer_len >= chunk_size:
                        should_play_tts = True
                    elif buffer_len > 0:
                        # Partial buffer but still playing - use what we have
                        should_play_tts = True
                    else:
                        # Buffer empty - stop playback mode
                        self._tts_playback_started = False
                else:
                    # Not yet playing - wait for minimum buffer
                    if buffer_len >= self._min_buffer_to_start:
                        self._tts_playback_started = True
                        should_play_tts = True
                
                if should_play_tts and buffer_len >= chunk_size:
                    # Full TTS chunk available - add TTS on top of ambient
                    tts_chunk = bytes(self._tts_output_buffer[:chunk_size])
                    del self._tts_output_buffer[:chunk_size]
                    
                    # Mix: ambient (constant) + TTS
                    ambient = np.frombuffer(ambient_bytes, dtype=np.int16).astype(np.float32) / 32768.0
                    tts = np.frombuffer(tts_chunk, dtype=np.int16).astype(np.float32) / 32768.0
                    mixed = ambient + tts
                    mixed = np.clip(mixed, -0.95, 0.95)  # Soft limit
                    output_bytes = (mixed * 32767).astype(np.int16).tobytes()
                    
                elif should_play_tts and buffer_len > 0:
                    # Partial TTS remaining at end of speech - drain it
                    tts_chunk = bytes(self._tts_output_buffer[:])
                    self._tts_output_buffer.clear()
                    self._tts_playback_started = False
                    
                    ambient = np.frombuffer(ambient_bytes, dtype=np.int16).astype(np.float32) / 32768.0
                    
                    # Only mix TTS for the portion we have
                    tts_samples = len(tts_chunk) // 2
                    tts = np.frombuffer(tts_chunk, dtype=np.int16).astype(np.float32) / 32768.0
                    ambient[:tts_samples] += tts
                    mixed = np.clip(ambient, -0.95, 0.95)
                    output_bytes = (mixed * 32767).astype(np.int16).tobytes()
                    
                else:
                    # No TTS ready - just send constant ambient
                    output_bytes = ambient_bytes
            
            # Send to client
            if self.is_raw_audio:
                # Web browser - raw bytes
                await self.send_message(output_bytes)
            else:
                # Phone call - JSON wrapped
                output_b64 = base64.b64encode(output_bytes).decode("ascii")
                data = {
                    "Kind": "AudioData",
                    "AudioData": {"Data": output_b64},
                    "StopAudio": None,
                }
                await self.send_message(json.dumps(data))
                
        except Exception:
            logger.exception("[VoiceLiveACSHandler] Error in _send_continuous_audio")

    async def acs_to_voicelive(self, stream_data):
        """Processes audio from ACS and forwards to Voice Live if not silent."""
        try:
            data = json.loads(stream_data)
            if data.get("kind") == "AudioData":
                audio_data = data.get("audioData", {})
                incoming_data = audio_data.get("data", "")
                
                # Determine chunk size from incoming audio
                if incoming_data:
                    incoming_bytes = base64.b64decode(incoming_data)
                    chunk_size = len(incoming_bytes)
                else:
                    chunk_size = DEFAULT_CHUNK_SIZE
                
                # Send continuous audio back to caller (ambient + TTS mixed)
                await self._send_continuous_audio(chunk_size)
                
                # Forward non-silent audio to Voice Live (existing logic)
                if not audio_data.get("silent", True):
                    await self.audio_to_voicelive(audio_data.get("data"))
        except Exception:
            logger.exception("[VoiceLiveACSHandler] Error processing ACS audio")

    async def web_to_voicelive(self, audio_bytes):
        """Encodes raw audio bytes and sends to Voice Live API."""
        chunk_size = len(audio_bytes)
        
        # Send continuous audio back to browser (ambient + TTS mixed)
        await self._send_continuous_audio(chunk_size)
        
        # Forward to Voice Live
        audio_b64 = base64.b64encode(audio_bytes).decode("ascii")
        await self.audio_to_voicelive(audio_b64)
