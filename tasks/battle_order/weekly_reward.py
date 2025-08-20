from module.base.timer import Timer

from tasks.base.page import page_battle_order
from tasks.base.ui import UI
from tasks.battle_order.assets.assets_battle_order_reward import *
from tasks.battle_order.switch import BATTLE_ORDER_TAB

class BattleOrderWeeklyReward(UI):
    def handle_battle_order_weekly_reward(self):
        self.device.click_record_clear()
        self.ui_ensure(page_battle_order)
        BATTLE_ORDER_TAB.set('周活跃',main=self)
        time=Timer(2,4).start()
        for _ in self.loop():
            if time.reached():
                break
            if self.appear_then_click(BATTLE_ORDER_WEEKLY_REWARD_CLAIM_SUCCESS,interval=0,similarity=0.9):
                continue
            res=self.detect_claimable_buttons(similarity=0.1)
            if res and len(res)>0:
                self.device.click(res[0])
                time.reset()







