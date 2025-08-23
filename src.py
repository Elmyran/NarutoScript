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

    def leader_board(self):
        from tasks.leaderboard.leaderboard import LeaderBoard
        LeaderBoard(config=self.config, device=self.device).run()
    def information_club(self):
        from tasks.information_club.information_club import InformationClub
        InformationClub(config=self.config, device=self.device).run()
    def monthly_sign_in(self):
        from tasks.activity.monthly_sign_in.monthly_sign_in import MonthlySignIn
        MonthlySignIn(config=self.config, device=self.device).run()
    def yi_le_la_mian(self):
        from  tasks.activity.yi_le_la_mian.yi_le_la_mian import YiLeLaMian
        YiLeLaMian(config=self.config, device=self.device).run()
    def recruit(self):
        from tasks.recruit.recruit import Recruit
        Recruit(config=self.config, device=self.device).run()
    def battle_order(self):
        from tasks.battle_order.battle_order import BattleOrder
        BattleOrder(config=self.config, device=self.device).run()
    def ding_ci_kao_rou(self):
        from tasks.activity.ding_ci_kao_rou.ding_ci_kao_rou import DingCiKaoRou
        DingCiKaoRou(config=self.config, device=self.device).handle_ding_ci_kao_rou()
    def mi_jing(self):
        from tasks.ren_zhe_tiao_zhan.ren_zhe_tiao_zhan import RenZheTiaoZhan
        RenZheTiaoZhan(config=self.config, device=self.device).run()



if __name__ == '__main__':
    src = StarRailCopilot('src')
    src.loop()
