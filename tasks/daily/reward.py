from module.base.timer import Timer
from module.base.utils import color_bar_percentage, get_color, color_similarity_2d
from tasks.base.page import page_main, page_daily
from tasks.base.ui import UI
from tasks.daily.assets.assets_daily_daily import *
from tasks.daily.assets.assets_daily_weekly import  *
import cv2
import numpy as np

from tasks.daily.utils import daily_utils


class DailyRewardClaim(UI,daily_utils):
    def handle_daily_reward(self):
        self.device.click_record_clear()
        self.ui_ensure(page_main)
        self.ui_goto(page_daily)
        self._reward_daily_claim()
        if self.config.DailyReward_Weekly:
            self._reward_weekly_claim()
        self.ui_goto_main()
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
        timer = Timer(20,30).start()
        for _ in self.loop():
            if timer.reached():
                break
            res=DAILY_REWARD_HAVE_CLAIMED.match_multi_template(self.device.image)
            if res and len(res)==4:
                break
            if self.appear_then_click(DAILY_REWARD_DETAIL,interval=1):
                continue
            if self.appear_then_click(DAILY_REWARD,interval=0):
                continue




