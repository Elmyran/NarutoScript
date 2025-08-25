from module.base.timer import Timer
from tasks.base.page import page_battle_order
from tasks.base.ui import UI
from tasks.battle_order.assets.assets_battle_order_task import *
from tasks.battle_order.assets.assets_battle_order_ui import BATTLE_ORDER_DETAIL
from tasks.battle_order.switch import BATTLE_ORDER_TAB
class BattleOrderWeeklyTask(UI):
    def handle_battle_order_weekly_task(self):
        self.device.click_record_clear()
        self.ui_ensure(page_battle_order)
        BATTLE_ORDER_TAB.set('周任务',main=self)
        time=Timer(30,30).start()
        for _ in self.loop():
            if time.reached():
                break
            if self.appear(BATTLE_ORDER_TASK_END):
                break
            if self.appear_then_click(BATTLE_ORDER_TASK_REWARD_CLAIM_SUCCESS,interval=0):
                continue
            if self.appear_then_click(BATTLE_ORDER_TASK_REWARD_CLAIM_CONFIRM,interval=0):
                continue
            BATTLE_ORDER_TASK_REWARD_CLAIM.load_search(BATTLE_ORDER_DETAIL.area)
            if self.appear_then_click(BATTLE_ORDER_TASK_REWARD_CLAIM,interval=0):
                continue
            if self.appear(BATTLE_ORDER_TASK_UNFINISH,interval=1):
                break



