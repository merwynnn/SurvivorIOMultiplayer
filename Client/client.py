import random
import string
import os
import base64
import sys

import numpy as np
from websocket import create_connection

import pygame
from pygame.math import Vector2 as Vec2

import _thread

from WeaponsAbilities import KnivesAbility
from Zombie import DefaultZombie
from player import Player


class Client:
    link = "wss://survivol-io-multiplayer.fly.dev/"
    #link = "ws://online-pong-websocket.herokuapp.com/0.0.0.0"
    #link = "wss://survivoriomultiplayer.onrender.com"
    #link = "ws://localhost:25565"

    def __init__(self):
        self.win = None

        username = input("Type your username: ")
        if username == "":
            numbers = "0123456789"
            username = ''.join(random.sample(string.ascii_letters + numbers, 10))  # Generate a random link
            
        self.code = input("Code: ")

        self.player = Player(username)

        self.players = {}      # Exclude himself

        self.zombies = {}

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
            if result[0] == "CurrentGameInfo":
                player_infos = result[1].split("|")
                for player_info in player_infos:
                    player_id, infos = player_info.split(":")
                    infos = infos.split("/")
                    if player_id == self.player.id:
                        player = self.player
                    else:
                        player = self.players.get(player_id)
                        if not player:
                            break
                    if player_id != self.player.id:
                        pos = Vec2((int(infos[0]), int(infos[1])))
                        player.position = pos
                    player.health = int(infos[2])
                    player.max_health = int(infos[3])

                    abilities = infos[4].split("!")
                    for ab in abilities:
                        ability_name, *ability_infos = ab.split("%")
                        ability = None
                        for p_ab in self.player.abilities:
                            if p_ab.ability_name == ability_name:
                                ability = p_ab
                                break

                        if not ability:
                            abi = None
                            if ability_name == "KnivesAbility":
                                abi = KnivesAbility(self.win)
                            self.player.abilities.append(abi)
                            ability = abi

                        ability.set_ability_info(ability_infos)

                zombie_infos = result[2].split("|")
                for zombie_info in zombie_infos:
                    if zombie_info != "":
                        zombie_id, infos = zombie_info.split(":")
                        infos = infos.split("/")
                        zombie = self.zombies.get(zombie_id)
                        if not zombie:
                            if infos[0] == "DefaultZombie":
                                zombie = DefaultZombie(self.win, zombie_id, None)
                                self.zombies[zombie_id] = zombie

                        pos = Vec2((int(infos[1]), int(infos[2])))
                        zombie.position = pos
                        zombie.scale = float(infos[3])

            elif result[0] == "GameInfo":
                self.player.id = result[1]
                print("Waiting For Players... [" + result[2] + "/" + result[3] + "]")

            elif result[0] == "OnNewPlayerJoin":
                new_player = Player(result[2])
                new_player.id = result[1]
                self.players[new_player.id] = new_player
                print(f"{new_player.username} joined the server ! [" + result[3] + "/" + result[4] + "]")

            elif result[0] == "StartInfo":
                self.has_game_started = True

    def on_open(self):
        content = self.get_content()
        print("Connecting...")
        self.websocket.send(f"ConnectToHost,{self.code},{self.player.username},{content}") 

    def start(self):
        print("Game started")

        self.win = pygame.display.set_mode((600, 600))
        self.player.win = self.win
        self.player.on_start()

        for player in self.players.values():
            player.win = self.win
            player.on_start()

        screen_center = self.get_screen_center()

        clock = pygame.time.Clock()

        while True:
            # Main Loop
            dt = clock.tick()

            self.win.fill(self.background_color)
            events = pygame.event.get()
            mouse_pos = Vec2(pygame.mouse.get_pos())
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()

            delta = screen_center - self.player.position  # Used to make the player always centered on the screen

            self.player.frame(mouse_pos, events, dt)
            self.player.draw(delta=delta)

            for player in self.players.values():
                player.draw(delta=delta)

            zombies = list(self.zombies.values())
            for zombie in zombies:
                zombie.draw(delta=delta)

            self.send_to_server(f"CurrentGameInfo,{self.player.id},{self.get_player_info()}")

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

    def send_to_server(self, message):
        self.websocket.send(f"ToHost,{self.code},{message}")


client = Client()
