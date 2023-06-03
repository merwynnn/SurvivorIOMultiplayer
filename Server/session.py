import asyncio
import math
import random
import string
from contextlib import suppress

from pygame.math import Vector2 as Vec2

from Zombie import DefaultZombie


class Session:
    def __init__(self):
        numbers = "0123456789"
        self.id = ''.join(random.sample(string.ascii_letters + numbers, 10))  # Generate a random link
        self.players = []

        self.max_players = 2
        self.full = False

        self.zombies = {}
        self.zombie_level = 1
        self.spawn_radius = 300


        self.spawn_zombie_task = None
        self.check_if_active_task = None
        self.game_loop_task = None


    async def join(self, new_player):
        if len(self.players) < self.max_players:
            for player in self.players:
                await player.websocket.send(
                    "OnNewPlayerJoin" + "," + str(new_player.id) + "," + str(new_player.username) + "," + str(len(self.players)+1) + "," + str(self.max_players))
                await new_player.websocket.send(
                    "OnNewPlayerJoin" + "," + str(player.id) + "," + str(player.username) + "," + str(len(self.players)+1) + "," + str(self.max_players))
            self.players.append(new_player)
            if len(self.players) == self.max_players:
                self.full = True

            return True
        else:
            return False

    def on_received_message_from_player(self, player, message):
        player.position = Vec2((int(message[0]), int(message[1])))
        msg = self.get_game_info_for_player(player)
        return msg

    def get_game_info_for_player(self, player):
        infos = []
        players = []
        for p in self.players:
            if p != player:
                players.append(f"{p.id}:{int(p.position[0])}/{int(p.position[1])}")

        infos.append("|".join(players))

        zombies = []
        for zombie in self.zombies.values():
            zombies.append(f"{zombie.id}:{zombie.class_name}/{int(zombie.position[0])}/{int(zombie.position[1])}")
        infos.append("|".join(zombies))

        return ",".join(infos)

    async def start(self):
        for player in self.players:
            await player.websocket.send("StartInfo")
        self.spawn_zombie_task = asyncio.ensure_future(self.spawn_zombies())
        self.check_if_active_task = asyncio.ensure_future(self.check_if_active())
        self.game_loop_task = asyncio.ensure_future(self.game_loop())

    async def stop_session(self):
        self.spawn_zombie_task.cancel()
        self.check_if_active_task.cancel()
        self.game_loop_task.cancel()
        with suppress(asyncio.CancelledError):
            await self.spawn_zombie_task
            await self.check_if_active_task
            await self.game_loop_task

    async def game_loop(self):
        while True:
            for zombie in self.zombies.values():
                player = self.get_nearest_player(zombie.position)
                zombie.move(player)

            await asyncio.sleep(0.1)

    async def spawn_zombies(self):
        while True:
            for player in self.players:
                nb_zombie = 5
                spawn_points = [Vec2(math.cos(2*math.pi/nb_zombie*x)*self.spawn_radius, math.sin(2*math.pi/nb_zombie*x)*self.spawn_radius) for x in range(0,nb_zombie+1)]
                for spawn_point in spawn_points:
                    zombie = DefaultZombie(spawn_point+player.position)
                    self.zombies[zombie.id] = zombie

            await asyncio.sleep(3)

    async def check_if_active(self):
        while True:
            active = False
            for player in self.players:
                if player.websocket.open:
                    active=True
                    break

            if not active:
                await self.stop_session()

            await asyncio.sleep(5)

    def get_nearest_player(self, position):
        d = math.inf
        p = None
        for player in self.players:
            dp = player.position.distance_to(position)
            if dp < d:
                d = dp
                p = player

        return p
