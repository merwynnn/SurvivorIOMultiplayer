
class Zombie:
    def __init__(self, win, id, pos):
        self.class_name = "Zombie"

        self.win = win
        self.id = id

        self.pos = pos

    def draw(self, delta):
        pass


class DefaultZombie(Zombie):
    def __init__(self, win, id, pos):
        super().__init__(win, id, pos)

        self.class_name = "DefaultZombie"

    def draw(self, delta):
