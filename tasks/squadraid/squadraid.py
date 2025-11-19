from module.base.base import ModuleBase





class SquadRaid(ModuleBase):
    def run(self):
        from tasks.squadraid.fight import SquadRaidFight
        SquadRaidFight(self.config,self.device).run()
        if self.config.SquadRaid_SquadRaidBenefit:
            from tasks.squadraid.benefit import HelpBattleBenefit
            HelpBattleBenefit(self.config,self.device).handle_help_battle_benefit()
        self.config.task_delay(server_update=True)
        self.config.task_stop()
