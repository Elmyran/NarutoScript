from module.logger import logger
from tasks.base.ui import UI

from tasks.battle_order.rank import BattleOrderRank
class BattleOrder(UI):
    def run(self):
        if self.config.BattleOrder_LikeAndShare:
            if not self.check_completed():
                BattleOrderRank(config=self.config, device=self.device).handle_battle_order_rank()
                self.config.stored.Dungeon.add(1)
            else:
                logger.info('BattleOrderRank 本周已完成，跳过')
        self.config.task_delay(server_update=True)
        self.config.task_stop()

    def check_completed(self):
        """检查精英副本是否今日已完成"""
        if self.config.stored.BattleOrderRank.is_expired():
            logger.info(' BattleOrderRank  status expired, resetting to incomplete')
            self.config.stored.BattleOrderRank.clear()
            return False

        completed = self.config.stored.BattleOrderRank.is_full()
        logger.attr(' BattleOrderRank completed today', completed)
        return completed




