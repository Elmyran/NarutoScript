from tasks.activity.activity_keyword import YiLeWaiMaiKeyword
from tasks.activity.assets.assets_activity import *
from tasks.activity.draglist import ACTIVITY_TAB_LIST
from tasks.freebies.assets.assets_freebies_yi_le_la_mian import *
from tasks.base.page import page_activity
from tasks.base.ui import UI
from datetime import datetime
from module.logger import logger

class YiLeLaMian(UI):
    def handle_la_mian(self):
        now = datetime.now() 
        if now.hour<11:
            logger.info(f'Not 11am yet, skip claim')
            return False
        if self.config.stored.YiLeLaMianFinishCount.is_expired():
            self.config.stored.YiLeLaMianFinishCount.clear()
        if self.config.stored.YiLeLaMianFinishCount.is_full():
            return True
        self._claim()
        self.config.stored.YiLeLaMianFinishCount.add()
        return True
    def _claim(self):
        self.ui_ensure(page_activity)
        ACTIVITY_TAB_LIST.search_rows(main=self,keyword=YiLeWaiMaiKeyword)
        for _ in  self.loop():
            if self.is_claim_done():
                break
            if self.appear_then_click(RAMEN_CLAIM,interval=1):
                continue
        return True
    def is_claim_done(self):
        return self.appear(RAMEN_CLAIM_DONE_1) and self.appear(RAMEN_CLAIM_DONE_2) and self.appear(RAMEN_CLAIM_DONE_3)




