from module.base.timer import Timer
from module.logger import logger
from tasks.base.page import page_recruit
from tasks.base.ui import UI
from tasks.recruit.assets.assets_recruit import *
from tasks.recruit.keywords import AdvancedRecruitment, NormalRecruitment
from tasks.recruit.draglist import RecruitDuration, RecruitTabList


class Recruit(UI):
    def run(self):
        premium_delay_time=self.handle_premium_recruit()
        if self.config.Recruit_SkipNormalRecruit:
            self.config.task_delay(target=premium_delay_time)
        else:    
            normal_delay_time=self.handle_normal_recruit()
            self.config.task_delay(target=[premium_delay_time, normal_delay_time])
        self.config.task_stop()
    def handle_premium_recruit(self):
        logger.hr("高级招募",level=1)
        premium_delay_time = self._premium_recruit()
        return premium_delay_time
    def handle_normal_recruit(self):
        logger.hr("普通招募",level=1)
        normal_delay_time=self._normal_recruit()
        return normal_delay_time
    def _premium_recruit(self):
        self.ui_ensure(page_recruit)
        RecruitTabList.search_rows(main=self, keyword=AdvancedRecruitment)
        self.wait_until_stable(PREMIUM_RECRUIT_FREE_DONE,timer=Timer(2,5),timeout=Timer(3, count=10))
        if self.appear(PREMIUM_RECRUIT_FREE_BUTTON):
            self.ui_click(click_button=PREMIUM_RECRUIT_FREE_BUTTON,check_button=RECRUIT_FREE_CONFIRM,direct_match=True)
            self.ui_click(click_button=RECRUIT_FREE_CONFIRM,check_button=PREMIUM_RECRUIT_FREE_DONE)
        ocr = RecruitDuration(PREMIUM_RECRUIT_REMAIN_TIMES)
        if self.appear(PREMIUM_RECRUIT_100_BUTTON):
            ocr = RecruitDuration(PREMIUM_RECRUIT_REMAIN_TIMES_100_BUTTON_STATUS)
        res = ocr.ocr_single_line(self.device.image)
        if res and res!="0:00:00":
            return res
        return None

    def _normal_recruit(self):
        self.ui_ensure(page_recruit)
        RecruitTabList.search_rows(main=self, keyword=NormalRecruitment)
        self.wait_until_stable(NORMAL_RECRUIT_FREE_DONE,timer=Timer(2,5),timeout=Timer(3, count=10))
        if self.appear(NORMAL_RECRUIT_FREE_BUTTON):
            self.ui_click(click_button=NORMAL_RECRUIT_FREE_BUTTON,check_button=RECRUIT_FREE_CONFIRM,direct_match=True)
            self.ui_click(click_button=RECRUIT_FREE_CONFIRM,check_button=NORMAL_RECRUIT_FREE_DONE)
        ocr = RecruitDuration(NORMAL_RECRUIT_REMAIN_TIMES)
        res = ocr.ocr_single_line(self.device.image)
        if res and res!="0:00:00":
            return res
        else:
            return None
