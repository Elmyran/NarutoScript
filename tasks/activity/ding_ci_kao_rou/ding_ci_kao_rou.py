from module.base.timer import Timer
from module.logger import logger
from module.ocr.ocr import Digit
from tasks.activity.assets.assets_activity_ding_ci_kao_rou import *
from tasks.activity.draglist import ACTIVITY_TAB_LIST
from tasks.activity.keyword import DingCiKaoRouKeyword

from tasks.base.page import page_activity
from tasks.base.ui import UI


class DingCiKaoRou(UI):
    def handle_ding_ci_kao_rou(self):
        self.device.click_record_clear()
        self.ui_ensure(page_activity)
        ACTIVITY_TAB_LIST.search_rows(main=self,keyword=DingCiKaoRouKeyword)
        self._handle_kao_rou()
        self._handle_reward_claim()
        self.ui_goto_main()
        self.config.task_delay(server_update=True)
        self.config.task_stop()

    def _handle_kao_rou(self):
        ocr=Digit(BEEF_1)
        for _ in self.loop():
            if self.appear(BEEF_CONFIRM):
                res=ocr.ocr_single_line(self.device.image)
                if res!=0:
                    self.device.swipe([513,511],[764,439])
                else:
                    break

        ocr=Digit(BEEF_2)
        for _ in self.loop():
            if self.appear(BEEF_CONFIRM):
                res=ocr.ocr_single_line(self.device.image)
                if res!=0:
                    self.device.swipe([767,547],[764,439])
                else:
                    break
        ocr=Digit(BEEF_3)
        for _ in self.loop():
            if self.appear(BEEF_CONFIRM):
                logger.info(BEEF_3.area)
                res=ocr.ocr_single_line(self.device.image)
                if res!=0:
                    self.device.swipe([1043,520],[764,439])
                else:
                    break
    def _handle_reward_claim(self):
        time=Timer(3,count=5).start()
        for _ in self.loop():
            if time.reached():
                return
            if self.appear_then_click(DING_CI_REWARD_RED_DOT,interval=0):
                break
        for _ in self.loop():
            if self.appear(DING_CI_REWARD_CLAIM_SUCCESS):
                break
            DING_CI_REWARD_CLAIM_BUTTON.load_search(DING_CI_REWARD_AREA.area)
            if self.appear_then_click(DING_CI_REWARD_CLAIM_BUTTON,interval=1):
                continue







