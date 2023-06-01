import random
import string


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
                await player.websocket.send("OnNewPlayerJoin" + "," + str(new_player.id) + "," + str(new_player.username))
                await new_player.websocket.send(
                    "OnNewPlayerJoin" + "," + str(player.id) + "," + str(player.username))
            self.players.append(new_player)
            if len(self.players) == self.max_players:
                self.full = True

            return True
        else:
            return False

    def on_received_message_from_player(self, player):
        msg = ""
        return msg

    async def start(self):
        for player in self.players:
            await player.websocket.send("StartInfo")
