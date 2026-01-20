from tasks.base.ui import UI


class JiFenSai(UI):
    def run(self):
       
     
        from tasks.ji_fen_sai.claim import JiFenSaiClaim
        JiFenSaiClaim(config=self.config,device=self.device).run()
        from tasks.ji_fen_sai.fight import JiFenSaiFight
        JiFenSaiFight(config=self.config,device=self.device).run()


        self.config.task_delay(server_update=True)
        self.config.task_stop()

