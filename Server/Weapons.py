import copy
import random
import string


class Knife:
    def __init__(self, knife_ability, pos, dir, speed):
        numbers = "0123456789"
        self.id = ''.join(random.sample(string.ascii_letters + numbers, 10))  # Generate a random link

        self.ability = knife_ability

        self.o_pos = copy.copy(pos)
        self.position = pos
        self.dir = dir

        self.speed = speed

    def game_loop(self):
        self.position += self.dir*self.speed
        if self.position.distance_to(self.o_pos) > 2000:
            self.ability.del_knife(self)
