from module.base.base import ModuleBase


class RenZheTiaoZhan(ModuleBase):
    def run(self):
        from tasks.ren_zhe_tiao_zhan.mi_jing import MiJing
        MiJing(config=self.config,device=self.device).handle_mi_jing()
        self.config.task_delay(server_update=True)
        self.config.task_stop()