from module.logger import logger
from tasks.base.ui import UI
from tasks.battle_order.rank import BattleOrderRank
class BattleOrder(UI):
    def run(self):
        if self.config.BattleOrder_LikeAndShare:
            if self.config.stored.BattleOrderRank.is_expired():
                self.config.stored.BattleOrderRank.clear()
            if not self.config.stored.BattleOrderRank.is_full():
                BattleOrderRank(config=self.config, device=self.device).handle_battle_order_rank()
                self.config.stored.BattleOrderRank.add()
            else:
                logger.info('BattleOrderRank 本周已完成，跳过')
        from tasks.battle_order.weekly_task import BattleOrderWeeklyTask
        BattleOrderWeeklyTask(config=self.config, device=self.device).handle_battle_order_weekly_task()
        from  tasks.battle_order.weekly_reward import BattleOrderWeeklyReward
        BattleOrderWeeklyReward(config=self.config, device=self.device).handle_battle_order_weekly_reward()
        from  tasks.battle_order.claim import BattleOrderClaim
        BattleOrderClaim(config=self.config, device=self.device).handle_battle_order_claim()
        self.config.task_call('TiLi')
        self.config.task_delay(server_update=True)
        self.config.task_stop()






