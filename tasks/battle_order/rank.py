import time
from module.base.timer import Timer
from module.exception import GameStuckError
from module.logger import logger
from tasks.base.assets.assets_base_page import FULL_SCREEN
from tasks.base.page import  page_battle_order_rank
from tasks.base.ui import UI
from tasks.battle_order.assets.assets_battle_order_rank import *
from tasks.freebies.assets.assets_freebies_dailyshare import QQ_MENU, SHARE_GOTO_QQ


class BattleOrderRank(UI):
    def handle_battle_order_rank(self):
        self.device.click_record_clear()
        self.ui_ensure(page_battle_order_rank)
        self._handle_battle_order_rank_like()
        self._handle_battle_order_share()
    def _handle_battle_order_rank_like(self):
        time=Timer(2,4).start()
        for _ in self.loop():
            if time.reached():
                break
            if self.match_template_color(BATTLE_ORDER_RANK_LIKE_BUTTON,interval=0):
                self.device.click(BATTLE_ORDER_RANK_LIKE_BUTTON)
                time.reset()
                continue

    def _handle_battle_order_share(self):
        packages = self.device.list_package() 
        if not 'com.tencent.mobileqq' in packages:
           logger.info('QQ not installed')  
           return True
        for _ in self.loop():
            if self.appear_then_click(BATTLE_ORDER_SHARE_GOTO_QQ):
                continue
            BATTLE_ORDER_RANK_GOTO_SHARE.load_search(FULL_SCREEN.area)
            if self.appear_then_click(BATTLE_ORDER_RANK_GOTO_SHARE,interval=0):
                continue
            current_app = self.device.app_current()
            if (current_app == 'com.tencent.mobileqq'):
                logger.info('Detected QQ is running, stopping QQ app')
                self.device.app_stop(package='com.tencent.mobileqq')
                verification_timer = Timer(2).start()
                while not verification_timer.reached():
                    if self.device.app_current() != 'com.tencent.mobileqq':
                        logger.info('QQ successfully stopped and verified')
                        verification_timer.set_current(3)
                if self.device.app_current() == 'com.tencent.mobileqq':
                    logger.info('Could not verify QQ closure')
                    continue
                else: break

        click_interval=Timer(2).start()
        for _   in self.loop():
            if self.ui_page_appear(page_battle_order_rank):
                break
            if click_interval.reached():
                self.device.click(BATTLE_ORDER_SHARE_GOTO_QQ)
                click_interval.reset()

