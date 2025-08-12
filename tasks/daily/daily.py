from module.base.base import ModuleBase
from tasks.daily.reward import DailyRewardClaim


class Daily_Reward(ModuleBase):
    def run(self):

        DailyRewardClaim(config=self.config, device=self.device).handle_daily_reward()


        self.config.task_delay(server_update=True)
        self.config.task_stop()
