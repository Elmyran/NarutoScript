from itertools import count
from module.base.timer import Timer
from module.logger.logger import logger

from tasks.base.page import page_main, page_zhaocai
from tasks.base.ui import UI
from tasks.zhaocai.assets.assets_zhaocai import ZHAO_CAI_RED_DOT, ZHAO_CAI_FREE, ZHAO_CAI_PAIED
from tasks.zhaocai.free import ZhaoCaiFree


class ZhaoCai(UI):
    def run(self):
        if self.config.ZhaoCai_ZhaoCaiFree:
            ZhaoCaiFree(self.config,self.device).handle_zhao_cai()

        self.config.task_delay(server_update=True)
        self.config.task_stop()



