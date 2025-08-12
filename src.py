from module.alas import AzurLaneAutoScript
from module.logger import logger


class StarRailCopilot(AzurLaneAutoScript):
    def restart(self):
        from tasks.login.login import Login
        Login(self.config, device=self.device).app_restart()

    def start(self):
        from tasks.login.login import Login
        Login(self.config, device=self.device).app_start()

    def stop(self):
        from tasks.login.login import Login
        Login(self.config, device=self.device).app_stop()

    def goto_main(self):
        from tasks.login.login import Login
        from tasks.base.ui import UI
        if self.device.app_is_running():
            logger.info('App is already running, goto main page')
            UI(self.config, device=self.device).ui_goto_main()
        else:
            logger.info('App is not running, start app and goto main page')
            Login(self.config, device=self.device).app_start()
            UI(self.config, device=self.device).ui_goto_main()

    def error_postprocess(self):
        # Exit cloud game to reduce extra fee
        if self.config.is_cloud_game:
            from tasks.login.login import Login
            Login(self.config, device=self.device).app_stop()


    def data_update(self):
        from tasks.item.data_update import DataUpdate
        DataUpdate(config=self.config, device=self.device).run()

    def freebies(self):
        from tasks.freebies.freebies import Freebies
        Freebies(config=self.config, device=self.device).run()

    def organization(self):
        from tasks.organization.organization import Organization
        Organization(config=self.config, device=self.device).run()
    def daily_reward(self):
        from tasks.daily.daily import Daily_Reward
        Daily_Reward(config=self.config, device=self.device).run()
    def squad_raid(self):
        from tasks.squadraid.squadraid import SquadRaid
        SquadRaid(config=self.config, device=self.device).run()
    def zhao_cai(self):
        from tasks.zhaocai.zhaocai import ZhaoCai
        ZhaoCai(config=self.config, device=self.device).run()
    def feng_rao(self):
        from tasks.fengrao.fengrao import FengRao
        FengRao(config=self.config, device=self.device).run()
    def mission(self):
        from tasks.mission.mission import Mission
        Mission(config=self.config,device=self.device).run()
    def survival_trail(self):
        from tasks.trail.survival import Survival
        Survival(config=self.config, device=self.device).run()
    def cultivation_road(self):
        from tasks.trail.cultivation import CultivationRoad
        CultivationRoad(config=self.config, device=self.device).run()
    def ti_li(self):
        from tasks.tili.tili import TiLi
        TiLi(config=self.config, device=self.device).run()
    def akatsuki(self):
        from tasks.organization.akatsuki import Akatsuki
        Akatsuki(config=self.config, device=self.device).run()
    def duel(self):
        from tasks.duel.duel import Duel
        Duel(config=self.config, device=self.device).run()




if __name__ == '__main__':
    src = StarRailCopilot('src')
    src.loop()
