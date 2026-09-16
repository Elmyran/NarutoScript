from tasks.activity.activity_keyword import WeiShouXunZongKeyword
from tasks.activity.assets.assets_activity_wei_shou_xun_zong_submit import SUBMIT_BUTTON, SUBMIT_END_CHECK
from tasks.activity.assets.assets_activity_wei_shou_xun_zong_claim import CLAIMABLE_CHECK, CLAIM_PAGE_BUTTON, CLAIM_PAGE_CHECK, CLAIM_BUTTON, CLAIM_END_CHECK
from tasks.base.page import page_activity
from tasks.activity.draglist import ACTIVITY_TAB_LIST
from tasks.base.ui import UI
from module.logger import logger
class WeiShouXunZong(UI):
    def run(self):
        logger.hr("尾兽寻踪",level=1)
        self.device.click_record_clear()
        self.ui_ensure(page_activity)
        ACTIVITY_TAB_LIST.search_rows(main=self,keyword=WeiShouXunZongKeyword)
        self.submit()
        self.claim()
        self.config.task_delay(server_update=True)
        self.config.task_stop()
    def submit(self):
        self.ui_click(click_button=SUBMIT_BUTTON,check_button=SUBMIT_END_CHECK)
    def claim(self):
        if self.appear(CLAIMABLE_CHECK):
            self.ui_click(click_button=CLAIM_PAGE_BUTTON,check_button=CLAIM_PAGE_CHECK)
            self.ui_click(click_button=CLAIM_BUTTON,check_button=CLAIM_END_CHECK,retry_wait=2)
if __name__ == '__main__':
    ns=WeiShouXunZong('ns',task='Alas')
    ns.device.screenshot()
    ns.run()
