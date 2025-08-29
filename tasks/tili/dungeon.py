from module.base.timer import Timer
from module.exception import GameStuckError
from module.ocr.ocr import Digit, DigitCounter
from tasks.base.assets.assets_base import TILI_REMAIN, TI_LI_REMAIN_COUNTER
from tasks.base.page import page_main, page_elite_dungeon
from tasks.base.ui import UI
from tasks.tili.assets.assets_tili_dungeon import *

class Dungeon(UI):
    def handle_dungeon(self):
        self.device.click_record_clear()
        self.device.stuck_record_clear()
        self.ui_ensure(page_main)
        ocr=DigitCounter(TI_LI_REMAIN_COUNTER,lang='cn')
        current,remain,total=ocr.ocr_single_line(self.device.image)
        if current<10 and total==200:
            self.config.TiLi_TiLiRemain=current
            return False
        self.ui_ensure(page_elite_dungeon)
        res=self._dungeon_sweep()
        self.ui_goto_main()
        if res:
            return True
        else:
            return False
    def _dungeon_sweep(self):
        time=Timer(60,count=60).start()
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
            if self.image_color_count(SWEEP_BUTTON,color=(251,182,0),threshold=221,count=200):
                continue
            if self.appear_then_click(CONVENIENT_SWEEP):
                continue




