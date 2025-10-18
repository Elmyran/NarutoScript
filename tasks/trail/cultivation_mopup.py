from module.ocr.ocr import Digit
from tasks.base.page import page_cultivation
from tasks.base.taskui import TaskUI
from tasks.trail.assets.assets_trail import *
from tasks.trail.assets.assets_trail_cultivation import *


class CultivationMopUp(TaskUI):
    def handle_cultivation_mop_up(self):
        self.device.click_record_clear()
        self.ui_ensure(page_cultivation)
        flag=self._cultivation_mop_up()
        if self.config.CultivationRoad_ClearRedDot and flag=='MOP_UP_SUCCESS':
            self._red_dot_clear()
        
        return flag
   
    def _cultivation_mop_up(self):
        detect_count=0
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
            else:
                detect_count+=1
                if detect_count>4:
                    ocr=Digit(CULTIVATION_MOP_UP_RESET_TIMES,lang='cn')
                    times=ocr.ocr_single_line(self.device.image)
                    if times==1:
                        return self._cultivation_reset()
                    elif times==0:
                        return 'MOP_UP_SUCCESS'

            if self.appear(CULTIVATION_RESET_MOP_UP_RUNNING):
                break
        return 'MOP_UP_SUCCESS'

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

   


    def _red_dot_clear(self):
        for _ in self.loop():
            if self.appear(CULTIVATION_BOX_CHECK):
                break
            if self.appear(CULTIVATION_BOX):
                self.device.click(CULTIVATION_BOX)
                continue

