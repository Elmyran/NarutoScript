from module.base.timer import Timer
from module.exception import GameStuckError
from module.ocr.ocr import Digit
from tasks.base.assets.assets_base import TILI_REMAIN
from tasks.base.page import page_main
from tasks.base.ui import UI
from tasks.tili.assets.assets_tili_dungeon import *

class Dungeon(UI):
    def handle_dungeon(self):
        self.device.click_record_clear()
        self.ui_ensure(page_main)
        ocr=Digit(TILI_REMAIN,lang='cn')
        ti_li=ocr.ocr_single_line(self.device.image)
        self.config.TiLi_TiLiRemain=ti_li
        if ti_li<10:
            return False
        res=self._dungeon_enter()
        self._dungeon_exit()
        if res:
            return True
        else:
            return False
    def _dungeon_enter(self):

        self.device.click_record_clear()
        time=Timer(20,count=30).start()
        time_enter=Timer(8,count=10).start()
        for _ in self.loop():
            if time_enter.reached():
                raise GameStuckError('Dungeon enter timeout')
            if self.appear(CONVENIENT_SWEEP):
                break
            if self.appear(SWITCH_TO_DUNGEON):
                self.device.click(SWITCH_TO_DUNGEON)
                continue
            if self.appear(MAIN_GOTO_DUNGEON):
                self.device.click(MAIN_GOTO_DUNGEON)
                continue

        for _ in self.loop():
            if  time.reached():
                raise GameStuckError('Dungeon Sweep Stucked')
            if self.appear(SWEEP_DONE):
                return True
            if self.appear(TI_LI_SHORTAGE):
                return False
            if self.appear(SWEEP_END_CONFIRM):
                return False
            if SWEEP_RUNNING.match_template(self.device.image,direct_match=True):
                continue
            if self.appear_then_click(SWEEP_CONFIRM_BUTTON):
                continue
            if self.appear_then_click(SWEEP_BUTTON):
                continue
            if self.appear_then_click(CONVENIENT_SWEEP):
                continue


    def _dungeon_exit(self):
        time=Timer(10,count=20).start()
        self.device.click_record_clear()
        for _ in self.loop():
            if  time.reached():
                raise GameStuckError('Dungeon Exit Stucked')
            if self.ui_page_appear(page_main):
                break
            if self.appear_then_click(TI_LI_SHORTAGE,interval=0):
                continue
            if self.appear(SWEEP_END_CONFIRM):
                self.device.click(DUNGEON_EXIT)
                continue
            if SWEEP_RUNNING.match_template(self.device.image,direct_match=True):
                self.device.click(DUNGEON_EXIT)
                self.device.click_record_remove(DUNGEON_EXIT)
                continue
            if self.appear(SWEEP_BUTTON):
                self.device.click(DUNGEON_EXIT)
                continue
            if self.appear(DUNGEON_EXIT):
                self.device.click(DUNGEON_EXIT)
                continue



