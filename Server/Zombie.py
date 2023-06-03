import string
import random


class Zombie:
    def __init__(self, pos, speed, strength):
        self.class_name = "Zombie"

        numbers = "0123456789"
        self.id = ''.join(random.sample(string.ascii_letters + numbers, 10))  # Generate a random link

        self.position = pos
        self.speed = speed
        self.strength = strength

    def move(self, player):
        self.position.move_towards_ip(player.position, self.speed)

class DefaultZombie(Zombie):
    def __init__(self, pos):
        super().__init__(pos, 0.5, 5)
        self.class_name = "DefaultZombie"

