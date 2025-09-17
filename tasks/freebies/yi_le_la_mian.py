from module.base.timer import Timer
from tasks.activity.assets.assets_activity import *
from tasks.freebies.assets.assets_freebies_yi_le_la_mian import *
from tasks.base.page import page_activity
from tasks.base.ui import UI


class YiLeLaMian(UI):
    def handle_la_mian(self):
        self.ui_ensure(page_activity)
        time=Timer(10,20).start()
        for _ in  self.loop():
            if time.reached():
                break
            REMEN_CLAIM_DONE.load_search(ACTIVITY_DETAIL_AREA.area)
            res=REMEN_CLAIM_DONE.match_multi_template(self.device.image,similarity=0.9)
            if res and len(res)==3:
                break
            if self.appear_then_click(RAMEN_CLAIM,interval=1):
                continue
        self.ui_goto_main()



