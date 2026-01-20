from module.base.timer import Timer
from module.exception import GameStuckError
from module.logger import logger
from tasks.base.assets.assets_base_page import FULL_SCREEN
from tasks.base.page import  page_battle_order_rank
from tasks.base.ui import UI
from tasks.battle_order.assets.assets_battle_order_rank import *


class BattleOrderRank(UI):
    def run(self):

        if not self.config.BattleOrder_LikeAndShare:
            return True
        if self.config.stored.BattleOrderRank.is_expired():
                self.config.stored.BattleOrderRank.clear()
        if self.config.stored.BattleOrderRank.is_full():
            logger.info('BattleOrderRank 本周已完成，跳过')
            return True
        self.handle_battle_order_rank()
        self.config.stored.BattleOrderRank.add()
    def handle_battle_order_rank(self):
        self.device.click_record_clear()
        self._handle_battle_order_rank_like()
        self._battle_order_share_flow()
    def _handle_battle_order_rank_like(self):
        self.ui_ensure(page_battle_order_rank)
        time=Timer(2,4).start()
        for _ in self.loop():
            if time.reached():
                break
            if self.match_template_color(BATTLE_ORDER_RANK_LIKE_BUTTON,interval=0):
                self.device.click(BATTLE_ORDER_RANK_LIKE_BUTTON)
                time.reset()
                continue

    def _battle_order_share_flow(self):
        packages = self.device.list_package() 
        if not 'com.tencent.mobileqq' in packages:
           logger.info('QQ not installed')  
           return True
        self.ui_ensure(page_battle_order_rank)
        self._share_goto_other_app()
        self._ensure_game_foreground()
        self._handle_remain_ui()
    def _share_goto_other_app(self):
        apps=['com.tencent.mobileqq', 'com.tencent.mm']
        time=Timer(30,30).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError('BATTLE_ORDER_RANK_SHARE_TIMEOUT')
            if self.appear_then_click(BATTLE_ORDER_SHARE_GOTO_OTHER_APP,interval=2):
                continue
            BATTLE_ORDER_RANK_GOTO_SHARE.load_search(FULL_SCREEN.area)
            if self.appear_then_click(BATTLE_ORDER_RANK_GOTO_SHARE,interval=1):
                continue
            if self.device.app_current() in apps:  
                logger.info('Detected App is running, stopping app')
                if self.device.app_current() == apps[0]:
                    self.device.app_stop(package=apps[0])  
                    if self._verify_app_stopped(apps[0]):  
                        return True  
                elif self.device.app_current() == apps[1]:
                    self.device.app_stop(package=apps[1])  
                    if self._verify_app_stopped(apps[1]):  
                        return True
                continue

       
    def _ensure_game_foreground(self):
        logger.info('Bringing game back to foreground')
        time=Timer(10).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError('Ensure game foreground timeout')
            if self.device.app_is_running():
                break
            else :
                self.device.app_start_adb()
        
    def _handle_remain_ui(self):
        click_interval=Timer(2).start()
        time=Timer(20,20).start()
        for _   in self.loop():
            if time.reached():
                raise GameStuckError('Handle remain ui timeout')
            if self.ui_page_appear(page_battle_order_rank):
                break
            if click_interval.reached():
                self.device.click(BATTLE_ORDER_SHARE_GOTO_OTHER_APP)
                click_interval.reset()

    def _verify_app_stopped(self, package_name, timeout=2):  
        verification_timer = Timer(timeout).start()  
        while not verification_timer.reached():  
            if self.device.app_current() != package_name:  
                logger.info(f'{package_name} successfully stopped and verified')  
                return True  
            self.device.screenshot()
        logger.warning(f'Could not verify {package_name} closure')  
        return False
