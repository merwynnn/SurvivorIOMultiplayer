import asyncio
import http
import random
import string

import websockets
import time
import signal
import os
from RemoteSession import RemoteSession

class RemoteServer:
    def __init__(self):
        self.sessions = {}

        try:
            self.port = int(os.environ["PORT"])
        except KeyError:
            self.port = 25565
        asyncio.run(self.main())

    async def main(self):
        print("Starting the server...")
        # Set the stop condition when receiving SIGTERM.
        loop = asyncio.get_running_loop()
        stop = loop.create_future()
        try:
            loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)
        except NotImplementedError:
            pass
        print("Server running on port ", self.port)
        async with websockets.serve(self.handler, "0.0.0.0", self.port, process_request=self.health_check):
            await asyncio.Future()  # run forever

        await stop

    async def health_check(self, path, request_headers):
        if path == "/healthz":
            return http.HTTPStatus.OK, [], b"OK\n"

    async def handler(self, websocket):
        async for m in websocket:
            message = m.split(',')

            if message[0] == "ToHost":
                session = self.sessions[message[1]]
                message.insert(3, session.websockets[websocket])
                await session.host.send(",".join(message[2::]))

            elif message[0] == "ToClient":
                session = self.sessions[message[1]]
                client_websocket = session.clients_id[message[2]]
                await client_websocket.send(",".join(message[3::]))

            elif message[0] == "Host":
                new_session = RemoteSession(websocket)
                self.sessions[new_session.id] = new_session
                await websocket.send("SessionInfo,"+new_session.id)

            elif message[0] == "ConnectToHost":
                session = self.sessions.get(message[1])
                if session:
                    id = self.get_id()
                    session.clients_id[id] = websocket
                    session.websockets[websocket] = id
                    await session.host.send(f"OnConnect,{id},{','.join(message[2::])}")


    def get_id(self):
        numbers = "0123456789"
        return ''.join(random.sample(string.ascii_letters + numbers, 10))  # Generate a random link

remoteServer = RemoteServer()
