

from module.ocr.ocr import DigitCounter
from tasks.activity.assets.assets_activity import ACTIVITY_CHECK
from tasks.freebies.assets.assets_freebies_monthly_sign_in import *
from tasks.activity.draglist import ACTIVITY_TAB_LIST
from tasks.activity.keyword import  MeiYueQianDaoKeyword
from tasks.base.page import  page_activity
from tasks.base.ui import UI
from module.base.timer import Timer


class MonthlySignIn(UI):
    def handle_monthly_sign_in(self):
        if self.config.stored.MonthlySignInFinishCount.is_expired():
            self.config.stored.MonthlySignInFinishCount.clear()
        if self.config.stored.MonthlySignInFinishCount.is_full():
            return True
        self.device.click_record_clear()
        self.ui_ensure(page_activity)
        ACTIVITY_TAB_LIST.search_rows(main=self,keyword=MeiYueQianDaoKeyword)
        ocr=DigitCounter(SIGN_IN_PROGRESS)
        click_interval=Timer(1).start()
        for _ in self.loop():
            if self.appear(MONTHLY_SIGN_IN_TITLE_HAVE_CLAIM):
                break
            if self.appear_then_click(MONTHLY_SIGN_IN_BUTTON,interval=0):
                continue
            current,remain,total=ocr.ocr_single_line(self.device.image)
            if remain==0 and total!=0:
                if click_interval.reached():
                    self.device.click(SIGN_IN_PROGRESS)
                    click_interval.reset()
                continue
            if self.appear(MONTHLY_SIGN_IN_HAVE_DONE):
                break
        self.ui_goto_main()
        self.config.stored.MailRewardFinishCount.add()





