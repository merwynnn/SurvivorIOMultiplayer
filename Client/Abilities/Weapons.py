import math

import pygame as pg

class Knife:
    def __init__(self, win, pos, dir):
        self.win = win
        self.position = pos
        self.dir = dir

        self.sprite = pg.image.load("Assets/knife.png").convert_alpha()
        self.sprite = pg.transform.scale(self.sprite,
                                    (self.sprite.get_width() * 0.03, self.sprite.get_height() * 0.03))

        angle = -(math.atan2(self.dir[0],self.dir[1]) * 180 / math.pi + 90)
        self.sprite = pg.transform.rotate(self.sprite, angle)

    def draw(self, delta):
        rect = self.sprite.get_rect(center=self.position + delta)
        self.win.blit(self.sprite, rect)
