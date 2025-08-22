from module.base.timer import Timer
from tasks.activity.assets.assets_activity_diao_yu_da_shi import *
from tasks.base.page import page_diao_yu_da_shi
from tasks.base.ui import UI


class DiaoYuDaShi(UI):
    def handle_diao_yu_da_shi(self):
        self.ui_ensure(page_diao_yu_da_shi)
        self.select_checkpoint()
        for _ in self.loop():
            self.device.click_record_clear()
            self.device.stuck_record_clear()
            if  self.check_fish() :
                self._fishing_start()
                self.ui_ensure(page_diao_yu_da_shi)
                self.select_checkpoint()
            else:
                self._fishing_start()
    def select_checkpoint(self):
        for _ in self.loop():
            self.device.click_record_clear()
            self.device.stuck_record_clear()
            if self.appear(DIAO_YU_CHECK):
                break
            CHECKPOINT_RED_DOT.load_search(CHECKPOINT_AREA.area)
            if self.appear_then_click(CHECKPOINT_RED_DOT,interval=1):
                continue
            if self.appear_then_click(CURRENT_CHECKPOINT_BUTTON,interval=1):
                continue

    def _fishing_start(self):
        self.device.screenshot()
        for _ in self.loop():
            self.device.click_record_clear()
            self.device.stuck_record_clear()
            if self.appear_then_click(FISHING_SUCCESS,interval=0):
                break
            if self.appear_then_click(FISHING_UPGRADE_CONFIRM,interval=0):
                break
            SPECIAL_FISH.load_search([0,0,1280,720])
            if self.appear_then_click(SPECIAL_FISH,interval=0,similarity=0.85):
                continue
            self.device.click(DIAO_YU_CHECK)
        time=Timer(3,count=6).start()
        for _ in self.loop():
            self.device.click_record_clear()
            self.device.stuck_record_clear()
            if self.ui_page_appear(page_diao_yu_da_shi):
                break
            if  time.reached():
                break
            if self.appear_then_click(FISHING_SUCCESS,interval=0):
                continue
            if self.appear_then_click(FISHING_UPGRADE_CONFIRM,interval=0):
                continue

    def check_fish(self):
        time=Timer(5,count=6).start()
        for _ in self.loop():
            self.device.click_record_clear()
            self.device.stuck_record_clear()
            if time.reached():
                return False
            SPECIAL_FISH.load_search([0,0,1280,720])
            if self.appear_then_click(SPECIAL_FISH,interval=0,similarity=0.3):
                continue



az=DiaoYuDaShi('alas',task='Alas')
az.handle_diao_yu_da_shi()