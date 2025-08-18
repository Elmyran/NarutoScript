from module.base.timer import Timer
from module.exception import GameStuckError
from module.logger import logger
from module.ocr.ocr import Digit
from tasks.base.page import page_main
from tasks.base.ui import UI
from tasks.trail.assets.assets_trail import *
from tasks.trail.assets.assets_trail_survival import *

#todo 超影传送15关，传送13关未适配
class SurvivalTrail(UI):
    def handle_survival_trail (self):
        self.device.click_record_clear()
        self.ui_ensure(page_main)
        self._enter_trail()
        self._mop_up()
        self.survival_exit()
    def _enter_trail(self):
        if self.appear(SURVIVAL_PAGE_CHECK):
            return True
        self.device.swipe( [1200, 314],[0, 322])
        move = True
        time = Timer(10, count=10).start()
        m=2
        for _ in self.loop():
            if time.reached():
                if move and m%2==0:
                    self.device.swipe([0, 322], [1200, 314])
                    time.reset()
                    m=m+1
                elif move and m%2==1:
                    self.device.swipe( [1200, 314],[0, 322])
                    m=m+1
                    time.reset()
                elif m>5:
                    raise GameStuckError("Survival Trial Stucked")
            if self.appear(SURVIVAL_PAGE_CHECK):
                break
            TRAIL_RED_DOT.load_search((200, 50, 1000, 700))
            if self.appear_then_click(TRAIL_RED_DOT):
                continue
            MAIN_GOTO_TRAIL.load_search((200, 50, 1000, 700))
            if MAIN_GOTO_TRAIL.match_template(self.device.image,direct_match=True):
                move = False
                continue
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

    def survival_exit(self):
        time=Timer(20, count=30).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError("Survival Trial Exit   Stucked")
            if self.ui_page_appear(page_main):
                break
            if self.appear(SURVIVAL_EXIT):
                self.device.click(SURVIVAL_EXIT)
                continue
            if self.appear(TRAIL_EXIT):
                self.device.click(TRAIL_EXIT)
                continue


