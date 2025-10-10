from module.base.timer import Timer
from module.exception import GameStuckError
from module.ocr.ocr import Digit
from tasks.base.assets.assets_base_page import FIGHT_CLOSE_CONFIRM, FIGHT_CLOSE
from tasks.base.page import page_main, page_mi_jing_room
from tasks.base.task_tab.draglist import TASK_TAB_LIST
from tasks.base.task_tab.task_keyword import RenZheTiaoZhanKeyword
from tasks.base.ui import UI
from tasks.ren_zhe_tiao_zhan.assets.assets_ren_zhe_tiao_zhan import *
from tasks.ren_zhe_tiao_zhan.auto_fight import AutoBattle
from tasks.ren_zhe_tiao_zhan.ocr import MiJingOcr
class MiJing(UI):
    def handle_mi_jing(self):
        if self.config.stored.MiJingCount.is_expired():
            self.config.stored.MiJingCount.clear()
        pre_count=self.config.stored.MiJingCount.value
        self.device.click_record_clear()

        self.ui_ensure(page_mi_jing_room)
        self._mi_jing_fight()
        if (self.config.stored.MiJingCount.value >= 6 > pre_count) or (
                self.config.stored.MiJingCount.value >= 15 > pre_count) or (
                self.config.stored.MiJingCount.value >= 21 > pre_count):
            from tasks.ren_zhe_tiao_zhan.mi_jing_box_claim import MiJingBoxClaim
            MiJingBoxClaim(config=self.config,device=self.device).handle_mi_jing_box_claim()
        self.ui_goto_main()
        return True
    def _select_mi_jing(self):
        ocr=MiJingOcr(MI_JING_TYPE)
        ticket=Digit(MI_JING_REMAIN_CHALLENGE_TICKET)
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

        for _ in  self.loop():
            type=ocr.ocr_single_line(self.device.image)
            if type and len(type)>0:
                if type in enable_types:
                    return True
                elif type in unenable_types:
                    break
            if self.appear_then_click(MI_JING_START_NOTIFY,interval=1):
                continue
            if self.appear_then_click(MI_JING_START_CONFIRM,interval=1):
                continue
            if self.appear(MI_JING_ROOM_START_FIGHT,interval=1):
                time=Timer(1,count=3).start()
                flag=True
                while flag:
                    if time.reached():
                        return 'End'
                    remain_tickets=ticket.ocr_single_line(self.device.image)
                    if remain_tickets>0:
                        self.device.click_record_remove(MI_JING_ROOM_START_FIGHT)
                        self.device.click(MI_JING_ROOM_START_FIGHT)
                        flag=False
        for _ in self.loop():
            if self.appear(MI_JING_ROOM_CHECK,interval=1):
                self.device.click_record_remove(FIGHT_CLOSE_CONFIRM)
                break
            if self.appear_then_click(FIGHT_CLOSE_CONFIRM,interval=0):
                continue
            if self.appear_then_click(FIGHT_CLOSE,interval=2,similarity=0.9):
                continue
        return False

    def _mi_jing_fight(self):
        battle=AutoBattle(config=self.config,device=self.device)
        for _ in self.loop():
            self.device.click_record_remove(MI_JING_REWARD_EXIT)
            self.device.click_record_remove(MI_JING_SUCCESS)
            MI_JING_REWARD_EXIT.load_search(MI_JING_REWARD_AREA.area)
            if self.appear(MI_JING_REWARD_EXIT,interval=1):
                MI_JING_REWARD_EXIT.clear_offset()
                self.device.click(MI_JING_REWARD_EXIT)
                continue
            MI_JING_SUCCESS.load_search(MI_JING_REWARD_AREA.area)
            if self.appear(MI_JING_SUCCESS,interval=1):
                MI_JING_SUCCESS.clear_offset()
                self.device.click(MI_JING_SUCCESS)
                continue
            if self.appear(MI_JING_ROOM_CHECK):
                res=self._select_mi_jing()
                if res=='End':
                    break
                elif res==False:
                    continue
                elif res==True:
                    battle.run()
       


