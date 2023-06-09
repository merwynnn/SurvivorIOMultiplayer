import random
import string
from pygame.math import Vector2 as Vec2
from WeaponsAbilities import KnivesAbility

class Player:
    def __init__(self, game, username, client_id, websocket):
        numbers = "0123456789"
        self.id = ''.join(random.sample(string.ascii_letters + numbers, 10))  # Generate a random link

        self.username = username
        self.game = game

        self.client_id = client_id
        self.websocket = websocket

        self.position = Vec2((0, 0))

        self.health = 1000
        self.max_health = 1000

        self.abilities = [KnivesAbility(self)]

