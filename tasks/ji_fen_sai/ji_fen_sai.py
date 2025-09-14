from tasks.base.ui import UI


class JiFenSai(UI):
    def run(self):
        if self.config.stored.JiFenSaiDailyRewardClaim.is_expired():
            self.config.stored.JiFenSaiDailyRewardClaim.clear()
        if self.config.JiFenSai_DailyRewardClaim:
            if not self.config.stored.JiFenSaiDailyRewardClaim.is_full():
                from tasks.ji_fen_sai.claim import JiFenSaiClaim
                if not JiFenSaiClaim(config=self.config,device=self.device).handle_ji_fen_sai_claim():
                    return False
                self.config.stored.JiFenSaiDailyRewardClaim.add(1)
        self.config.task_delay(server_update=True)
        self.config.task_stop()

