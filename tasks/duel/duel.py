
from tasks.base.ui import UI


class Duel(UI):
    def run(self):
        if self.config.stored.DuelDaily.is_expired():
            self.config.stored.DuelDaily.clear()
        if not self.config.stored.DuelDaily.is_full():
            from tasks.duel.duel_daily import DuelDaily
            if DuelDaily(config=self.config, device=self.device).handle_duel_daily()=='Delay 5 Minute':
                self.config.task_delay(minute=5)
                return
            self.config.stored.DuelDaily.add()
        current_victory_count=self.config.Duel_CurrentVictoryCount
        target_victory_count=self.config.Duel_TargetVictoryNumber
        if self.config.Duel_DuelWeeklyStatus and current_victory_count < target_victory_count:
            self.config.get_next_task()
            if len(self.config.pending_task) == 1 :
                from tasks.duel.duel_weekly import DuelWeekly
                DuelWeekly(config=self.config, device=self.device).handle_duel_weekly()
                self.config.task_delay(server_update=True)
                self.config.task_stop()
            else:
                self.config.task_delay(minute=10)
        else:
            self.config.task_delay(server_update=True)
            self.config.task_stop()







