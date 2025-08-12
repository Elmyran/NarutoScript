import re

from module.base.base import ModuleBase
from module.base.timer import Timer
from module.logger import logger













class DataUpdate(ModuleBase):
    def _get_data(self):
        """
        Page:
            in: page_item, KEYWORDS_ITEM_TAB.UpgradeMaterials
        """
        credit, jade = 0, 0
        logger.attr('Credit', credit)
        logger.attr('StellarJade', jade)
        return credit, jade

    def _get_relic(self):
        """
        Page:
            in: page_item, KEYWORDS_ITEM_TAB.Relics
        """
        relic = 0
        logger.attr('Relic', relic)
        return relic

    def run(self):
        # 跳过实际的数据获取，直接设置空值
        credit, jade, relic = 0, 0, 0

        with self.config.multi_set():
            self.config.stored.Credit.value = credit
            self.config.stored.StallerJade.value = jade
            self.config.stored.Relic.value = relic
            self.config.task_delay(server_update=True)
