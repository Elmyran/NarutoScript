from module.base.timer import Timer
from module.exception import GameStuckError
from module.ocr.ocr import Digit
from tasks.base.assets.assets_base import TILI_REMAIN
from tasks.base.page import page_main, page_elite_dungeon
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
        self.ui_ensure(page_elite_dungeon)
        res=self._dungeon_sweep()
        self.ui_goto_main()
        if res:
            return True
        else:
            return False
    def _dungeon_sweep(self):
        time=Timer(40,count=60).start()
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




