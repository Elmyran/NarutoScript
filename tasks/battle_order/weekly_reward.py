from module.base.timer import Timer
from tasks.base.page import page_battle_order
from tasks.base.ui import UI
from tasks.battle_order.assets.assets_battle_order_reward import *
from tasks.battle_order.ocr import BattleOrderOcr
from tasks.battle_order.ui.switch import BATTLE_ORDER_TAB

class BattleOrderWeeklyReward(UI):
    current_progress=0
    def run(self):
        if self.config.stored.BattleOrderActivityPoints.is_expired():
            self.config.stored.BattleOrderActivityPoints.clear()
        if self.config.stored.BattleOrderActivityPoints.is_full():
            return True
        self.device.click_record_clear()
        self.handle_battle_order_weekly_reward()
        return True
    def handle_battle_order_weekly_reward(self):
        self.ui_ensure(page_battle_order)
        BATTLE_ORDER_TAB.set('周活跃',main=self)
        self._claim_weekly_reward()
    def _claim_weekly_reward(self):
        checked_buttons = [  
            BATTLE_ORDER_ACTIVE_POINTS_1_CHECKED,  
            BATTLE_ORDER_ACTIVE_POINTS_2_CHECKED,   
            BATTLE_ORDER_ACTIVE_POINTS_3_CHECKED,  
            BATTLE_ORDER_ACTIVE_POINTS_4_CHECKED,  
            BATTLE_ORDER_ACTIVE_POINTS_5_CHECKED  
        ]  
        progress = [50, 100, 150, 200, 300]  
        click_timer=Timer(1).start()
        current_points=self._get_current_activity_points()

        for _ in self.loop():
            if self.appear_then_click(BATTLE_ORDER_WEEKLY_REWARD_CLAIM_SUCCESS,interval=0):
                click_timer.reset()
                continue
            self._get_current_progress(checked_buttons,progress)
            if self.current_progress==progress[4]:
                break
            if click_timer.reached():
                claimable = []  
                for i, threshold in enumerate(progress):  
                    if (self.current_progress < threshold <= current_points):  
                        claimable.append(checked_buttons[i])
                if claimable:
                        self.device.click(claimable[0])
                        click_timer.reset()
                else:
                    break
                    
        self.config.stored.BattleOrderActivityPoints.value=self.current_progress
    def _get_current_activity_points(self) -> int:
        ocr=BattleOrderOcr(BATTLE_ORDER_WEEKLY_REWARD_ACTIVITY_POINTS)
        current_points=0
        ocr_times=Timer(1,3).start()
        for _ in self.loop():
            if ocr_times.reached():
                break
            res=ocr.ocr_single_line(self.device.image)
            if res!=0:
                current_points=res
                break
   
        return current_points
    def _get_current_progress(self,checked_buttons,thresholds) -> int:
        current_progress = 0  
        # 从高到低检查每个阈值
        for i in range(len(thresholds) - 1, -1, -1):
            if self.appear(checked_buttons[i],similarity=0.6):  
                current_progress = thresholds[i]
                break  # 找到最高的就停止
        if current_progress>self.current_progress:
            self.current_progress=current_progress
