from module.base.timer import Timer
from module.ocr.ocr import Digit
from tasks.base.page import page_battle_order
from tasks.base.ui import UI
from tasks.battle_order.assets.assets_battle_order_reward import *
from tasks.battle_order.ui.switch import BATTLE_ORDER_TAB
from module.logger import logger


class BattleOrderWeeklyReward(UI):
    def run(self):
        if self.config.stored.BattleOrderActivityProgress.is_expired():
            self.config.stored.BattleOrderActivityProgress.clear()
        if self.config.stored.BattleOrderActivityProgress.is_full():
            return True

        self.device.click_record_clear()
        self.handle_battle_order_weekly_reward()

        return True

    def handle_battle_order_weekly_reward(self):
        self.ui_ensure(page_battle_order)
        BATTLE_ORDER_TAB.set('周活跃', main=self)
        self._claim_weekly_reward()

    def _claim_weekly_reward(self):
        checked_buttons = [
            BATTLE_ORDER_ACTIVE_POINTS_1_CHECKED,
            BATTLE_ORDER_ACTIVE_POINTS_2_CHECKED,
            BATTLE_ORDER_ACTIVE_POINTS_3_CHECKED,
            BATTLE_ORDER_ACTIVE_POINTS_4_CHECKED,
            BATTLE_ORDER_ACTIVE_POINTS_5_CHECKED,
        ]
        thresholds = [50, 100, 150, 200, 300]

        # 从存档恢复上次的领取进度
        self.current_progress = self.config.stored.BattleOrderActivityProgress.value
        logger.attr("RestoredProgress", self.current_progress)

        BATTLE_ORDER_WEEKLY_REWARD_CLAIM.load_search(BATTLE_ORDER_WEEKLY_REWARD_AREA.area)

        click_timer = Timer(1).start()

        for _ in self.loop():

            if self.appear_then_click(BATTLE_ORDER_WEEKLY_REWARD_CLAIM_SUCCESS, interval=0):
                click_timer.reset()
                continue

            # 读取本周活跃度 
            current_points = self._get_current_activity_points()
            # 检测已领取档位
            self._get_current_progress(checked_buttons, thresholds)

            # 5档全部领完 → 退出
            if self.current_progress >= thresholds[-1]:
                logger.info("All 5 weekly rewards claimed")
                break

            if click_timer.reached():
                # 找出可领取的档位：活跃度达标 且 该档位尚未领取
                claimable = any(
                    self.current_progress < t <= current_points
                    for t in thresholds
                )
                if claimable:
                    self.device.click(BATTLE_ORDER_WEEKLY_REWARD_CLAIM)
                    click_timer.reset()
                else:
                    # 没有可领取的档位（活跃度不够下一档，或全部领完）
                    logger.info("No claimable reward tier")
                    break

        # 循环结束后保存进度
        self.config.stored.BattleOrderActivityProgress.set(self.current_progress)

    def _get_current_activity_points(self) -> int:
        ocr = Digit(BATTLE_ORDER_WEEKLY_REWARD_ACTIVITY_POINTS)
        current_points = ocr.ocr_single_line(self.device.image)
        if current_points:
            self.config.stored.ActivityProgressWeekly.set(current_points)
        logger.attr("ActivityPoints", current_points)
        return current_points

    def _get_current_progress(self, checked_buttons, thresholds) -> int:
        current_progress = 0
        # 从高到低检查每档的 CHECKED 图标，找到已领取的最高档
        for i in range(len(thresholds) - 1, -1, -1):
            if self.appear(checked_buttons[i]):
                current_progress = thresholds[i]
                break
        if current_progress > self.current_progress:
            self.current_progress = current_progress
        logger.attr("RewardProgress", self.current_progress)


if __name__ == '__main__':
    az = BattleOrderWeeklyReward('ns', task='Alas')
    az.run()

