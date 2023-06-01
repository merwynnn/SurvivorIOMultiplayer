import asyncio

import websockets
from session import Session
from player import Player
import time
import signal
import os

class Server:
    def __init__(self):
        self.sessions = []

        self.files_check = self.get_files()

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
        print("Server running on port ", self.port)
        async with websockets.serve(self.handler, "0.0.0.0", self.port):
            await asyncio.Future()  # run forever

    async def handler(self, websocket):
        async for m in websocket:
            message = m.split(',')
            if message[0] == "GameInfo":
                for session in self.sessions:
                    if session.id == message[1]:
                        for i, player in enumerate(session.players):
                            if player.id == message[2]:
                                msg = session.on_received_message_from_player(player)
                                await player.websocket.send("GameInfo" + msg)
                                break
                        break

            elif message[0] == "Matchmaking":
                if len(message>2):
                    # Checking if the player is cheating
                    is_cheating = self.is_cheating(message[2:].join(","))
                    if not is_cheating:
                        matchmaking_info = await self.matchmaking(message[1:], websocket)
                        await websocket.send("MatchmakingInfo" + "," + str(matchmaking_info[0].id) + "," + str(matchmaking_info[1].id))
                        print(message[1], " joined the server !")
                        if matchmaking_info[0].full:            #If session is full, start the game
                            time.sleep(2)
                            await matchmaking_info[0].start()

    async def matchmaking(self, username, websocket):
        if not self.sessions or self.sessions[-1].full:   #If there is no open session, or if last session is full create one
            session = Session()
            self.sessions.append(session)
            new_player = Player(username, websocket)
            await session.join(new_player)
            new_player.session = session
        else:                                               #Join open session
            new_player = Player(username, websocket)
            session = self.sessions[-1]
            await session.join(new_player)
            new_player.session = session
        return (session, new_player)

    def is_cheating(self, message):
        # Anti-cheat system. Reads all the files in the client directory and check if they are the same as the one sent by the client
        files = {}
        message = message.split("///")
        for m in message:
            result = m.split("|||")
            if len(result) == 2:
                file, content = result
                files[file] = content
            else:
                return True

        for file_name, content in self.files_check.items():
            n = files.get(file_name)
            if n:
                if content != n:
                    return True
            else:
                return True
        return False

    def get_files(self):
        files = []
        dir = '../Client'
        for root, _, fs in os.walk(dir):
            for file_name in fs:
                if file_name.endswith(".py"):
                    files.append(os.path.join(root, file_name))

        e = {}
        for f in files:
            with open(f, 'r') as fi:
                e[os.path.basename(fi.name)] = fi.read()
        return e
server = Server()



