from module.ocr.ocr import DigitCounter
from tasks.freebies.assets.assets_freebies_monthly_sign_in import *
from tasks.activity.draglist import ACTIVITY_TAB_LIST
from tasks.activity.activity_keyword import  MeiYueQianDaoKeyword
from tasks.base.page import  page_activity
from tasks.base.ui import UI
import re
from module.base.timer import Timer
from tasks.freebies.assets.assets_freebies_yi_le_la_mian import RAMEN_TAB_CHECK
class MonthlySignInOcr(DigitCounter):
    def after_process(self, result):
        result=result.replace('V','')
        result = re.sub(r'当月签到：', '', result)  
        result = re.sub(r'天$', '', result) 
        result = re.sub(r'^(\d)(\d{2})$', r'\1/\2', result)  
        result = re.sub(r'^(\d{2})(\d{2})$', r'\1/\2', result)  
        return result

class MonthlySignIn(UI):
    def handle_monthly_sign_in(self):
        if self.config.stored.MonthlySignInFinishCount.is_expired():
            self.config.stored.MonthlySignInFinishCount.clear()
        if self.config.stored.MonthlySignInFinishCount.is_full():
            return True
        self.device.click_record_clear()
        self.ui_ensure(page_activity)
        self.wait_until_stable(  
                    RAMEN_TAB_CHECK,  
                    timer=Timer(0, count=0),  
                    timeout=Timer(1.5, count=5)  
                )   
        ACTIVITY_TAB_LIST.search_rows(main=self,keyword=MeiYueQianDaoKeyword)
        self._sign_in()
        self._monthly_title_claim()
        self.config.stored.MonthlySignInFinishCount.add()
    def _sign_in(self):
        for _ in self.loop():
            if self.appear(MONTHLY_SIGN_IN_NOT_REACH_REQUIRE):
                break
            if self.appear(MONTHLY_SIGN_IN_HAVE_DONE):
                break
            if self.appear_then_click(MONTHLY_SIGN_IN_BUTTON,interval=1):
                continue
    def _monthly_title_claim(self):
        ocr=MonthlySignInOcr(SIGN_IN_PROGRESS)
        click_interval=Timer(1).start()
        for _ in self.loop():
            if self.appear(MONTHLY_SIGN_IN_TITLE_HAVE_CLAIM):
                break
            current,remain,total=ocr.ocr_single_line(self.device.image)
            if remain==0 and total!=0:
                if click_interval.reached():
                    self.device.click(SIGN_IN_PROGRESS)
                    click_interval.reset()
                continue
            elif remain!=0 and total!=0:
                break
if __name__ == '__main__':
    pass