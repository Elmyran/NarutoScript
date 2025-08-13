from module.base.timer import Timer
from module.exception import GameStuckError
from module.ocr.ocr import DigitCounter
from tasks.activity.assets.assets_activity import ACTIVITY_LIST_AREA
from tasks.activity.assets.assets_activity_monthly_sign_in import ACTIVITY_GOTO_MONTHLY_SIGN_IN, MONTHLY_SIGN_IN_BUTTON, \
    MONTHLY_SIGN_IN_HAVE_DONE, SIGN_IN_PROGRESS
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
        self.device.swipe([89,680],[93,146])
        first=True
        time=Timer(10,20).start()
        for _ in self.loop():
            if time.reached():
                if first:
                    self.device.swipe([89,680],[93,146])
                    first=False
                    time.reset()
                    continue
                raise GameStuckError('Monthly sign in stuck')
            if self.appear(MONTHLY_SIGN_IN_BUTTON) or self.appear(MONTHLY_SIGN_IN_HAVE_DONE):
                break
            ACTIVITY_GOTO_MONTHLY_SIGN_IN.load_search(ACTIVITY_LIST_AREA.area)
            if self.appear_then_click(ACTIVITY_GOTO_MONTHLY_SIGN_IN, interval=0,similarity=0.9):
                continue
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






