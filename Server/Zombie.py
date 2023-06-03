import string
import random
import pygame


class Zombie:
    def __init__(self, pos, speed, strength, health):
        self.class_name = "Zombie"

        numbers = "0123456789"
        self.id = ''.join(random.sample(string.ascii_letters + numbers, 10))  # Generate a random link

        self.position = pos
        self.speed = speed
        self.strength = strength

        self.health = health

        self.size = (960, 960)
        self.scale = 0.1

    def move(self, player):
        self.position.move_towards_ip(player.position, self.speed)

    def collide_with_rect(self, rect):
        rect1 = pygame.Rect(self.position, (self.size[0]*self.scale, self.size[1]*self.scale))

        if rect1.colliderect(rect):
            return True
        return False


class DefaultZombie(Zombie):
    def __init__(self, pos):
        super().__init__(pos, speed=0.3, strength=5, health=50)
        self.class_name = "DefaultZombie"

        self.size = (960, 960)

