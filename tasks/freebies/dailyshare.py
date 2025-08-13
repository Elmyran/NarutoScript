from  module.base.timer import Timer
from module.exception import GameStuckError
from module.logger import logger

from tasks.base.page import page_main, page_panel
from tasks.base.ui import UI
from tasks.freebies.assets.assets_freebies_dailyshare import MAIN_GOTO_PANEL, SHARE_BUTTON, SHARE_GOTO_QQ, QQ_GOTO_MAIN, \
    QQ_MENU


class DailyShare(UI):
    def handle_daily_share(self):
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
            if self.appear(QQ_MENU,interval=1):
                self.device.app_stop_adb('com.tencent.mobileqq')
                break

        for _ in self.loop():
            if self.ui_page_appear(page_main):
                break
            if self.appear(SHARE_GOTO_QQ,interval=1):
                self.device.click(SHARE_BUTTON)
                continue











