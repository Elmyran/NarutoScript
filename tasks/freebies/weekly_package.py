from tasks.base.page import  page_chongzhi
from tasks.base.ui import UI
from tasks.freebies.assets.assets_freebies_weekly_package import *


class WeeklyPackage(UI):
    def handle_weekly_package(self):
        self.ui_ensure(page_chongzhi)
        for _ in self.loop():
            if self.appear(WEEKLY_PACKAGE_HAVE_CLAIM_DONE):
                break
            if self.appear_then_click(WEEKLY_PACKAGE_CLAIM_BUTTON,interval=0):
                continue
            if self.appear_then_click(WEEKLY_PACKAGE_BUTTON,interval=1):
                continue
        self.ui_goto_main()
