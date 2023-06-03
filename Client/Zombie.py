import pygame as pg


class Zombie:
    def __init__(self, win, id, pos):
        self.class_name = "Zombie"

        self.win = win
        self.id = id

        self.position = pos
        self.scale = 0.1

    def draw(self, delta):
        pass


class DefaultZombie(Zombie):
    def __init__(self, win, id, pos):
        super().__init__(win, id, pos)

        self.class_name = "DefaultZombie"
        self.sprite = pg.image.load("Assets/zombie-sprite.png").convert_alpha()

        self.scale = 0.1

    def draw(self, delta):
        sprite = pg.transform.scale(self.sprite,
                                    (self.sprite.get_width() * self.scale, self.sprite.get_height() * self.scale))
        rect = sprite.get_rect(center=self.position + delta)
        self.win.blit(sprite, rect)
