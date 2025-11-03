from module.base.timer import Timer
from module.exception import GameStuckError
from module.logger import logger
from tasks.base.page import page_main, page_daily_share
from tasks.base.taskui import TaskUI
from tasks.freebies.assets.assets_freebies_dailyshare import SHARE_BUTTON, SHARE_GOTO_QQ


class DailyShare(TaskUI):
    def handle_daily_share(self):
        if self.config.stored.DailyShareFinishCount.is_expired():
            self.config.stored.DailyShareFinishCount.clear()
        if self.config.stored.DailyShareFinishCount.is_full():
            return True
        self._daily_share_flow()
        self.config.stored.DailyShareFinishCount.add()
    def _daily_share_flow(self):
        packages = self.device.list_package() 
        if not 'com.tencent.mobileqq' in packages:  
           logger.warning('QQ not installed')
           return True
        self._share_goto_other_app()
        self._ensure_game_foreground()
        self._handle_remain_ui()
    def _share_goto_other_app(self):
        self.device.click_record_clear()
        timeout = Timer(30, count=30).start()  
        self.ui_ensure(page_daily_share)
        for _ in self.loop():
            if timeout.reached():  
                raise GameStuckError('Share goto other app timeout') 
            self.device.click_record_clear()
            if self.appear(SHARE_GOTO_QQ,interval=2):
                self.device.click(SHARE_GOTO_QQ)
                continue
            if self.device.app_current() == 'com.tencent.mobileqq':  
                logger.info('Detected QQ is running, stopping QQ app')  
                self.device.app_stop(package='com.tencent.mobileqq')  
                if self._verify_app_stopped('com.tencent.mobileqq'):  
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
        timeout = Timer(20, count=20).start()  
        for _   in self.loop():
            if timeout.reached():  
                raise GameStuckError('Handle remain ui timeout') 
            if self.ui_page_appear(page_main):
                break
            if self.appear_then_click(SHARE_GOTO_QQ,interval=2):
                continue

    def _verify_app_stopped(self, package_name, timeout=2):  
        verification_timer = Timer(timeout).start()  
        while not verification_timer.reached():  
            if self.device.app_current() != package_name:  
                logger.info(f'{package_name} successfully stopped and verified')  
                return True  
            self.device.screenshot()
        logger.warning(f'Could not verify {package_name} closure')  
        return False


az=DailyShare('ns',task='Alas')
az.ui_ensure(page_daily_share)





