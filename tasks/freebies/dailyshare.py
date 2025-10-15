from  module.base.timer import Timer
from module.exception import GameStuckError
from module.logger import logger

from tasks.base.page import page_main, page_panel
from tasks.base.ui import UI
from tasks.freebies.assets.assets_freebies_dailyshare import SHARE_BUTTON, SHARE_GOTO_QQ


class DailyShare(UI):
    def handle_daily_share(self):
        if self.config.stored.DailyShareFinishCount.is_expired():
            self.config.stored.DailyShareFinishCount.clear()
        if self.config.stored.DailyShareFinishCount.is_full():
            return True
        self._share()
        self.config.stored.DailyShareFinishCount.add()
    def _share(self):
        packages = self.device.list_package() 
        if not 'com.tencent.mobileqq' in packages:  
           logger.info('QQ not installed')
           return True
        self.device.click_record_clear()
        self.ui_ensure(page_panel)
        time=Timer(30,count=30).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError("DailyShare Game stuck")
            self.device.click_record_clear()
            if self.appear(SHARE_BUTTON,interval=1):
                self.device.click(SHARE_BUTTON)
                continue
            if self.appear(SHARE_GOTO_QQ,interval=2):
                self.device.click(SHARE_GOTO_QQ)
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
            if time.reached():
                raise GameStuckError('BATTLE ORDER RANK SHARE BACK TO GAME STUCK')
            if self.ui_page_appear(page_main):
                break
            if click_interval.reached():
                self.device.click(SHARE_GOTO_QQ)
                click_interval.reset()
        









