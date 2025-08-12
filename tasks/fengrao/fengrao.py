from tasks.base.ui import UI
from tasks.fengrao.fight import FengRaoFight

class FengRao(UI):
    def run(self):
        FengRaoFight(self.config,self.device).handle_feng_rao()
        self.config.task_delay(server_update=True)
        self.config.task_stop()
