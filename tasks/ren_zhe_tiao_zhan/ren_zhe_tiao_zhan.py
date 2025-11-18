from module.base.base import ModuleBase
from module.logger import logger


class RenZheTiaoZhan(ModuleBase):
    def run(self):
        pre_count=self.config.stored.MiJingCount.value
        from tasks.ren_zhe_tiao_zhan.mi_jing import MiJing
        MiJing(config=self.config,device=self.device).run()
        if (self.config.stored.MiJingCount.value >= 9 > pre_count) or (
                self.config.stored.MiJingCount.value >= 15 > pre_count) or (
                self.config.stored.MiJingCount.value >= 21 > pre_count):
            from tasks.ren_zhe_tiao_zhan.mi_jing_box_claim import MiJingBoxClaim
            MiJingBoxClaim(config=self.config,device=self.device).handle_mi_jing_box_claim()
        self.config.task_delay(server_update=True)
        self.config.task_stop()