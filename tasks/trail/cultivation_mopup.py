from module.base.timer import Timer
from module.exception import GameStuckError
from module.logger import logger
from module.ocr.ocr import Digit
from tasks.base.page import page_main
from tasks.base.task_tab.draglist import TASK_TAB_LIST
from tasks.base.task_tab.task_keyword import TrailKeyword
from tasks.base.ui import UI
from tasks.trail.assets.assets_trail import *
from tasks.trail.assets.assets_trail_cultivation import *


class CultivationMopUp(UI):
    def handle_cultivation_mop_up(self):
        self.device.click_record_clear()
        self.ui_ensure(page_main)
        if not TASK_TAB_LIST.search_rows(main=self,keyword=TrailKeyword):
            raise GameStuckError(' Trail Not Found')
        self._enter_cultivation()
        flag=self._cultivation_mop_up()
        if self.config.CultivationRoad_ClearRedDot and flag=='MOP_UP_SUCCESS':
            self._red_dot_clear()
        self._cultivation_exit()
        return flag
    def _enter_cultivation(self):
        time = Timer(10, count=10).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError("Survival Trial Stucked")
            if self.appear(TRAIL_CULTIVATION_CHECK):
                self.device.click(TRAIL_CULTIVATION_CHECK)
                continue
            if self.appear(CULTIVATION_PAGE_CHECK):
                break

        logger.info(f"survival trial entered")

    def _cultivation_mop_up(self):
        for _ in self.loop():
            if self.appear(CULTIVATION_MOP_UP_REWARD_CLAIM):
                self.device.click(CULTIVATION_MOP_UP_REWARD_CLAIM)
                continue
            if self.appear(CULTIVATION_MOP_UP_SUCCESS):
                self.device.click(CULTIVATION_MOP_UP_SUCCESS)
                continue
            if self.appear(CULTIVATION_CLAIM_CHAO_YING):
                self.device.click(CULTIVATION_CLAIM_CHAO_YING)
                continue
            if self.appear(CULTIVATION_MOP_UP_DONE) :
                ocr=Digit(CULTIVATION_MOP_UP_RESET_TIMES,lang='cn')
                times=ocr.ocr_single_line(self.device.image)
                if times==1:
                    return self._cultivation_reset()
                elif times==0:
                    return 'MOP_UP_SUCCESS'
            if self.appear(CULTIVATION_RESET_MOP_UP_RUNNING):
                break

    def _cultivation_reset(self):
        for _ in self.loop():
            ocr=Digit(CULTIVATION_MOP_UP_RESET_TIMES,lang='cn')
            times=ocr.ocr_single_line(self.device.image)
            if self.appear(CULTIVATION_RESET_MOP_UP_RUNNING):
                return 'MOP_UP_RUNNING'

            if self.appear_then_click(CULTIVATION_RESET_MOP_UP):
                continue
            if self.appear_then_click(CULTIVATION_RESET_CONFIRM):
                continue
            if times==1:
                self.appear_then_click(CULTIVATION_RESET_BUTTON)


        return True

    def _cultivation_exit(self):
        time=Timer(10, count=10).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError("Cultivation exit Stucked")
            if self.ui_page_appear(page_main):
                break
            if self.appear(CULTIVATION_BOX_CHECK):
                self.device.click(CULTIVATION_EXIT)
                continue
            if self.appear(CULTIVATION_MOP_UP_RUNNING_EXIT):
                self.device.click(CULTIVATION_MOP_UP_RUNNING_EXIT)
                continue
            if self.appear(CULTIVATION_EXIT):
                self.device.click(CULTIVATION_EXIT)
                continue


    def _red_dot_clear(self):
        for _ in self.loop():
            if self.appear(CULTIVATION_BOX_CHECK):
                break
            if self.appear(CULTIVATION_BOX):
                self.device.click(CULTIVATION_BOX)
                continue

