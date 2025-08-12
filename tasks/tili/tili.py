from module.base.base import ModuleBase
from module.logger import logger


class TiLi(ModuleBase):
    def run(self):
        if self.config.TiLi_DungeonFirst:
            if not self.check_elite_dungeon_completed_today():
                from tasks.tili.dungeon import Dungeon
                res=Dungeon(self.config, self.device).handle_dungeon()
                if res:
                    self.mark_elite_dungeon_completed()
            else:
                logger.info('精英副本今日已完成，跳过')

        from tasks.tili.equipment import Equipment
        Equipment(self.config, self.device).handle_equipment()
        self.config.task_delay(minute=360)
        self.config.task_stop()
    def check_elite_dungeon_completed_today(self):
        """检查精英副本是否今日已完成"""
        if self.config.stored.Dungeon.is_expired():
            logger.info(' dungeon status expired, resetting to incomplete')
            self.config.stored.Dungeon.clear()
            return False

        completed = self.config.stored.Dungeon.is_full()
        logger.attr(' dungeon completed today', completed)
        return completed
    def mark_elite_dungeon_completed(self):
        """标记精英副本为已完成"""
        logger.info('Marking elite dungeon as completed')
        self.config.stored.Dungeon.add(1)