from module.base.timer import Timer
from module.logger import logger
from tasks.base.page import  page_daily
from tasks.base.ui import UI
from tasks.freebies.assets.assets_freebies_daily_daily import *
from tasks.freebies.assets.assets_freebies_daily_weekly import  *


class ActivityRewardClaim(UI):
    def handle_daily_reward(self):
        self.device.click_record_clear()
        self.ui_ensure(page_daily)
        self._reward_daily_claim()
        self._reward_weekly_claim()

    def _reward_weekly_claim(self):

        time=Timer(5,10).start()
        for _ in self.loop():
            if time.reached():
                break
            if self.appear_then_click(WEEKlY_BUTTON,interval=1):
                continue
            if self.appear_then_click(WEEKLY_CLAIM,interval=1):
                continue
            if self.appear(WEEKLY_CLAIM_DONE):
                break

    def _reward_daily_claim(self):
        timer = Timer(10,10).start()
        for _ in self.loop():
            if timer.reached():
                logger.info('Daily Reward Claim Ttimeout')
                break
            if self.is_reward_claimed_all():
                logger.info('Daily Reward Claimed All')
                break
            if self.appear_then_click(DAILY_REWARD_DETAIL,interval=0):
                continue
            if self.appear_then_click(DAILY_REWARD,interval=1,similarity=0.95):
                timer.reset()
                continue
    def is_reward_claimed_all(self):
        return self.appear(DAILY_REWARD_CLAIMED_10) and self.appear(DAILY_REWARD_CLAIMED_40) and self.appear(DAILY_REWARD_CLAIMED_80) and self. appear(DAILY_REWARD_CLAIMED_100)

