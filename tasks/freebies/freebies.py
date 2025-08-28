from module.base.base import ModuleBase
from module.logger import logger
from tasks.freebies.dailyshare import DailyShare
from tasks.freebies.friendgifts import FriendGifts

from tasks.freebies.mail import MailReward
from tasks.freebies.weekly_package import WeeklyPackage


class Freebies(ModuleBase):
    def run(self):
        """
        Run all freebie tasks
        """
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

        self.config.task_delay(server_update=True)
        self.config.task_stop()
