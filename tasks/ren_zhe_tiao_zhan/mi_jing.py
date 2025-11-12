from module.logger import logger
from tasks.ren_zhe_tiao_zhan.ocr import MiJingDigit
from tasks.base.assets.assets_base_page import FIGHT_CLOSE_CONFIRM, FIGHT_CLOSE
from tasks.base.page import  page_mi_jing_room
from tasks.base.taskui import TaskUI
from tasks.ren_zhe_tiao_zhan.assets.assets_ren_zhe_tiao_zhan import *
from tasks.ren_zhe_tiao_zhan.auto_fight import AutoBattle
from tasks.ren_zhe_tiao_zhan.ocr import MiJingOcr
class MiJing(TaskUI):
    ticket:int=0
    pre_count:int=0
    def run(self):
        if self.config.stored.MiJingCount.is_expired():
            self.config.stored.MiJingCount.clear()
        self.pre_count=self.config.stored.MiJingCount.value
        self.device.click_record_clear()
        self.handle_mi_jing()
       

    def handle_mi_jing(self):
        self.ui_ensure(page_mi_jing_room)
        battle=AutoBattle(config=self.config,device=self.device)
        for _ in self.loop():
            self.ticket_recognition()
            if self.is_going_to_stop():
                break
            self.enter_mi_jing()
            if not self.is_going_fight():
                self.back_to_mi_jing_room()
                continue
            battle.run()
            self.back_to_mi_jing_room()
        return True
    def is_going_to_stop(self):
        if self.config.stored.MiJingCount.value - self.pre_count == self.config.MiJingCount_MiJingFightCount:
            logger.info(f'MiJing reached the limit: {self.config.MiJingCount_MiJingFightCount}, task will stop')
            return True
        if self.ticket==0:
            return True
        return False


    def back_to_mi_jing_room(self):
        for _ in self.loop():
            if self.appear_then_click(MI_JING_FAIL,interval=1):
                continue
            MI_JING_SUCCESS.load_search(MI_JING_REWARD_AREA.area)
            if self.appear_then_click(MI_JING_SUCCESS,interval=1):
                continue
            MI_JING_REWARD_EXIT.load_search(MI_JING_REWARD_AREA.area)
            if self.appear(MI_JING_REWARD_EXIT,interval=1):
                MI_JING_REWARD_EXIT.clear_offset()
                self.device.click(MI_JING_REWARD_EXIT)
                continue
            if self.appear(MI_JING_REWARD_CLAIM,interval=1):
                MI_JING_REWARD_CLAIM.clear_offset()
                self.device.click(MI_JING_REWARD_CLAIM)
                continue
            if self.appear_then_click(FIGHT_CLOSE_CONFIRM,interval=0):
                continue
            if self.appear_then_click(FIGHT_CLOSE,interval=2):
                continue
            if self.appear(MI_JING_ROOM_CHECK) and self.appear(MI_JING_TICKET_CHECK,similarity=0.6):
                self.device.click_record_remove(FIGHT_CLOSE_CONFIRM)
                break
        
    def is_going_fight(self):
        ocr=MiJingOcr(MI_JING_TYPE)
        enable_types=[]
        unenable_types=['毒风秘境','阴阳秘境']
        if self.config.MiJingType_LuoYan:
            enable_types.append('落岩秘境')
        else:
            unenable_types.append('落岩秘境')
        if self.config.MiJingType_LeiTing:
            enable_types.append('雷霆秘境')
        else:
            unenable_types.append('雷霆秘境')
        if self.config.MiJingType_LieYan:
            enable_types.append('烈炎秘境')
        else:
            unenable_types.append('烈炎秘境')
        if self.config.MiJingType_ShuiLao:
            enable_types.append('水牢秘境')
        else:
            unenable_types.append('水牢秘境')
        if self.config.MiJingType_GangTi:
            enable_types.append('罡体秘境')
        else:
            unenable_types.append('罡体秘境')
        type=ocr.ocr_single_line(self.device.image)
        if type in enable_types:
            return True
        elif type in unenable_types:
            return False
        return False
    def enter_mi_jing(self):
        for _ in self.loop():
            if self.appear_then_click(MI_JING_START_NOTIFY,interval=1):
                continue
            if self.appear_then_click(MI_JING_START_CONFIRM,interval=1):
                continue
            if self.appear_then_click(MI_JING_ROOM_START_FIGHT,interval=1):
                continue
            if self.appear(MI_JING_FIGHT_CHECK):
                break

    def ticket_recognition(self):
        ocr=MiJingDigit(MI_JING_REMAIN_CHALLENGE_TICKET)
        self.ticket=ocr.ocr_single_line(self.device.image)
