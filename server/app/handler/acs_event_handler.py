"""Handler for processing ACS (Azure Communication Services) call and callback events."""

import json
import logging
import uuid
from urllib.parse import urlencode, urlparse, urlunparse

from azure.communication.callautomation import (AudioFormat,
                                                MediaStreamingAudioChannelType,
                                                MediaStreamingContentType,
                                                MediaStreamingOptions,
                                                StreamingTransportType)
from azure.communication.callautomation.aio import CallAutomationClient
from azure.eventgrid import EventGridEvent, SystemEventNames
from quart import Response

logger = logging.getLogger(__name__)


class AcsEventHandler:
    """Handles ACS event processing and call answering logic."""

    def __init__(self, config):
        self.acs_client = CallAutomationClient.from_connection_string(
            config["ACS_CONNECTION_STRING"]
        )

    async def process_incoming_call(self, events: list, host_url, config):
        """Processes incoming call events and answers calls with media streaming."""
        logger.info("incoming event data")

        for event_dict in events:
            event = EventGridEvent.from_dict(event_dict)
            logger.info("incoming event data --> %s", event.data)

            if (
                event.event_type
                == SystemEventNames.EventGridSubscriptionValidationEventName
            ):
                logger.info("Validating subscription")
                validation_code = event.data["validationCode"]
                return Response(
                    response=json.dumps({"validationResponse": validation_code}),
                    status=200,
                )

            if event.event_type == "Microsoft.Communication.IncomingCall":
                logger.info("Incoming call received: data=%s", event.data)

                caller_info = event.data["from"]
                caller_id = (
                    caller_info["phoneNumber"]["value"]
                    if caller_info["kind"] == "phoneNumber"
                    else caller_info["rawId"]
                )

                logger.info("incoming call handler caller id: %s", caller_id)
                incoming_call_context = event.data["incomingCallContext"]
                query_parameters = urlencode({"callerId": caller_id})
                guid = uuid.uuid4()

                callback_events_uri = (
                    f"{config['ACS_DEV_TUNNEL']}/acs/callbacks"
                    if config["ACS_DEV_TUNNEL"]
                    else f"{host_url}/acs/callbacks"
                )
                callback_uri = f"{callback_events_uri}/{guid}?{query_parameters}"

                parsed_url = urlparse(callback_events_uri)
                websocket_url = urlunparse(
                    ("wss", parsed_url.netloc, "/acs/ws", "", "", "")
                )

                logger.info("callback url: %s", callback_uri)
                logger.info("websocket url: %s", websocket_url)

                media_streaming_options = MediaStreamingOptions(
                    transport_url=websocket_url,
                    transport_type=StreamingTransportType.WEBSOCKET,
                    content_type=MediaStreamingContentType.AUDIO,
                    audio_channel_type=MediaStreamingAudioChannelType.MIXED,
                    start_media_streaming=True,
                    enable_bidirectional=True,
                    audio_format=AudioFormat.PCM24_K_MONO,
                )

                result = await self.acs_client.answer_call(
                    incoming_call_context=incoming_call_context,
                    operation_context="incomingCall",
                    callback_url=callback_uri,
                    media_streaming=media_streaming_options,
                )

                logger.info(
                    "Answered call for connection id: %s", result.call_connection_id
                )

                # Bridge call_connection_id to shared demo state for transfer
                demo_state = config.get("DEMO_CALL_STATE", {})
                demo_state["call_connection_id"] = result.call_connection_id
                demo_state["context_id"] = str(guid)

                return Response(status=200)

        return Response(status=400)

    async def demo_transfer_call(self, call_connection_id: str, target: str) -> dict:
        """Transfers an active call to target phone number (demo use)."""
        try:
            from azure.communication.callautomation import PhoneNumberIdentifier

            call_connection = self.acs_client.get_call_connection(call_connection_id)
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

    async def process_callback_events(self, context_id: str, raw_events: list, config):
        """Processes ACS callback events such as call connected, media started, etc."""
        for event in raw_events:
            event_data = event["data"]
            call_connection_id = event_data["callConnectionId"]

            logger.info(
                "Received Event:-> %s, Correlation Id:-> %s, CallConnectionId:-> %s",
                event["type"],
                event_data["correlationId"],
                call_connection_id,
            )

            if event["type"] == "Microsoft.Communication.CallConnected":
                properties = await self.acs_client.get_call_connection(
                    call_connection_id
                ).get_call_properties()

                logger.info(
                    "MediaStreamingSubscription:--> %s",
                    properties.media_streaming_subscription,
                )
                logger.info(
                    "Received CallConnected event for connection id: %s",
                    call_connection_id,
                )
                logger.info("CORRELATION ID:--> %s", event_data["correlationId"])
                logger.info("CALL CONNECTION ID:--> %s", call_connection_id)

            elif event["type"] == "Microsoft.Communication.MediaStreamingStarted":
                update = event_data["mediaStreamingUpdate"]
                logger.info(
                    "Media streaming content type:--> %s", update["contentType"]
                )
                logger.info(
                    "Media streaming status:--> %s", update["mediaStreamingStatus"]
                )
                logger.info(
                    "Media streaming status details:--> %s",
                    update["mediaStreamingStatusDetails"],
                )

            elif event["type"] == "Microsoft.Communication.MediaStreamingStopped":
                update = event_data["mediaStreamingUpdate"]
                logger.info(
                    "Media streaming content type:--> %s", update["contentType"]
                )
                logger.info(
                    "Media streaming status:--> %s", update["mediaStreamingStatus"]
                )
                logger.info(
                    "Media streaming status details:--> %s",
                    update["mediaStreamingStatusDetails"],
                )

            elif event["type"] == "Microsoft.Communication.MediaStreamingFailed":
                result_info = event_data["resultInformation"]
                logger.info(
                    "Code:-> %s, Subcode:-> %s",
                    result_info["code"],
                    result_info["subCode"],
                )
                logger.info("Message:-> %s", result_info["message"])

            elif event["type"] == "Microsoft.Communication.CallDisconnected":
                logger.info(
                    "CallDisconnected event received for: %s", call_connection_id
                )

            elif event["type"] == "Microsoft.Communication.CallTransferAccepted":
                logger.info("Transfer accepted for: %s", call_connection_id)

            elif event["type"] == "Microsoft.Communication.CallTransferFailed":
                logger.warning(
                    "Transfer FAILED for: %s  %s", call_connection_id, event_data
                )

        return Response(status=200)
