from tasks.base.page import  page_chongzhi
from tasks.base.ui import UI
from tasks.freebies.assets.assets_freebies_weekly_package import *


class WeeklyPackage(UI):
    def handle_weekly_package(self):
        if self.config.stored.PrivilegPackageFinishCount.is_expired():
            self.config.stored.PrivilegPackageFinishCount.clear()
        if self.config.stored.PrivilegPackageFinishCount.is_full():
            return True
        self.ui_ensure(page_chongzhi)
        for _ in self.loop():
            if self.match_template_color(WEEKLY_PACKAGE_HAVE_CLAIM_DONE):
                break
            if self.appear_then_click(WEEKLY_PACKAGE_CLAIM_BUTTON,interval=1):
                continue
            if self.match_template_color(WEEKLY_PACKAGE_BUTTON,interval=1):
                self.device.click(WEEKLY_PACKAGE_BUTTON)
                continue
        self.ui_goto_main()
        self.config.stored.PrivilegPackageFinishCount.add()

