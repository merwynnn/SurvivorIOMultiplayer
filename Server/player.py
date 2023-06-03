import random
import string
import numpy as np
from pygame.math import Vector2 as Vec2
from Abilities.WeaponsAbilities import KnivesAbility

class Player:
    def __init__(self, username, websocket):
        numbers = "0123456789"
        self.id = ''.join(random.sample(string.ascii_letters + numbers, 10))  # Generate a random link

        self.username = username
        self.session = None
        self.websocket = websocket

        self.position = Vec2((0, 0))

        self.health = 1000
        self.max_health = 1000

        self.abilities = [KnivesAbility(self)]

