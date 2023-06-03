import random
import string
from pygame.math import Vector2 as Vec2


class Session:
    def __init__(self):
        numbers = "0123456789"
        self.id = ''.join(random.sample(string.ascii_letters + numbers, 10))  # Generate a random link
        self.players = []
        self.max_players = 2
        self.full = False

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
        for p in self.players:
            if p != player:
                infos.append(f"{p.id}:{int(p.position[0])}/{int(p.position[1])}")
        return ",".join(infos)

    async def start(self):
        for player in self.players:
            await player.websocket.send("StartInfo")