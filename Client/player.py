import math

import pygame as pg
from pygame.math import Vector2 as Vec2
import numpy as np

class Player:
    def __init__(self, username):
        self.win = None

        self.id = None
        self.username = username

        self.position = Vec2((0, 0))
        self.speed = 1.5

        self.sprite = None
        self.rect = None

        self.scale = 0.1

    def on_start(self):
        self.sprite = pg.image.load("Assets/player-sprite.png").convert_alpha()

    def frame(self, mouse_pos, events):
        keys = pg.key.get_pressed()
        if keys[pg.K_z]:
            self.position[1] -= self.speed
        if keys[pg.K_s]:
            self.position[1] += self.speed
        if keys[pg.K_q]:
            self.position[0] -= self.speed
        if keys[pg.K_d]:
            self.position[0] += self.speed

        #self.angle = -(math.atan2(mouse_pos[1]-self.win.get_height()/2,mouse_pos[0]-self.win.get_width()/2) * 180/math.pi + 90)

    def draw(self, delta):
        #img = pg.transform.rotozoom(self.sprite, self.angle, self.scale)
        sprite = pg.transform.scale(self.sprite, (self.sprite.get_width()*self.scale, self.sprite.get_height()*self.scale))
        rect = sprite.get_rect(center = self.position+delta)
        self.win.blit(sprite, rect)