from module.base.timer import Timer
from module.exception import GameStuckError
from tasks.base.page import page_battle_order, page_battle_order_rank
from tasks.base.ui import UI
from tasks.battle_order.assets.assets_battle_order import *
from tasks.freebies.assets.assets_freebies_dailyshare import QQ_MENU


class BattleOrderRank(UI):
    def handle_battle_order_rank(self):
        self.ui_ensure(page_battle_order_rank)
        self._handle_battle_order_rank_like()
        self._handle_battle_order_share()
    def _handle_battle_order_rank_like(self):
        time=Timer(20,count=20).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError("BATTLE ORDER RANK LIKE STUCK")
            if self.appear(BATTLE_ORDER_RANK_HAVE_LIKED):
                break
            if self.appear_then_click(BATTLE_ORDER_RANK_LIKE_BUTTON):
                continue
            if self.appear_then_click(BATTLE_ORDER_GOTO_RANK):
                continue

    def _handle_battle_order_share(self):
        time=Timer(30,count=30).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError('BATTLE ORDER RANK SHARE  STUCK')
            if self.appear_then_click(BATTLE_ORDER_SHARE_GOTO_QQ):
                continue
            if self.appear_then_click(BATTLE_ORDER_RANK_GOTO_SHARE):
                continue
            if self.appear(QQ_MENU,interval=1):
                self.device.app_stop_adb('com.tencent.mobileqq')
                break
        for _   in self.loop():
            if time.reached():
                raise GameStuckError('BATTLE ORDER RANK SHARE BACK TO GAME STUCK')
            if self.appear(BATTLE_ORDER_RANK_GOTO_SHARE):
                break

