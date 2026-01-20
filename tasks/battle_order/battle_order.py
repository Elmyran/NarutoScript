from module.logger import logger
from tasks.base.ui import UI

class BattleOrder(UI):
    def run(self):
        

        from tasks.battle_order.rank import BattleOrderRank    
        BattleOrderRank(config=self.config, device=self.device).run()
        from tasks.battle_order.weekly_task import BattleOrderWeeklyTask
        BattleOrderWeeklyTask(config=self.config, device=self.device).handle_battle_order_weekly_task()
        from  tasks.battle_order.weekly_reward import BattleOrderWeeklyReward
        BattleOrderWeeklyReward(config=self.config, device=self.device).run()
        from  tasks.battle_order.claim import BattleOrderClaim
        BattleOrderClaim(config=self.config, device=self.device).handle_battle_order_claim()
        self.config.task_delay(server_update=True)
        self.config.task_stop()






