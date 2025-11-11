from module.base.timer import Timer
from module.ocr.ocr import Digit, DigitCounter
from tasks.base.page import  page_daily
from tasks.base.ui import UI
from tasks.freebies.assets.assets_freebies_daily_daily import *
from tasks.freebies.assets.assets_freebies_daily_weekly import  *


class ActivityRewardClaim(UI):
    progress=0
    def run(self):
        self.device.click_record_clear()
        self.handle_daily_reward()
        self.handle_weekly_reward()
    def handle_daily_reward(self):
        if self.config.stored.ActivityProgressTodayCount.is_expired():
            self.config.stored.ActivityProgressTodayCount.clear()
        if self.config.stored.ActivityProgressTodayCount.is_full():
            return True
        self.ui_ensure(page_daily)
        self.daily_progress_recognition()
        self._reward_daily_claim()
        self.config.stored.ActivityProgressTodayCount.add()
        
    def handle_weekly_reward(self):
        if not self.config.stored.ActivityProgressWeekly.is_full():
            return True
        if self.config.stored.ActivityProgressWeeklyCount.is_expired():
            self.config.stored.ActivityProgressWeeklyCount.clear()
        if self.config.stored.ActivityProgressWeeklyCount.is_full():
            return True
        self.ui_ensure(page_daily)
        if self._reward_weekly_claim():
            self.config.stored.ActivityProgressWeeklyCount.add()
        
    def daily_progress_recognition(self):
        # Daily Progress
        ocr=Digit(DAILY_PROGRESS)
        progress=ocr.ocr_single_line(self.device.image)
        self.config.stored.ActivityProgressToday.set(progress)
        # Weekly Progress
        ocr=DigitCounter(WEEKLY_ACTIVITY_PROGRESS)
        progress,_,_=ocr.ocr_single_line(self.device.image)
        self.config.stored.ActivityProgressWeekly.set(progress)

    def _reward_daily_claim(self):
        check_buttons=[DAILY_REWARD_CLAIMED_10,DAILY_REWARD_CLAIMED_40,DAILY_REWARD_CLAIMED_80,DAILY_REWARD_CLAIMED_100]
        progress=[10,40,80,100]
        click_timer=Timer(1)
        for _ in self.loop():
            if self.is_reward_claimed_all():
                break
            self._get_claim_progress(check_buttons,progress)
            if self.progress==progress[3]:
                break
            if click_timer.reached():
                claimable=self._get_claimable_buttons(check_buttons,progress)
                if claimable:
                        self.device.click(claimable[0])
                        click_timer.reset()
                else:
                    return False
        return True

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

        
        
        
    def is_reward_claimed_all(self):
        return self.appear(DAILY_REWARD_CLAIMED_10) and self.appear(DAILY_REWARD_CLAIMED_40) and self.appear(DAILY_REWARD_CLAIMED_80) and self. appear(DAILY_REWARD_CLAIMED_100)


    def _get_claim_progress(self,checked_buttons,thresholds) -> int:
        current_progress = 0  

        for i in range(len(thresholds) - 1, -1, -1):
            if self.appear(checked_buttons[i]):  
                current_progress = thresholds[i]
                break  
        if current_progress>self.progress:
            self.progress=current_progress
    def _get_claimable_buttons(self,check_buttons,progress) -> list:
        claimable = []  
        for i, threshold in enumerate(progress):  
            if (self.progress < threshold <= self.config.stored.ActivityProgressToday.value):  
                claimable.append(check_buttons[i])
        return claimable



