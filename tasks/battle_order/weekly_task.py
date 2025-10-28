
from module.logger.logger import logger
from module.base.timer import Timer
from module.ocr.ocr import DigitCounter
from tasks.base.page import page_battle_order
from tasks.base.ui import UI
from tasks.battle_order.assets.assets_battle_order_task import *
from tasks.battle_order.assets.assets_battle_order_ui import BATTLE_ORDER_DETAIL
from tasks.battle_order.switch import BATTLE_ORDER_TAB
class BattleOrderWeeklyTask(UI):
    def handle_battle_order_weekly_task(self):
        if self.config.stored.BattleOrderTaskProgress.is_expired():
            self.config.stored.BattleOrderTaskProgress.clear()
        if self.config.stored.BattleOrderTaskProgress.is_full():
            return True
        self.device.click_record_clear()
        self.ui_ensure(page_battle_order)
        BATTLE_ORDER_TAB.set('周任务',main=self)
        claim_time=Timer(3,6).start()
        for _ in self.loop():
            if claim_time.reached():
                break
            if self.appear(BATTLE_ORDER_TASK_END):
                break
            if self.appear_then_click(BATTLE_ORDER_TASK_REWARD_CLAIM_SUCCESS,interval=1):
                claim_time.reset()
                continue
            if self.appear_then_click(BATTLE_ORDER_TASK_REWARD_CLAIM_CONFIRM,interval=0):
                claim_time.reset()
                continue
            BATTLE_ORDER_TASK_REWARD_CLAIM.load_search(BATTLE_ORDER_DETAIL.area)
            if self.match_template_color(BATTLE_ORDER_TASK_REWARD_CLAIM,interval=1):
                self.device.click(BATTLE_ORDER_TASK_REWARD_CLAIM)
                claim_time.reset()
                continue
            
        ocr_time=Timer(1,3).start()
        progress=0
        ocr=DigitCounter(BATTLE_ORDER_TASK_PROGRESS)
        for _ in self.loop():
            if ocr_time.reached():
                break
            current,remain,total=ocr.ocr_single_line(self.device.image)
            if total!=0:
                progress=current
                break
        self.config.stored.BattleOrderTaskProgress.value=progress





