from Client.Abilities.Weapons import Knife

from pygame.math import Vector2 as Vec2


class Weapon:
    def __init__(self, win):
        self.win = win

    def draw(self, delta):
        pass

    def set_ability_info(self, info):
        pass


class KnivesAbility(Weapon):
    def __init__(self, win):
        super().__init__(win)

        self.knives = {}

        self.ability_name = "KnivesAbility"

    def draw(self, delta):
        knives = list(self.knives.values())
        for knife in knives:
            knife.draw(delta)

    def set_ability_info(self, info):
        ability_infos = info.split("#")
        not_checked_knives = list(self.knives.values())

        for knife_info in ability_infos:
            knife_id = knife_info[0]

            knife = self.knives.get(knife_id)

            pos = Vec2((int(knife_info[1]), int(knife_info[2])))
            dir = Vec2((int(knife_info[3]), int(knife_info[4])))

            if not knife:
                knife = Knife(self.win, pos, dir)
                self.knives[knife_id] = knife
            else:
                not_checked_knives.remove(knife)
                knife.position = pos
                knife.dir = dir

        for k in not_checked_knives:
            del self.knives[k.id]
            del k


