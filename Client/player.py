import math

import pygame as pg
from pygame.math import Vector2 as Vec2
import numpy as np

class Player:
    def __init__(self, win, username):
        self.win = win

        self.id = None
        self.username = username

        self.position = Vec2((0, 0))
        self.speed = 1

        self.sprite = pg.image.load("robot.png").convert_alpha()
        self.rect = None

        self.scale = 0.5
        self.angle = 0

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

        self.angle = -(math.atan2(mouse_pos[1]-self.win.get_height()/2,mouse_pos[0]-self.win.get_width()/2) * 180/math.pi + 90)

    def draw(self, delta):
        img = pg.transform.rotozoom(self.sprite, self.angle, self.scale)
        self.rect = img.get_rect(center = self.position+delta)
        self.win.blit(img, self.rect)