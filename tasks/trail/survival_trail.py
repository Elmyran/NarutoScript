from module.base.timer import Timer
from module.exception import GameStuckError
from module.logger import logger
from module.ocr.ocr import Digit
from tasks.base.page import page_survival_trail
from tasks.base.task_tab.draglist import TASK_TAB_LIST
from tasks.base.task_tab.task_keyword import TrailKeyword
from tasks.base.ui import UI
from tasks.trail.assets.assets_trail import *
from tasks.trail.assets.assets_trail_survival import *


class SurvivalTrail(UI):
    def handle_survival_trail (self):
        self.device.click_record_clear()
        self.ui_ensure(page_survival_trail)
        self.handle_teleport()
        self._mop_up()
        self._mop_up_check()
    def handle_teleport(self):
        logger.info('handle teleport')
        for _ in self.loop():
            if self.appear_then_click(SURVIVAL_TELEPORT,interval=0):
                continue
            if self.appear_then_click(SURVIVAL_CHAO_YING_CONFIRM,interval=0):
                continue
            if self.appear(SURVIVAL_CHECK):
                break
            if self.appear(SURVIVAL_HAVE_DONE):
                break

    def _mop_up(self):
        logger.info('start mop up')
        for _ in self.loop():
            if self.appear(SURVIVAL_HAVE_DONE):
                break
            if self.appear(SURVIVAL_MOP_UP_DONE):
                break
            if self.appear(SURVIVAL_MOP_UP_FAILED):
                break
            if self.appear_then_click(SURVIVAL_MOP_UP_CHECKPOINT_VICTORY,interval=1):
                continue
            if self.appear(SURVIVAL_MOP_UP_RUNNING):
                continue
            if self.appear_then_click(SURVIVAL_MOP_UP_CONFIRM,interval=1):
                continue
            if self.appear_then_click(SURVIVAL_READY_CONFIRM,interval=1):
                continue
            if self.appear_then_click(SURVIVAL_READY,interval=1):
                continue
            if self.appear(SURVIVAL_CHECK):
                if self.appear_then_click(SURVIVAL_MOP_UP_BUTTON,interval=2):
                    continue
        return True
    def _mop_up_check(self):
        for _ in self.loop():
            ocr=Digit(SURVIVAL_MOP_UP_TIMES,lang='cn')
            times=ocr.ocr_single_line(self.device.image)

            if times==0:
                self.config.SurvivalTrail_SurvivalTrialResetTimes=times
                break
            elif times==1:
                self.config.SurvivalTrail_SurvivalTrialResetTimes=times
                if self._survival_reset():
                    logger.info('survival trial reset')
                    self._mop_up()
                else :
                    break
    def _survival_reset(self):
        time=Timer(10, count=20).start()
        for _ in self.loop():
            if time.reached():
                return False
            if self.appear(SURVIVAL_RESET_FAILED):
                return False
            if self.appear_then_click(SURVIVAL_RESET_BUTTON,interval=2):
                continue
        return True


