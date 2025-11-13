from venv import logger
from module.base.timer import Timer
from module.config.utils import get_server_next_monday_update
from tasks.base.taskui import TaskUI
from datetime import datetime, timedelta
from module.config.utils import get_server_next_monday_update
from module.ocr.ocr import Digit
from tasks.base.assets.assets_base_page import CLOSE
from tasks.base.page import page_cultivation
from tasks.trail.assets.assets_trail import *
from tasks.trail.assets.assets_trail_cultivation import *
from tasks.base.assets.assets_base_code_second import *
from tasks.trail.ocr import CultivationDuration

class CultivationRoad(TaskUI):
    def run(self):
        delay_time=self.handle_cultivation_mop_up()
        if self.config.CultivationRoad_ClearRedDot:
            self._red_dot_clear()
        self.config.task_delay(target=delay_time)
        self.config.task_stop()
        
    def handle_cultivation_mop_up(self):
        self.device.click_record_clear()
        self.ui_ensure(page_cultivation)
        delay=self.is_excute_manual_before()
        if delay:
            self.back_to_cultivation_page()
            return delay
        ocr=Digit(CULTIVATION_RESET_COUNT)
        count=ocr.ocr_single_line(self.device.image)
        if count>0:
            self.reset()
            if self.mop_up_finish():
                self.back_to_cultivation_page()
                monday = get_server_next_monday_update(self.config.Scheduler_ServerUpdate)
                return monday
            self.back_to_cultivation_page()   
            return datetime.now()+timedelta(hours=2)
            
        else:
            if not self.try_mop_up():
                self.back_to_cultivation_page()
                monday = get_server_next_monday_update(self.config.Scheduler_ServerUpdate)
                return monday
            if self.mop_up_finish():
                self.back_to_cultivation_page()
                monday = get_server_next_monday_update(self.config.Scheduler_ServerUpdate)
                return monday
            self.back_to_cultivation_page() 
            return datetime.now()+timedelta(hours=2)
    def is_excute_manual_before(self):
        logger.info("Checking if cultivation mop-up is in progress or rewards are to be claimed...")
        timer=Timer(1,count=3).start()
        for _ in self.loop():
            if timer.reached():
                logger.info('check timeout, assuming no mop-up in progress or rewards to claim.')
                return False
            if self.is_reward_claim():
                self.claim_reward()
                return False
            if self.is_mop_up_running():
                ocr=CultivationDuration(CULTIVATION_MOP_UP_REMAIN_TIMES)
                delay_time=ocr.ocr_single_line(self.device.image)
                return delay_time
        

    def back_to_cultivation_page(self):
        logger.info("Returning to cultivation page...")
        for _ in self.loop():
            if self.match_template_color(CULTIVATION_BOX):
                break
            if self.appear_then_click(CLOSE,interval=1):
                continue
    def try_mop_up(self):
        logger.info("Trying to start cultivation mop-up...")
        for _ in self.loop():
            if self.appear_then_click(CULTIVATION_MOP_UP_BUTTON,interval=1):
                continue
            if self.appear(CULTIVATION_MOP_UP_DONE):
                return False
            if self.appear(CULTIVATION_RESET_MOP_UP_FINISH_NOW):
                break
            if self.appear(CULTIVATION_CLAIM_CHAO_YING):
                break
        return True
    def mop_up_finish(self):
        logger.info("Checking if cultivation mop-up is finished...")
        if self.appear(CULTIVATION_CLAIM_CHAO_YING):
            self.claim_reward()
            return True
        if not self.config.CultivationRoad_CultivationFinish:
            return False
        
        for _ in self.loop():
            if self.appear_then_click(CULTIVATION_RESET_MOP_UP_FINISH_NOW,interval=1):
                continue
            if self.appear_then_click(CULTIVATION_MOP_UP_REWARD_CLAIM,interval=1):
                continue
            if self.appear(CODE_SECOND_PASSWORD):
                self.handle_second_password(self.config.PanRen_SecondPassword)
                continue
            if self.match_template_color(CULTIVATION_MOP_UP_BUTTON):
                break
        return True
        
    def claim_reward(self):
        for _ in self.loop():
            if self.appear_then_click(CULTIVATION_CLAIM_CHAO_YING,interval=1):
                continue
            if self.appear_then_click(CULTIVATION_MOP_UP_REWARD_CLAIM,interval=1):
                continue
            if self.appear_then_click(CULTIVATION_MOP_UP_SUCCESS,interval=1):
                continue
            if self.match_template_color(CULTIVATION_MOP_UP_BUTTON):
                break
    def is_reward_claim(self):
        return self.appear(CULTIVATION_CLAIM_CHAO_YING) or self.appear(CULTIVATION_MOP_UP_REWARD_CLAIM) or self.appear(CULTIVATION_MOP_UP_SUCCESS)
    def is_mop_up_running(self):
        
        
        return self.appear(CULTIVATION_RESET_MOP_UP_FINISH_NOW)
    def reset(self):
        for _ in self.loop():
            if self.appear(CULTIVATION_RESET_MOP_UP_FINISH_NOW):
                break
            if self.appear(CULTIVATION_CLAIM_CHAO_YING):
                break         
            if self.appear_then_click(CULTIVATION_RESET_CONFIRM,interval=1):
                continue
            if self.appear_then_click(CULTIVATION_RESET_MOP_UP,interval=1):
                continue
            if self.match_template_color(CULTIVATION_RESET_BUTTON,interval=1):
                self.device.click(CULTIVATION_RESET_BUTTON)
                continue
        return True                
    def _red_dot_clear(self):
        for _ in self.loop():
            if self.appear(CULTIVATION_BOX_CHECK):
                break
            if self.appear(CULTIVATION_BOX):
                self.device.click(CULTIVATION_BOX)
                continue
