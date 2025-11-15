from module.base.timer import Timer
from module.logger import logger
from module.ocr.ocr import Digit
from tasks.base.page import page_survival_trail
from tasks.base.taskui import TaskUI
from tasks.trail.assets.assets_trail import *
from tasks.trail.assets.assets_trail_survival import *


class Survival(TaskUI):
    
    def run(self):
        self.handle_survival_trail()
        self.config.task_delay(server_update=True)
        self.config.task_stop()
    def handle_survival_trail (self):
        self.device.click_record_clear()
        self.ui_ensure(page_survival_trail)
        self._mop_up()
        if self._survival_reset():
            self._mop_up()
    def _mop_up(self):
        logger.info('start mop up')
        for _ in self.loop():
            if self.appear_then_click(SURVIVAL_TELEPORT,interval=1):
                continue
            if self.appear_then_click(SURVIVAL_CHAO_YING_CONFIRM,interval=1):
                continue
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
            if self.match_template_color(SURVIVAL_MOP_UP_BUTTON,interval=2):
                self.device.click(SURVIVAL_MOP_UP_BUTTON)
                continue
        return True
    def _survival_reset(self):
        logger.info('survival trial reset')
        ocr=Digit(SURVIVAL_MOP_UP_TIMES,lang='cn')
        times=ocr.ocr_single_line(self.device.image)
        if times==0:
            self.config.SurvivalTrail_SurvivalTrialResetTimes=times
            logger.info('no reset times left')
            return False
        timeout=Timer(10, count=10).start()
        for _ in self.loop():
            if timeout.reached():
                break
            if self.appear(SURVIVAL_RESET_FAILED):
                break
            if self.appear_then_click(SURVIVAL_RESET_CONFIRM,interval=1):
                continue
            if self.appear_then_click(SURVIVAL_RESET_BUTTON,interval=2):
                continue
        return True
