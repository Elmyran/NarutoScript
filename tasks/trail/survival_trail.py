from module.base.timer import Timer
from module.exception import GameStuckError
from module.logger import logger
from module.ocr.ocr import Digit
from tasks.base.page import page_main
from tasks.base.task_tab.draglist import TASK_TAB_LIST
from tasks.base.task_tab.task_keyword import TrailKeyword
from tasks.base.ui import UI
from tasks.trail.assets.assets_trail import *
from tasks.trail.assets.assets_trail_survival import *


class SurvivalTrail(UI):
    def handle_survival_trail (self):
        self.device.click_record_clear()
        self.ui_ensure(page_main)
        if not TASK_TAB_LIST.search_rows(main=self,keyword=TrailKeyword):
            raise GameStuckError(' Trail Not Found')
        self._enter_survival()
        self._mop_up()
        self.ui_goto_main()
    def _enter_survival(self):
        time = Timer(10, count=10).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError("Survival Trial Stucked")
            if self.appear(SURVIVAL_PAGE_CHECK):
                break
            if self.appear(TRAIL_SURVIVAL_CHECK):
                self.device.click(TRAIL_SURVIVAL_CHECK)
                continue
            if self.appear(SURVIVAL_TELEPORT):
                break
        logger.info(f"survival trial entered")

    def _mop_up(self):
        time = Timer(40, count=60).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError("Survival Trial Stucked")
            if self.appear_then_click(SURVIVAL_TELEPORT,interval=0):
                continue
            if self.appear_then_click(SURVIVAL_CHAO_YING_CONFIRM,interval=0):
                continue
            if self.appear(SURVIVAL_CHECK):
                break
            if self.appear(SURVIVAL_HAVE_DONE):
                break

        for _ in self.loop():
            if time.reached():
                raise GameStuckError("Survival Trial Stucked")
            if self.appear(SURVIVAL_HAVE_DONE):
                break
            if self.appear(SURVIVAL_MOP_UP_DONE):
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

        for _ in self.loop():
            if time.reached():
                raise GameStuckError("Survival Trial Stucked")
            ocr=Digit(SURVIVAL_MOP_UP_TIMES,lang='cn')
            times=ocr.ocr_single_line(self.device.image)
            print(times)
            if times==0:
                self.config.SurvivalTrail_SurvivalTrialResetTimes=times
                break
            elif times==1:
                self.config.SurvivalTrail_SurvivalTrialResetTimes=times
                if self._survival_reset():
                    self._mop_up()
                else :
                    break

        return True

    def _survival_reset(self):
        time=Timer(10, count=20).start()
        for _ in self.loop():
            if time.reached():
                return False
            if self.appear(SURVIVAL_RESET_FAILED):
                return False
            if self.appear_then_click(SURVIVAL_RESET_BUTTON):
                continue
        return True



