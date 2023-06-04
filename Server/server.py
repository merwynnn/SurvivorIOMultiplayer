import asyncio
import http

from websocket import create_connection
import _thread

from game import Game
from player import Player
import time
import signal
import os

class Server:
    link = "wss://survivoriomultiplayer.onrender.com"

    def __init__(self):  
        self.websocket = None
        
        self.code = None
        
        self.game = Game(self)
        
        self.main()

    def main(self):

        self.websocket = create_connection(self.link)
        self.on_open()
        self.on_message()
        #_thread.start_new_thread(self.on_message, ())

    def on_message(self):
        while True:
            message = self.websocket.recv()
            message = message.split(',')
            if message[0] == "CurrentGameInfo":
                client_id = message[1]
                for i, player in enumerate(self.game.players):
                    if player.id == message[2]:
                        msg = self.game.on_received_message_from_player(player, message[3::])
                        self.send_to_client(client_id, f"CurrentGameInfo,{msg}")
                        break
                        
            elif message[0] == "SessionInfo":
                self.code = message[1]
                print(f"Code: {self.code}")

            elif message[0] == "OnConnect":
                if not self.game.full:
                    # Checking if the player is cheating
                    is_cheating = False  # self.is_cheating(",".join(message[2:]))
                    if not is_cheating:
                        new_player = Player(self.game, username=message[2], client_id=message[1], websocket=self.websocket)
                        self.game.join(new_player)
                        self.send_to_client(new_player.client_id, f"GameInfo,{str(new_player.id)},{str(len(self.game.players))},{str(self.game.max_players)}")
                        print(message[2], " joined the server !")
                        if self.game.full:  # If session is full, start the game
                            self.game.start()
    
    def on_open(self):
        self.websocket.send("Host")

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

    def send_to_client(self, client_id, message):
        self.websocket.send(f"ToClient,{self.code},{client_id},{message}")

server = Server()



