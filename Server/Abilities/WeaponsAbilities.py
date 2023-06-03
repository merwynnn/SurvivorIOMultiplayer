import asyncio
from contextlib import suppress
from Weapons import *

class WeaponAbility:
    def __init__(self, player):
        self.player = player

        self.main_task = None

    def game_loop(self):
        pass

    def get_ability_info(self):
        pass

    def stop_main_task(self):
        if self.main_task:
            self.main_task.cancel()
            with suppress(asyncio.CancelledError):
                await self.main_task

    def start_main_task(self, func):
        self.main_task = asyncio.ensure_future(func())


class KnivesAbility(WeaponAbility):
    def __init__(self, player):
        super().__init__(player)

        self.knives = []

    def game_loop(self):
        knives = copy.copy(self.knives)
        for knife in knives:
            knife.game_loop()

    def get_ability_info(self):
        knives = []
        for knife in self.knives:
            knives.append(f"{knife.id}#{knife.position[0]}#{knife.position[1]}#{knife.dir[0]}#{knife.dir[1]}")

        return f"KnivesAbility%{'%'.join(knives)}"

    async def spawn_knife(self):
        player = self.player.session.get_nearest_player(self.player.position)
        pos_delta = self.player.position.move_towards(player.position, 1)
        dir = pos_delta-self.player.position
        dir.normalize()
        knife = Knife(self, self.player.position+dir*2, dir, 1)
        self.knives.append(knife)

    def del_knife(self, knife):
        self.knives.remove(knife)
        del knife

