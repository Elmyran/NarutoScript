import datetime
from module.base.base import ModuleBase
from module.logger import logger
from module.config.utils import get_server_next_update, nearest_future 
from module.base.timer import future_time  
from datetime import datetime, timedelta  
class Freebies(ModuleBase):
    def run(self):
        """
        Run all freebie tasks
        """
        delay_time = get_server_next_update(self.config.Scheduler_ServerUpdate)
        if self.config.PrivilegeWeeklyPackage_PrivilegeWeeklyPackageClaim:
            logger.hr(" Weekly Package ",level=1)
            from tasks.freebies.weekly_package import WeeklyPackage
            WeeklyPackage(config=self.config,device=self.device).handle_weekly_package()    
        if self.config.Freebies_DailyShareStart:
            logger.hr('Daily Share', level=1)
            from tasks.freebies.dailyshare import DailyShare
            DailyShare(config=self.config, device=self.device).handle_daily_share()
        if self.config.Freebies_FriendGiftsStart:
            logger.hr('Friend Gifts', level=1)
            from tasks.freebies.friendgifts import FriendGifts
            FriendGifts(config=self.config, device=self.device).handle_friend_gifts()
        if self.config.Freebies_YiLeLaMianClaim:
            logger.hr('Yi Le La Mian', level=1)
            from tasks.freebies.yi_le_la_mian import YiLeLaMian
            if not YiLeLaMian(config=self.config, device=self.device).handle_la_mian():
                time = future_time("11:00")  
                delay_time = nearest_future([delay_time, time])
        if self.config.Freebies_InformationClubSignIn:
            logger.hr('Information Club', level=1)
            from tasks.freebies.information_club import InformationClub
            InformationClub(config=self.config, device=self.device).handle_information_club()
        if  self.config.Freebies_MailRewardClaim:
            logger.hr('Mail Reward', level=1)
            from tasks.freebies.mail import MailReward
            MailReward(config=self.config, device=self.device).handle_mail_reward()
        if self.config.ZhaoCai_ZhaoCaiFree:
            logger.hr('Zhao Cai Free', level=1)
            from tasks.freebies.zhaocai import ZhaoCaiFree
            ZhaoCaiFree(config=self.config, device=self.device).handle_zhao_cai()
        if self.config.Freebies_LeaderBoardclaim:
            logger.hr('Leader Board', level=1)
            from tasks.freebies.leaderboard import LeaderBoard
            res=LeaderBoard(config=self.config, device=self.device).run()
            if not res:
                time = future_time("08:00")  
                delay_time = nearest_future([delay_time, time])
        if self.config.Freebies_MonthlySignIn:
            logger.hr('Monthly Sign In', level=1)
            from tasks.freebies.monthly_sign_in import MonthlySignIn
            MonthlySignIn(config=self.config, device=self.device).handle_monthly_sign_in()
        if self.config.Freebies_ActivityReward:
            logger.hr('Daily Reward', level=1)
            from tasks.freebies.activityreward import ActivityRewardClaim
            ActivityRewardClaim(config=self.config, device=self.device).handle_daily_reward()
        
        self.config.task_delay(target=delay_time)
        self.config.task_stop()
