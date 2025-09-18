import datetime
from module.base.base import ModuleBase
from module.logger import logger
from tasks.freebies.dailyshare import DailyShare
from tasks.freebies.friendgifts import FriendGifts

from tasks.freebies.mail import MailReward
from tasks.freebies.weekly_package import WeeklyPackage
from module.config.utils import get_server_next_update, nearest_future 
from module.base.timer import future_time  
from datetime import datetime, timedelta  
class Freebies(ModuleBase):
    def run(self):
        """
        Run all freebie tasks
        """
        delay_time = get_server_next_update(self.config.Scheduler_ServerUpdate)
        if self.config.WeeklyFreebies_WeeklyPackage:
            logger.hr(" Weekly Package ",level=1)
            if self.config.stored.WeeklyPackage.is_expired():
                self.config.stored.WeeklyPackage.clear()
            if not self.config.stored.WeeklyPackage.is_full():
                WeeklyPackage(config=self.config,device=self.device).handle_weekly_package()
                self.config.stored.WeeklyPackage.add(1)
        if self.config.DailyFreebies_DailyShare:
            logger.hr('Daily Share', level=1)
            DailyShare(config=self.config, device=self.device).handle_daily_share()
        if self.config.DailyFreebies_FriendGifts:
            logger.hr('Friend Gifts', level=1)
            FriendGifts(config=self.config, device=self.device).handle_friend_gifts()
        # To actually get RedemptionCode rewards, you need to receive the mail
        if  self.config.DailyFreebies_MailReward:
            logger.hr('Mail Reward', level=1)
            MailReward(config=self.config, device=self.device).handle_mail_reward()
        if self.config.ZhaoCai_ZhaoCaiFree:
            logger.hr('Zhao Cai Free', level=1)
            from tasks.freebies.zhaocai import ZhaoCaiFree
            ZhaoCaiFree(config=self.config, device=self.device).handle_zhao_cai()
        if self.config.InformationClub_SignIn:
            logger.hr('Information Club', level=1)
            from tasks.freebies.information_club import InformationClub
            InformationClub(config=self.config, device=self.device).handle_information_club()
        if self.config.LeaderBoard_claim:
            logger.hr('Leader Board', level=1)
            from tasks.freebies.leaderboard import LeaderBoard
            if not LeaderBoard(config=self.config, device=self.device).handle_leader_board():
                five_minutes_later = datetime.now() + timedelta(minutes=5)
                delay_time = nearest_future([delay_time, five_minutes_later])
        if self.config.MonthlySignIn_SignIn:
            logger.hr('Monthly Sign In', level=1)
            from tasks.freebies.monthly_sign_in import MonthlySignIn
            MonthlySignIn(config=self.config, device=self.device).handle_monthly_sign_in()
        if self.config.YiLeLaMian_Claim:
            logger.hr('Yi Le La Mian', level=1)
            from tasks.freebies.yi_le_la_mian import YiLeLaMian
            if not YiLeLaMian(config=self.config, device=self.device).handle_la_mian():
                time = future_time("11:00")  
                delay_time = nearest_future([delay_time, time])  
        if self.config.DailyReward_Daily:
            logger.hr('Daily Reward', level=1)
            from tasks.freebies.dailyreward import DailyRewardClaim
            DailyRewardClaim(config=self.config, device=self.device).handle_daily_reward()
        
        self.config.task_delay(target=delay_time)
        self.config.task_call('TiLi')
        self.config.task_stop()
