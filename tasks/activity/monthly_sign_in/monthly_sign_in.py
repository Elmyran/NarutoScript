
from module.ocr.ocr import DigitCounter
from tasks.activity.assets.assets_activity_monthly_sign_in import MONTHLY_SIGN_IN_BUTTON, \
    MONTHLY_SIGN_IN_HAVE_DONE, SIGN_IN_PROGRESS
from tasks.activity.draglist import ACTIVITY_TAB_LIST
from tasks.activity.keyword import MonthlySignInKeyword
from tasks.base.page import page_main, page_activity
from tasks.base.ui import UI


class MonthlySignIn(UI):
    def run(self):
        self.handle_monthly_sign_in()
        self.config.task_delay(server_update=True)
        self.config.task_stop()
    def handle_monthly_sign_in(self):
        self.device.click_record_clear()
        self.ui_ensure(page_activity)
        ACTIVITY_TAB_LIST.search_rows(main=self,keyword=MonthlySignInKeyword)
        for _ in self.loop():
            ocr=DigitCounter(SIGN_IN_PROGRESS)
            current,remain,total=ocr.ocr_single_line(self.device.image)
            if remain==0 and total!=0:
                self.device.click(SIGN_IN_PROGRESS)
            if self.appear(MONTHLY_SIGN_IN_HAVE_DONE):
                break
            if self.appear_then_click(MONTHLY_SIGN_IN_BUTTON,interval=0):
                continue
        self.ui_goto_main()






