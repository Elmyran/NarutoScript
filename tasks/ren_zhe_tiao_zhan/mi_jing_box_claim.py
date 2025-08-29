from module.base.timer import Timer
from tasks.autofight.joystick import GameControl
from tasks.base.page import page_ren_zhe_tiao_zhan
from tasks.ren_zhe_tiao_zhan.assets.assets_ren_zhe_tiao_zhan_mi_jing_box_claim import *
class MiJingBoxClaim(GameControl):
    def handle_mi_jing_box_claim(self):
        self.ui_ensure(page_ren_zhe_tiao_zhan)
        self._box_check()
        self._box_claim()
        self.ui_goto_main()
    def _box_claim(self):
        time=Timer(2,count=4).start()
        for _ in self.loop():
            if time.reached():
                break
            MI_JING_BOX_FREE_CLIAM_BUTTON.load_search(MI_JING_BOX_CLAIM_BUTTON_AREA.area)
            if self.appear_then_click(MI_JING_BOX_FREE_CLIAM_BUTTON,interval=1):
                time.reset()
                continue
            if self.appear_then_click(REN_ZHE_TIAO_ZHAN_GOTO_BOX,interval=1):
                time.reset()
                continue
    def _box_check(self):
        for _ in self.loop():
            REN_ZHE_TIAO_ZHAN_GOTO_BOX.load_search((0,0,1280,720))
            if self.appear(REN_ZHE_TIAO_ZHAN_GOTO_BOX):
                break
            else:
                self.move_to_direction(270,duration=0.1)


