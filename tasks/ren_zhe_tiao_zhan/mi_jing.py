from module.base.timer import Timer
from module.ocr.ocr import Digit
from tasks.base.assets.assets_base_page import FIGHT_CLOSE_CONFIRM, FIGHT_CLOSE
from tasks.base.page import page_main, page_mi_jing_room
from tasks.base.ui import UI
from tasks.ren_zhe_tiao_zhan.assets.assets_ren_zhe_tiao_zhan import *
from tasks.ren_zhe_tiao_zhan.auto_fight import AutoBattle
from tasks.ren_zhe_tiao_zhan.ocr import MiJingOcr
class MiJing(UI):
    def handle_mi_jing(self):
        self.device.click_record_clear()
        self.ui_ensure(page_main)
        self.swipe_and_appear_then_click(click_obj=MAIN_GOTO_REN_ZHE_TIAO_ZHAN,check_obj=REN_ZHE_TIAO_ZHAN_CHECK,right=True)
        self.ui_ensure(page_mi_jing_room)
        self._mi_jing_fight()
        self.ui_goto_main()
    def _select_mi_jing(self):
        ocr=MiJingOcr(MI_JING_TYPE)
        ticket=Digit(MI_JING_REMAIN_CHALLENGE_TICKETS)
        type_1=['落岩秘境','雷霆秘境','烈炎秘境','水牢秘境','罡体秘境']
        type_2=['毒风秘境','阴阳秘境']
        for _ in  self.loop():
            type=ocr.ocr_single_line(self.device.image)
            if type and len(type)>0:
                if type in type_1:
                    return True
                elif type in type_2:
                    break
            if self.appear_then_click(MI_JING_START_NOTIFY,interval=1):
                continue
            if self.appear_then_click(MI_JING_START_CONFIRM,interval=1):
                continue
            if self.appear(MI_JING_ROOM_CHECK,interval=1):
                time=Timer(1,count=3).start()
                flag=True
                while flag:
                    if time.reached():
                        return 'End'
                    remain_tickets=ticket.ocr_single_line(self.device.image)
                    if remain_tickets>0:
                        self.device.click(MI_JING_ROOM_CHECK)
                        flag=False
        for _ in self.loop():
            if self.appear(MI_JING_ROOM_CHECK,interval=1):
                break
            if self.appear_then_click(FIGHT_CLOSE_CONFIRM,interval=0):
                continue
            if self.appear_then_click(FIGHT_CLOSE,interval=2,similarity=0.9):
                continue
        return False

    def _mi_jing_fight(self):
        battle=AutoBattle(config=self.config,device=self.device)
        battle.start_services()
        try:
            for _ in self.loop():
                MI_JING_REWARD_EXIT.load_search(MI_JING_REWARD_AREA.area)
                if self.appear_then_click(MI_JING_REWARD_EXIT,interval=0):
                    continue
                MI_JING_SUCCESS.load_search(MI_JING_REWARD_AREA.area)
                if self.appear_then_click(MI_JING_SUCCESS,interval=0):
                    continue
                res=self._select_mi_jing()
                if res=='End':
                    break
                elif res==False:
                    continue
                elif res==True:
                    battle.run()
        finally:
            battle.stop_services()



