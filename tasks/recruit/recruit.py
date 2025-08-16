from module.ocr.ocr import Duration
from tasks.base.page import page_recruit
from tasks.base.ui import UI
from tasks.recruit.assets.assets_recruit import *

from tasks.recruit.switch import SWITCH_RECRUIT_TAB, RecruitDuration


class Recruit(UI):
    def run(self):
        self.handle_recruit()
    def handle_recruit(self):
        premium_delay_time = self._premium_recruit()
        if not self.config.Recruit_SkipNormalRecruit:
            normal_delay_time=self._normal_recruit()
            self.config.task_delay(target=[premium_delay_time, normal_delay_time])
        else:
            self.config.task_delay(target=premium_delay_time)
        self.ui_goto_main()
        self.config.task_stop()
    def _premium_recruit(self):
        self.ui_ensure(page_recruit)
        SWITCH_RECRUIT_TAB.set('高级招募', main=self)
        for _ in self.loop():
            if self.appear(PREMIUM_RECRUIT_FREE_DONE):
                break
            RECRUIT_FREE_CONFIRM.load_search(FREE_BUTTON_CONFIRM_AREA.area)
            if self.appear_then_click(RECRUIT_FREE_CONFIRM, interval=1):
                continue
            if self.appear_then_click(PREMIUM_RECRUIT_FREE_BUTTON, interval=1):
                continue
        ocr = RecruitDuration(PREMIUM_RECRUIT_REMAIN_TIMES)
        res = ocr.ocr_single_line(self.device.image)
        if res and res!="0:00:00":
            return res
        return None

    def _normal_recruit(self):
        self.ui_ensure(page_recruit)
        SWITCH_RECRUIT_TAB.set('普通招募', main=self)
        for _ in self.loop():
            if self.appear(NORMAL_RECRUIT_FREE_DONE, interval=1):
                break
            RECRUIT_FREE_CONFIRM.load_search(FREE_BUTTON_CONFIRM_AREA.area)
            if self.appear_then_click(RECRUIT_FREE_CONFIRM, interval=1):
                continue
            if self.appear_then_click(NORMAL_RECRUIT_FREE_BUTTON, interval=1):
                continue
        ocr = RecruitDuration(NORMAL_RECRUIT_REMAIN_TIMES)
        res = ocr.ocr_single_line(self.device.image)
        if res and res!="0:00:00":
            return res
        else:

            return None


