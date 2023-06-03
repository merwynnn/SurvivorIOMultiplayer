import math

import pygame as pg
from pygame.math import Vector2 as Vec2
import numpy as np

from Abilities.WeaponsAbilities import KnivesAbility


class Player:
    def __init__(self, username):
        self.win = None

        self.id = None
        self.username = username

        self.position = Vec2((0, 0))
        self.speed = 0.3

        self.health = 1000
        self.max_health = 1000

        self.sprite = None
        self.rect = None

        self.scale = 0.1

        self.abilities = [KnivesAbility(self)]

    def on_start(self):
        self.sprite = pg.image.load("Assets/player-sprite.png").convert_alpha()

    def frame(self, mouse_pos, events, dt):
        keys = pg.key.get_pressed()
        up = keys[pg.K_z] or keys[pg.K_UP]
        down = keys[pg.K_s] or keys[pg.K_DOWN]
        left = keys[pg.K_q] or keys[pg.K_LEFT]
        right = keys[pg.K_d] or keys[pg.K_RIGHT]

        move = pg.math.Vector2(right - left, down - up)
        if move.length_squared() > 0:
            move.scale_to_length(self.speed * dt)
            self.position += move


        # self.angle = -(math.atan2(mouse_pos[1]-self.win.get_height()/2,mouse_pos[0]-self.win.get_width()/2) * 180/math.pi + 90)

    def draw(self, delta):
        # img = pg.transform.rotozoom(self.sprite, self.angle, self.scale)
        sprite = pg.transform.scale(self.sprite,
                                    (self.sprite.get_width() * self.scale, self.sprite.get_height() * self.scale))
        rect = sprite.get_rect(center=self.position + delta)
        self.win.blit(sprite, rect)

        health_bar_length = 70
        health_bar_height = 7

        health_bar_width = int(self.health / self.max_health * health_bar_length)

        pos = (rect.midtop[0]-health_bar_length//2, rect.midtop[1]-health_bar_height-10)

        # Draw the red background of the health bar
        pg.draw.rect(self.win, (0, 0, 0), (pos[0], pos[1], health_bar_length, health_bar_height))

        # Draw the green foreground of the health bar
        pg.draw.rect(self.win, (0, 255, 0), (pos[0], pos[1], health_bar_width, health_bar_height))

        for ability in self.abilities:
            ability.draw(delta)
