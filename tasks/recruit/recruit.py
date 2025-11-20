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
        logger.hr("Premium Recruit)",level=1)
        premium_delay_time = self._premium_recruit()
        return premium_delay_time
    def handle_normal_recruit(self):
        logger.hr("Normal Recruit)",level=1)
        normal_delay_time=self._normal_recruit()
        return normal_delay_time
    def _premium_recruit(self):
        self.ui_ensure(page_recruit)
        RecruitTabList.search_rows(main=self, keyword=AdvancedRecruitment)
        self.wait_until_stable(PREMIUM_RECRUIT_FREE_BUTTON,timeout=Timer(1, count=3))
        wait_recruit_end=True
        for _ in self.loop():
            if wait_recruit_end and self.appear(PREMIUM_RECRUIT_FREE_DONE,similarity=0.7):
                break
            RECRUIT_FREE_CONFIRM.load_search(FREE_BUTTON_CONFIRM_AREA.area)
            if self.appear_then_click(RECRUIT_FREE_CONFIRM,similarity=0.7, interval=1):
                wait_recruit_end=True
                continue
            if self.appear_then_click(PREMIUM_RECRUIT_FREE_BUTTON, interval=1):
                wait_recruit_end=False
                continue
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
        self.wait_until_stable(NORMAL_RECRUIT_FREE_BUTTON,timeout=Timer(1, count=3))
        wait_recruit_end=True
        for _ in self.loop():
            if wait_recruit_end and self.appear(NORMAL_RECRUIT_FREE_DONE,similarity=0.7):
                break
            RECRUIT_FREE_CONFIRM.load_search(FREE_BUTTON_CONFIRM_AREA.area)
            if self.appear_then_click(RECRUIT_FREE_CONFIRM,similarity=0.7, interval=1):
                wait_recruit_end=True
                continue
            if self.appear_then_click(NORMAL_RECRUIT_FREE_BUTTON, interval=1):
                wait_recruit_end = False
                continue   
        ocr = RecruitDuration(NORMAL_RECRUIT_REMAIN_TIMES)
        res = ocr.ocr_single_line(self.device.image)
        if res and res!="0:00:00":
            return res
        else:
            return None
