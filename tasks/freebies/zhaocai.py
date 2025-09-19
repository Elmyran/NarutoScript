from module.exception import GameStuckError
from tasks.base.page import  page_zhaocai
from tasks.base.ui import UI
from tasks.freebies.assets.assets_freebies_zhaocai import ZHAO_CAI_RED_DOT, ZHAO_CAI_FREE, ZHAO_CAI_PAIED, ZHAO_CAI_CHECK
from module.logger.logger import logger
from module.base.timer import Timer

class ZhaoCaiFree(UI):
    def handle_zhao_cai(self):
        if self.config.stored.ZhaoCaiFinishCount.is_expired():
            self.config.stored.ZhaoCaiFinishCount.clear()
        if self.config.stored.ZhaoCaiFinishCount.is_full():
            return True
        self.device.click_record_clear()
        self.ui_ensure(page_zhaocai)
        self.free_zhao_cai()
        self.ui_goto_main()
        self.config.stored.ZhaoCaiFinishCount.add()


    def free_zhao_cai(self):
        time=Timer(20,count=20).start()
        for _ in self.loop():
            if time.reached():
                logger.warning("ZhaoCai timeout")
                raise GameStuckError("ZhaoCai timeout after 20 seconds")
            if self.appear_then_click(ZHAO_CAI_FREE,interval=1):
                continue
            if self.appear(ZHAO_CAI_PAIED):
                self.ui_goto_main()
                break


    def _enter_zhao_cai(self):
        for _ in self.loop():
            if self.appear(ZHAO_CAI_RED_DOT,interval=1):
                self.device.click(ZHAO_CAI_RED_DOT)
                continue
            if self.appear(ZHAO_CAI_CHECK):
                break

