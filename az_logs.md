2026-03-12T16:49:11.967699166Z 2026-03-12 16:49:11,966 app.handler.acs_event_handler INFO: MediaStreamingSubscription:--> <azure.communication.callautomation._models.MediaStreamingSubscription object at 0x755d4dd94ec0>
2026-03-12T16:49:11.967719597Z 2026-03-12 16:49:11,966 app.handler.acs_event_handler INFO: Received CallConnected event for connection id: 1f005880-9aed-4ac4-9f48-e9da16a2b28b
2026-03-12T16:49:11.967727809Z 2026-03-12 16:49:11,966 app.handler.acs_event_handler INFO: CORRELATION ID:--> 7c5b03fb-dc3d-43c2-8046-1f67ff795990
2026-03-12T16:49:11.967744024Z 2026-03-12 16:49:11,966 app.handler.acs_event_handler INFO: CALL CONNECTION ID:--> 1f005880-9aed-4ac4-9f48-e9da16a2b28b
2026-03-12T16:49:11.968639850Z [2026-03-12 16:49:11 +0000] [1] [INFO] 100.100.0.191:60614 POST /acs/callbacks/9e4894d1-bbdb-4682-8605-5367ee9e4e93 1.1 200 - 98589
2026-03-12T16:49:12.092900610Z 2026-03-12 16:49:12,092 app.handler.acs_event_handler INFO: Received Event:-> Microsoft.Communication.ParticipantsUpdated, Correlation Id:-> 7c5b03fb-dc3d-43c2-8046-1f67ff795990, CallConnectionId:-> 1f005880-9aed-4ac4-9f48-e9da16a2b28b
2026-03-12T16:49:12.093965012Z [2026-03-12 16:49:12 +0000] [1] [INFO] 100.100.0.191:60614 POST /acs/callbacks/9e4894d1-bbdb-4682-8605-5367ee9e4e93 1.1 200 - 2206
2026-03-12T16:49:13.894286668Z 2026-03-12 16:49:13,894 app.handler.acs_media_handler INFO: AI: Thank you for calling County Services. I can help direct your call. Who or what department are you trying to reach today?
2026-03-12T16:49:13.894909800Z 2026-03-12 16:49:13,894 app.handler.acs_media_handler INFO: Response Done: Id=resp_1Ub3VW7AZaH0Il3tbCVUGM
2026-03-12T16:49:20.759574273Z 2026-03-12 16:49:20,759 app.handler.acs_media_handler INFO: Voice activity detection started at 8669 ms
2026-03-12T16:49:22.158122253Z 2026-03-12 16:49:22,157 app.handler.acs_media_handler INFO: Speech stopped
2026-03-12T16:49:22.991861573Z 2026-03-12 16:49:22,991 app.handler.acs_media_handler INFO: User: I wanna pay for a permit.
2026-03-12T16:49:25.729236916Z 2026-03-12 16:49:25,729 app.handler.acs_media_handler INFO: AI: Thank you for letting me know. Permits are handled by the Public Works department. I can connect you to Public Works. Does that sound right?
2026-03-12T16:49:25.729682821Z 2026-03-12 16:49:25,729 app.handler.acs_media_handler INFO: Response Done: Id=resp_17kQRmqUm7bvNSHqj9ahww
2026-03-12T16:49:32.839796145Z 2026-03-12 16:49:32,839 app.handler.acs_media_handler INFO: Voice activity detection started at 20749 ms
2026-03-12T16:49:33.378909962Z 2026-03-12 16:49:33,378 app.handler.acs_media_handler INFO: Speech stopped
2026-03-12T16:49:33.484074020Z 2026-03-12 16:49:33,483 app.handler.acs_media_handler INFO: User: Ja.
2026-03-12T16:49:34.659336124Z 2026-03-12 16:49:34,659 app.handler.acs_media_handler INFO: AI: I will transfer you to Public Works now.
2026-03-12T16:49:34.659571480Z 2026-03-12 16:49:34,659 app.handler.acs_media_handler INFO: ROUTING: department=Public Works mode=live target=+19453821555
2026-03-12T16:49:34.660776034Z 2026-03-12 16:49:34,660 azure.core.pipeline.policies.http_logging_policy INFO: Request URL: 'https://acs-smecpocaiccas-3cfyc.unitedstates.communication.azure.com/calling/callConnections/1f005880-9aed-4ac4-9f48-e9da16a2b28b:transferToParticipant?api-version=REDACTED'
2026-03-12T16:49:34.660797627Z Request method: 'POST'
2026-03-12T16:49:34.660805709Z Request headers:
2026-03-12T16:49:34.660842525Z     'Content-Type': 'application/json'
2026-03-12T16:49:34.660849385Z     'Content-Length': '92'
2026-03-12T16:49:34.660856165Z     'Repeatability-First-Sent': 'REDACTED'
2026-03-12T16:49:34.660863036Z     'Repeatability-Request-ID': 'REDACTED'
2026-03-12T16:49:34.660869936Z     'Accept': 'application/json'
2026-03-12T16:49:34.660876777Z     'x-ms-client-request-id': '72fde434-1e33-11f1-a909-cea82f4f6847'
2026-03-12T16:49:34.660883577Z     'User-Agent': 'azsdk-python-communication-callautomation/1.5.0 Python/3.12.13 (Linux-6.6.121.1-1.azl3-x86_64-with-glibc2.36)'
2026-03-12T16:49:34.660890257Z     'x-ms-date': 'REDACTED'
2026-03-12T16:49:34.660897178Z     'x-ms-content-sha256': 'REDACTED'
2026-03-12T16:49:34.660903697Z     'x-ms-return-client-request-id': 'true'
2026-03-12T16:49:34.660931820Z     'Authorization': 'REDACTED'
2026-03-12T16:49:34.660939111Z A body is sent with the request
2026-03-12T16:49:34.729353636Z 2026-03-12 16:49:34,729 azure.core.pipeline.policies.http_logging_policy INFO: Response status: 202
2026-03-12T16:49:34.729396511Z Response headers:
2026-03-12T16:49:34.729405905Z     'Date': 'Thu, 12 Mar 2026 16:49:34 GMT'
2026-03-12T16:49:34.729413406Z     'Content-Type': 'application/json; charset=utf-8'
2026-03-12T16:49:34.729436912Z     'Transfer-Encoding': 'chunked'
2026-03-12T16:49:34.729444553Z     'Connection': 'keep-alive'
2026-03-12T16:49:34.729451153Z     'MS-CV': 'REDACTED'
2026-03-12T16:49:34.729457783Z     'Repeatability-Result': 'REDACTED'
2026-03-12T16:49:34.729464574Z     'X-Microsoft-Skype-Client': 'REDACTED'
2026-03-12T16:49:34.729471344Z     'X-Ms-Client-Version': 'REDACTED'
2026-03-12T16:49:34.729478294Z     'api-supported-versions': 'REDACTED'
2026-03-12T16:49:34.729485255Z     'x-ms-client-request-id': '72fde434-1e33-11f1-a909-cea82f4f6847'
2026-03-12T16:49:34.729951892Z     'X-Microsoft-Skype-Chain-ID': 'REDACTED'
2026-03-12T16:49:34.729960415Z     'x-azure-ref': 'REDACTED'
2026-03-12T16:49:34.729966213Z     'Strict-Transport-Security': 'REDACTED'
2026-03-12T16:49:34.729972002Z     'X-Cache': 'REDACTED'
2026-03-12T16:49:34.730921419Z 2026-03-12 16:49:34,729 app.handler.acs_media_handler INFO: Transfer initiated: call_connection_id=1f005880-9aed-4ac4-9f48-e9da16a2b28b target=+19453821555
2026-03-12T16:49:34.730935981Z 2026-03-12 16:49:34,729 asyncio ERROR: Unclosed client session
2026-03-12T16:49:34.730944063Z client_session: <aiohttp.client.ClientSession object at 0x755d4d220e00>
2026-03-12T16:49:34.730950754Z source_traceback: Object created at (most recent call last):
2026-03-12T16:49:34.730964955Z   File "/app/server.py", line 136, in <module>
2026-03-12T16:49:34.730971575Z     app.run(debug=True, host="0.0.0.0", port=8000)
2026-03-12T16:49:34.730977995Z   File "/app/.venv/lib/python3.12/site-packages/quart/app.py", line 878, in run
2026-03-12T16:49:34.730984384Z     loop.run_until_complete(asyncio.gather(*tasks))
2026-03-12T16:49:34.730990684Z   File "/usr/local/lib/python3.12/asyncio/base_events.py", line 678, in run_until_complete
2026-03-12T16:49:34.730997134Z     self.run_forever()
2026-03-12T16:49:34.731003614Z   File "/usr/local/lib/python3.12/asyncio/base_events.py", line 645, in run_forever
2026-03-12T16:49:34.731010073Z     self._run_once()
2026-03-12T16:49:34.731016613Z   File "/usr/local/lib/python3.12/asyncio/base_events.py", line 1991, in _run_once
2026-03-12T16:49:34.731022913Z     handle._run()
2026-03-12T16:49:34.731029373Z   File "/usr/local/lib/python3.12/asyncio/events.py", line 88, in _run
2026-03-12T16:49:34.731035802Z     self._context.run(self._callback, *self._args)
2026-03-12T16:49:34.731042272Z   File "/app/app/handler/acs_media_handler.py", line 240, in _receiver_loop
2026-03-12T16:49:34.731048832Z     await self._handle_transfer(department)
2026-03-12T16:49:34.731055372Z   File "/app/app/handler/acs_media_handler.py", line 303, in _handle_transfer
2026-03-12T16:49:34.731061942Z     result = await self._transfer_call(call_connection_id, target)
2026-03-12T16:49:34.731068322Z   File "/app/app/handler/acs_media_handler.py", line 316, in _transfer_call
2026-03-12T16:49:34.731074992Z     await call_connection.transfer_call_to_participant(
2026-03-12T16:49:34.731082793Z   File "/app/.venv/lib/python3.12/site-packages/azure/core/tracing/decorator_async.py", line 119, in wrapper_use_tracer
2026-03-12T16:49:34.731089243Z     return await func(*args, **kwargs)
2026-03-12T16:49:34.731096054Z   File "/app/.venv/lib/python3.12/site-packages/azure/communication/callautomation/aio/_call_connection_client_async.py", line 278, in transfer_call_to_participant
2026-03-12T16:49:34.731102533Z     result = await self._call_connection_client.transfer_to_participant(self._call_connection_id, request, **kwargs)
2026-03-12T16:49:34.731108853Z   File "/app/.venv/lib/python3.12/site-packages/azure/core/tracing/decorator_async.py", line 119, in wrapper_use_tracer
2026-03-12T16:49:34.731115333Z     return await func(*args, **kwargs)
2026-03-12T16:49:34.731121853Z   File "/app/.venv/lib/python3.12/site-packages/azure/communication/callautomation/_generated/aio/operations/_operations.py", line 895, in transfer_to_participant
2026-03-12T16:49:34.731128292Z     pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
2026-03-12T16:49:34.731134852Z   File "/app/.venv/lib/python3.12/site-packages/azure/core/pipeline/_base_async.py", line 229, in run
2026-03-12T16:49:34.731141362Z     return await first_node.send(pipeline_request)
2026-03-12T16:49:34.731147752Z   File "/app/.venv/lib/python3.12/site-packages/azure/core/pipeline/_base_async.py", line 77, in send
2026-03-12T16:49:34.731161352Z     response = await self.next.send(request)
2026-03-12T16:49:34.731166801Z   File "/app/.venv/lib/python3.12/site-packages/azure/core/pipeline/_base_async.py", line 77, in send
2026-03-12T16:49:34.731171938Z     response = await self.next.send(request)
2026-03-12T16:49:34.731177277Z   File "/app/.venv/lib/python3.12/site-packages/azure/core/pipeline/_base_async.py", line 77, in send
2026-03-12T16:49:34.731182384Z     response = await self.next.send(request)
2026-03-12T16:49:34.731187602Z   [Previous line repeated 2 more times]
2026-03-12T16:49:34.731192950Z   File "/app/.venv/lib/python3.12/site-packages/azure/core/pipeline/policies/_redirect_async.py", line 76, in send
2026-03-12T16:49:34.731198338Z     response = await self.next.send(request)
2026-03-12T16:49:34.731205029Z   File "/app/.venv/lib/python3.12/site-packages/azure/core/pipeline/policies/_retry_async.py", line 178, in send
2026-03-12T16:49:34.731210507Z     response = await self.next.send(request)
2026-03-12T16:49:34.731215815Z   File "/app/.venv/lib/python3.12/site-packages/azure/core/pipeline/_base_async.py", line 77, in send
2026-03-12T16:49:34.731220953Z     response = await self.next.send(request)
2026-03-12T16:49:34.731226241Z   File "/app/.venv/lib/python3.12/site-packages/azure/core/pipeline/_base_async.py", line 77, in send
2026-03-12T16:49:34.731231559Z     response = await self.next.send(request)
2026-03-12T16:49:34.731237598Z   File "/app/.venv/lib/python3.12/site-packages/azure/core/pipeline/_base_async.py", line 77, in send
2026-03-12T16:49:34.731244278Z     response = await self.next.send(request)
2026-03-12T16:49:34.731249566Z   [Previous line repeated 3 more times]
2026-03-12T16:49:34.731254794Z   File "/app/.venv/lib/python3.12/site-packages/azure/core/pipeline/_base_async.py", line 111, in send
2026-03-12T16:49:34.731260022Z     await self._sender.send(request.http_request, **request.context.options),
2026-03-12T16:49:34.731265390Z   File "/app/.venv/lib/python3.12/site-packages/azure/core/pipeline/transport/_aiohttp.py", line 311, in send
2026-03-12T16:49:34.731270788Z     await self.open()
2026-03-12T16:49:34.731277909Z   File "/app/.venv/lib/python3.12/site-packages/azure/core/pipeline/transport/_aiohttp.py", line 190, in open
2026-03-12T16:49:34.731283497Z     self.session = aiohttp.ClientSession(**clientsession_kwargs)
2026-03-12T16:49:34.731288836Z 2026-03-12 16:49:34,730 asyncio ERROR: Unclosed connector
2026-03-12T16:49:34.731293983Z connections: ['deque([(<aiohttp.client_proto.ResponseHandler object at 0x755d4d363b90>, 549506.741963255)])']
2026-03-12T16:49:34.731299171Z connector: <aiohttp.connector.TCPConnector object at 0x755d4d220e60>
2026-03-12T16:49:34.731304379Z source_traceback: Object created at (most recent call last):
2026-03-12T16:49:34.731309667Z   File "/app/server.py", line 136, in <module>
2026-03-12T16:49:34.731315286Z     app.run(debug=True, host="0.0.0.0", port=8000)
2026-03-12T16:49:34.731320974Z   File "/app/.venv/lib/python3.12/site-packages/quart/app.py", line 878, in run
2026-03-12T16:49:34.731326503Z     loop.run_until_complete(asyncio.gather(*tasks))
2026-03-12T16:49:34.731332071Z   File "/usr/local/lib/python3.12/asyncio/base_events.py", line 678, in run_until_complete
2026-03-12T16:49:34.731337699Z     self.run_forever()
2026-03-12T16:49:34.731343248Z   File "/usr/local/lib/python3.12/asyncio/base_events.py", line 645, in run_forever
2026-03-12T16:49:34.731348466Z     self._run_once()
2026-03-12T16:49:34.731353664Z   File "/usr/local/lib/python3.12/asyncio/base_events.py", line 1991, in _run_once
2026-03-12T16:49:34.731359022Z     handle._run()
2026-03-12T16:49:34.731369077Z   File "/usr/local/lib/python3.12/asyncio/events.py", line 88, in _run
2026-03-12T16:49:34.731374625Z     self._context.run(self._callback, *self._args)
2026-03-12T16:49:34.731380094Z   File "/app/app/handler/acs_media_handler.py", line 240, in _receiver_loop
2026-03-12T16:49:34.731385662Z     await self._handle_transfer(department)
2026-03-12T16:49:34.731390850Z   File "/app/app/handler/acs_media_handler.py", line 303, in _handle_transfer
2026-03-12T16:49:34.731396378Z     result = await self._transfer_call(call_connection_id, target)
2026-03-12T16:49:34.731401827Z   File "/app/app/handler/acs_media_handler.py", line 316, in _transfer_call
2026-03-12T16:49:34.731406874Z     await call_connection.transfer_call_to_participant(
2026-03-12T16:49:34.731411842Z   File "/app/.venv/lib/python3.12/site-packages/azure/core/tracing/decorator_async.py", line 119, in wrapper_use_tracer
2026-03-12T16:49:34.731416689Z     return await func(*args, **kwargs)
2026-03-12T16:49:34.731422758Z   File "/app/.venv/lib/python3.12/site-packages/azure/communication/callautomation/aio/_call_connection_client_async.py", line 278, in transfer_call_to_participant
2026-03-12T16:49:34.731427896Z     result = await self._call_connection_client.transfer_to_participant(self._call_connection_id, request, **kwargs)
2026-03-12T16:49:34.731433204Z   File "/app/.venv/lib/python3.12/site-packages/azure/core/tracing/decorator_async.py", line 119, in wrapper_use_tracer
2026-03-12T16:49:34.731438342Z     return await func(*args, **kwargs)
2026-03-12T16:49:34.731443460Z   File "/app/.venv/lib/python3.12/site-packages/azure/communication/callautomation/_generated/aio/operations/_operations.py", line 895, in transfer_to_participant
2026-03-12T16:49:34.731448487Z     pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
2026-03-12T16:49:34.731453665Z   File "/app/.venv/lib/python3.12/site-packages/azure/core/pipeline/_base_async.py", line 229, in run
2026-03-12T16:49:34.731459083Z     return await first_node.send(pipeline_request)
2026-03-12T16:49:34.731464722Z   File "/app/.venv/lib/python3.12/site-packages/azure/core/pipeline/_base_async.py", line 77, in send
2026-03-12T16:49:34.731497021Z     response = await self.next.send(request)
2026-03-12T16:49:34.731504272Z   File "/app/.venv/lib/python3.12/site-packages/azure/core/pipeline/_base_async.py", line 77, in send
2026-03-12T16:49:34.731511192Z     response = await self.next.send(request)
2026-03-12T16:49:34.731517993Z   File "/app/.venv/lib/python3.12/site-packages/azure/core/pipeline/_base_async.py", line 77, in send
2026-03-12T16:49:34.731525304Z     response = await self.next.send(request)
2026-03-12T16:49:34.731578334Z   [Previous line repeated 2 more times]
2026-03-12T16:49:34.731586186Z   File "/app/.venv/lib/python3.12/site-packages/azure/core/pipeline/policies/_redirect_async.py", line 76, in send
2026-03-12T16:49:34.731593226Z     response = await self.next.send(request)
2026-03-12T16:49:34.731610973Z   File "/app/.venv/lib/python3.12/site-packages/azure/core/pipeline/policies/_retry_async.py", line 178, in send
2026-03-12T16:49:34.731617854Z     response = await self.next.send(request)
2026-03-12T16:49:34.731624754Z   File "/app/.venv/lib/python3.12/site-packages/azure/core/pipeline/_base_async.py", line 77, in send
2026-03-12T16:49:34.731631534Z     response = await self.next.send(request)
2026-03-12T16:49:34.731658405Z   File "/app/.venv/lib/python3.12/site-packages/azure/core/pipeline/_base_async.py", line 77, in send
2026-03-12T16:49:34.731665456Z     response = await self.next.send(request)
2026-03-12T16:49:34.731672577Z   File "/app/.venv/lib/python3.12/site-packages/azure/core/pipeline/_base_async.py", line 77, in send
2026-03-12T16:49:34.731685787Z     response = await self.next.send(request)
2026-03-12T16:49:34.731702352Z   [Previous line repeated 3 more times]
2026-03-12T16:49:34.731708080Z   File "/app/.venv/lib/python3.12/site-packages/azure/core/pipeline/_base_async.py", line 111, in send
2026-03-12T16:49:34.731713699Z     await self._sender.send(request.http_request, **request.context.options),
2026-03-12T16:49:34.731776534Z   File "/app/.venv/lib/python3.12/site-packages/azure/core/pipeline/transport/_aiohttp.py", line 311, in send
2026-03-12T16:49:34.731791367Z     await self.open()
2026-03-12T16:49:34.731797105Z   File "/app/.venv/lib/python3.12/site-packages/azure/core/pipeline/transport/_aiohttp.py", line 190, in open
2026-03-12T16:49:34.731828883Z     self.session = aiohttp.ClientSession(**clientsession_kwargs)
2026-03-12T16:49:34.731849525Z   File "/app/.venv/lib/python3.12/site-packages/aiohttp/client.py", line 372, in __init__
2026-03-12T16:49:34.731855414Z     connector = TCPConnector(
2026-03-12T16:49:34.731861533Z   File "/app/.venv/lib/python3.12/site-packages/aiohttp/connector.py", line 963, in __init__
2026-03-12T16:49:34.731867342Z     super().__init__(
2026-03-12T16:49:34.731873040Z 2026-03-12 16:49:34,730 app.handler.acs_media_handler INFO: Response Done: Id=resp_4e1cID3qGAko4eMsBsOZft
2026-03-12T16:49:35.572835088Z 2026-03-12 16:49:35,572 app.handler.acs_event_handler INFO: Received Event:-> Microsoft.Communication.CallTransferFailed, Correlation Id:-> 7c5b03fb-dc3d-43c2-8046-1f67ff795990, CallConnectionId:-> 1f005880-9aed-4ac4-9f48-e9da16a2b28b
2026-03-12T16:49:35.572885605Z 2026-03-12 16:49:35,572 app.handler.acs_event_handler WARNING: Transfer FAILED for: 1f005880-9aed-4ac4-9f48-e9da16a2b28b  {'version': '2025-06-15', 'resultInformation': {'code': 400, 'subCode': 580042, 'message': 'Bad Request. DiagCode: 400#580042.@'}, 'callConnectionId': '1f005880-9aed-4ac4-9f48-e9da16a2b28b', 'serverCallId': 'aHR0cHM6Ly9hcGkuZmxpZ2h0cHJveHkuc2t5cGUuY29tL2FwaS92Mi9jcC9jb252LXVzd2UtMDQtcHJvZC1ha3MuY29udi5za3lwZS5jb20vY29udi90YjhURWZaVzBrS0M3aGU4VVVUamd3P2k9MTAtMTI4LTE2MS0xNzYmZT02MzkwODgzMTczMTgyODc0OTk=', 'correlationId': '7c5b03fb-dc3d-43c2-8046-1f67ff795990', 'publicEventType': 'Microsoft.Communication.CallTransferFailed'}
2026-03-12T16:49:35.573961383Z [2026-03-12 16:49:35 +0000] [1] [INFO] 100.100.0.191:47970 POST /acs/callbacks/9e4894d1-bbdb-4682-8605-5367ee9e4e93 1.1 200 - 2304
2026-03-12T16:49:58.628001997Z 2026-03-12 16:49:58,627 app.handler.acs_event_handler INFO: Received Event:-> Microsoft.Communication.MediaStreamingStopped, Correlation Id:-> 7c5b03fb-dc3d-43c2-8046-1f67ff795990, CallConnectionId:-> 1f005880-9aed-4ac4-9f48-e9da16a2b28b
2026-03-12T16:49:58.628084141Z 2026-03-12 16:49:58,627 app.handler.acs_event_handler INFO: Media streaming content type:--> Audio
2026-03-12T16:49:58.628122849Z 2026-03-12 16:49:58,627 app.handler.acs_event_handler INFO: Media streaming status:--> mediaStreamingStopped
2026-03-12T16:49:58.628234368Z 2026-03-12 16:49:58,627 app.handler.acs_event_handler INFO: Media streaming status details:--> streamConnectionInterrupted
2026-03-12T16:49:58.629364130Z [2026-03-12 16:49:58 +0000] [1] [INFO] 100.100.0.191:37458 POST /acs/callbacks/9e4894d1-bbdb-4682-8605-5367ee9e4e93 1.1 200 - 3666
2026-03-12T16:49:58.692214994Z 2026-03-12 16:49:58,692 acs_ws INFO: ACS WebSocket cancelled
2026-03-12T16:49:58.695100573Z [2026-03-12 16:49:58 +0000] [1] [ERROR] Error in ASGI Framework
2026-03-12T16:49:58.695123318Z Traceback (most recent call last):
2026-03-12T16:49:58.695131470Z   File "/app/.venv/lib/python3.12/site-packages/hypercorn/asyncio/task_group.py", line 27, in _handle
2026-03-12T16:49:58.695138431Z     await app(scope, receive, send, sync_spawn, call_soon)
2026-03-12T16:49:58.695146002Z   File "/app/.venv/lib/python3.12/site-packages/hypercorn/app_wrappers.py", line 34, in __call__
2026-03-12T16:49:58.695161956Z     await self.app(scope, receive, send)
2026-03-12T16:49:58.695167685Z   File "/app/.venv/lib/python3.12/site-packages/quart/app.py", line 1735, in __call__
2026-03-12T16:49:58.695175026Z     await self.asgi_app(scope, receive, send)
2026-03-12T16:49:58.695180735Z   File "/app/.venv/lib/python3.12/site-packages/quart/app.py", line 1761, in asgi_app
2026-03-12T16:49:58.695186433Z     await asgi_handler(receive, send)
2026-03-12T16:49:58.695192002Z   File "/app/.venv/lib/python3.12/site-packages/quart/asgi.py", line 196, in __call__
2026-03-12T16:49:58.695197710Z     await cancel_tasks(pending)
2026-03-12T16:49:58.695203159Z   File "/app/.venv/lib/python3.12/site-packages/quart/utils.py", line 179, in cancel_tasks
2026-03-12T16:49:58.695208527Z     raise_task_exceptions(tasks)
2026-03-12T16:49:58.695214476Z   File "/app/.venv/lib/python3.12/site-packages/quart/utils.py", line 186, in raise_task_exceptions
2026-03-12T16:49:58.695220195Z     raise task.exception()
2026-03-12T16:49:58.695225763Z   File "/app/.venv/lib/python3.12/site-packages/quart/asgi.py", line 246, in handle_websocket
2026-03-12T16:49:58.695231442Z     response = await _handle_exception(self.app, error)
2026-03-12T16:49:58.695237000Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-03-12T16:49:58.695243079Z   File "/app/.venv/lib/python3.12/site-packages/quart/asgi.py", line 408, in _handle_exception
2026-03-12T16:49:58.695248948Z     raise error
2026-03-12T16:49:58.695254396Z   File "/app/.venv/lib/python3.12/site-packages/quart/asgi.py", line 244, in handle_websocket
2026-03-12T16:49:58.695260345Z     response = await self.app.handle_websocket(websocket)
2026-03-12T16:49:58.695287607Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-03-12T16:49:58.695293526Z   File "/app/.venv/lib/python3.12/site-packages/quart/app.py", line 1480, in handle_websocket
2026-03-12T16:49:58.695299354Z     return await self.handle_websocket_exception(error)
2026-03-12T16:49:58.695313666Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-03-12T16:49:58.695319184Z   File "/app/.venv/lib/python3.12/site-packages/quart/app.py", line 1476, in handle_websocket
2026-03-12T16:49:58.695324833Z     return await self.full_dispatch_websocket(websocket_context)
2026-03-12T16:49:58.695341348Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-03-12T16:49:58.695347157Z   File "/app/.venv/lib/python3.12/site-packages/quart/app.py", line 1525, in full_dispatch_websocket
2026-03-12T16:49:58.695353026Z     result = await self.handle_user_exception(error)
2026-03-12T16:49:58.695379546Z              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-03-12T16:49:58.695385585Z   File "/app/.venv/lib/python3.12/site-packages/quart/app.py", line 1059, in handle_user_exception
2026-03-12T16:49:58.695401609Z     raise error
2026-03-12T16:49:58.695407168Z   File "/app/.venv/lib/python3.12/site-packages/quart/app.py", line 1523, in full_dispatch_websocket
2026-03-12T16:49:58.695413367Z     result = await self.dispatch_websocket(websocket_context)
2026-03-12T16:49:58.695420288Z              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-03-12T16:49:58.695426046Z   File "/app/.venv/lib/python3.12/site-packages/quart/app.py", line 1613, in dispatch_websocket
2026-03-12T16:49:58.695431775Z     return await self.ensure_async(handler)(**websocket_.view_args)  # type: ignore[return-value]
2026-03-12T16:49:58.695437574Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-03-12T16:49:58.695443302Z   File "/app/server.py", line 95, in acs_ws
2026-03-12T16:49:58.695448851Z     await handler.stop_audio_output()
2026-03-12T16:49:58.695454590Z           ^^^^^^^^^^^^^^^^^^^^^^^^^
2026-03-12T16:49:58.695466718Z AttributeError: 'ACSMediaHandler' object has no attribute 'stop_audio_output'
2026-03-12T16:49:58.695472266Z 2026-03-12 16:49:58,692 hypercorn.error ERROR: Error in ASGI Framework
2026-03-12T16:49:58.695477945Z Traceback (most recent call last):
2026-03-12T16:49:58.695483754Z   File "/app/.venv/lib/python3.12/site-packages/hypercorn/asyncio/task_group.py", line 27, in _handle
2026-03-12T16:49:58.695489372Z     await app(scope, receive, send, sync_spawn, call_soon)
2026-03-12T16:49:58.695495051Z   File "/app/.venv/lib/python3.12/site-packages/hypercorn/app_wrappers.py", line 34, in __call__
2026-03-12T16:49:58.695500739Z     await self.app(scope, receive, send)
2026-03-12T16:49:58.695506348Z   File "/app/.venv/lib/python3.12/site-packages/quart/app.py", line 1735, in __call__
2026-03-12T16:49:58.695512197Z     await self.asgi_app(scope, receive, send)
2026-03-12T16:49:58.695517535Z   File "/app/.venv/lib/python3.12/site-packages/quart/app.py", line 1761, in asgi_app
2026-03-12T16:49:58.695536654Z     await asgi_handler(receive, send)
2026-03-12T16:49:58.695542312Z   File "/app/.venv/lib/python3.12/site-packages/quart/asgi.py", line 196, in __call__
2026-03-12T16:49:58.695548111Z     await cancel_tasks(pending)
2026-03-12T16:49:58.695553559Z   File "/app/.venv/lib/python3.12/site-packages/quart/utils.py", line 179, in cancel_tasks
2026-03-12T16:49:58.695559278Z     raise_task_exceptions(tasks)
2026-03-12T16:49:58.695575132Z   File "/app/.venv/lib/python3.12/site-packages/quart/utils.py", line 186, in raise_task_exceptions
2026-03-12T16:49:58.695580911Z     raise task.exception()
2026-03-12T16:49:58.695598107Z   File "/app/.venv/lib/python3.12/site-packages/quart/asgi.py", line 246, in handle_websocket
2026-03-12T16:49:58.695603705Z     response = await _handle_exception(self.app, error)
2026-03-12T16:49:58.695609534Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-03-12T16:49:58.695615083Z   File "/app/.venv/lib/python3.12/site-packages/quart/asgi.py", line 408, in _handle_exception
2026-03-12T16:49:58.695632469Z     raise error
2026-03-12T16:49:58.695638047Z   File "/app/.venv/lib/python3.12/site-packages/quart/asgi.py", line 244, in handle_websocket
2026-03-12T16:49:58.695643846Z     response = await self.app.handle_websocket(websocket)
2026-03-12T16:49:58.695649525Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-03-12T16:49:58.695664928Z   File "/app/.venv/lib/python3.12/site-packages/quart/app.py", line 1480, in handle_websocket
2026-03-12T16:49:58.695670767Z     return await self.handle_websocket_exception(error)
2026-03-12T16:49:58.695676646Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-03-12T16:49:58.695723026Z   File "/app/.venv/lib/python3.12/site-packages/quart/app.py", line 1476, in handle_websocket
2026-03-12T16:49:58.695743447Z     return await self.full_dispatch_websocket(websocket_context)
2026-03-12T16:49:58.695750508Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-03-12T16:49:58.695757288Z   File "/app/.venv/lib/python3.12/site-packages/quart/app.py", line 1525, in full_dispatch_websocket
2026-03-12T16:49:58.695764279Z     result = await self.handle_user_exception(error)
2026-03-12T16:49:58.695771049Z              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-03-12T16:49:58.695777949Z   File "/app/.venv/lib/python3.12/site-packages/quart/app.py", line 1059, in handle_user_exception
2026-03-12T16:49:58.695785040Z     raise error
2026-03-12T16:49:58.695791760Z   File "/app/.venv/lib/python3.12/site-packages/quart/app.py", line 1523, in full_dispatch_websocket
2026-03-12T16:49:58.695799011Z     result = await self.dispatch_websocket(websocket_context)
2026-03-12T16:49:58.695822797Z              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-03-12T16:49:58.695828456Z   File "/app/.venv/lib/python3.12/site-packages/quart/app.py", line 1613, in dispatch_websocket
2026-03-12T16:49:58.695834104Z     return await self.ensure_async(handler)(**websocket_.view_args)  # type: ignore[return-value]
2026-03-12T16:49:58.695839913Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-03-12T16:49:58.695845421Z   File "/app/server.py", line 95, in acs_ws
2026-03-12T16:49:58.695850850Z     await handler.stop_audio_output()
2026-03-12T16:49:58.695856218Z           ^^^^^^^^^^^^^^^^^^^^^^^^^
2026-03-12T16:49:58.695862137Z AttributeError: 'ACSMediaHandler' object has no attribute 'stop_audio_output'
2026-03-12T16:49:59.079518635Z 2026-03-12 16:49:59,078 app.handler.acs_event_handler INFO: Received Event:-> Microsoft.Communication.CallDisconnected, Correlation Id:-> 7c5b03fb-dc3d-43c2-8046-1f67ff795990, CallConnectionId:-> 1f005880-9aed-4ac4-9f48-e9da16a2b28b
2026-03-12T16:49:59.079555691Z 2026-03-12 16:49:59,078 app.handler.acs_event_handler INFO: CallDisconnected event received for: 1f005880-9aed-4ac4-9f48-e9da16a2b28b
2026-03-12T16:49:59.081413315Z [2026-03-12 16:49:59 +0000] [1] [INFO] 100.100.0.191:37458 POST /acs/callbacks/9e4894d1-bbdb-4682-8605-5367ee9e4e93 1.1 200 - 4243