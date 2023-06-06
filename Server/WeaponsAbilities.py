import _thread
import asyncio
import time
from contextlib import suppress
from Weapons import *


class WeaponAbility:
    def __init__(self, player):
        self.player = player

        self.main_task_func = None
        self._stop_main_task = False

    def game_loop(self):
        pass

    def get_ability_info(self):
        pass

    def stop_main_task(self):
        self._stop_main_task = True

    def start_main_task(self, func):
        self.main_task_func = func
        self._stop_main_task = False
        _thread.start_new_thread(self.loop, ())

    def loop(self):
        while not self._stop_main_task:
            self.main_task_func()


class KnivesAbility(WeaponAbility):
    def __init__(self, player):
        super().__init__(player)

        self.knives = []

        self.shot_delay = 1

        self.start_main_task(self.spawn_knife)

    def game_loop(self):
        knives = copy.copy(self.knives)
        for knife in knives:
            knife.game_loop()

    def get_ability_info(self):
        knives = []
        for knife in self.knives:
            knives.append(f"{knife.id}#{knife.position[0]}#{knife.position[1]}#{knife.dir[0]}#{knife.dir[1]}")

        return f"KnivesAbility%{'%'.join(knives)}"

    def spawn_knife(self):
        zombie = self.player.game.get_nearest_zombie(self.player.position)
        if zombie:
            pos_delta = self.player.position.move_towards(zombie.position, 1)
            dir = pos_delta - self.player.position
            if dir.length() > 0:

                dir.normalize()
                knife = Knife(self, self.player.position + dir * 2, dir, 5)
                self.knives.append(knife)
        time.sleep(self.shot_delay)

    def del_knife(self, knife):
        self.knives.remove(knife)
        del knife
