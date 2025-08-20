from module.base.base import ModuleBase
from module.logger import logger


class TiLi(ModuleBase):
    def run(self):
        if self.config.TiLi_DungeonFirst:
            if self.config.stored.Dungeon.is_expired():
                self.config.stored.Dungeon.clear()
            if not self.config.stored.Dungeon.is_full():
                from tasks.tili.dungeon import Dungeon
                res=Dungeon(self.config, self.device).handle_dungeon()
                if res:
                    self.config.stored.Dungeon.add()
            else:
                logger.info('精英副本今日已完成，跳过')

        from tasks.tili.equipment import Equipment
        Equipment(self.config, self.device).handle_equipment()
        self.config.task_delay(minute=360)
        self.config.task_stop()
