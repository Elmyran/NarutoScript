from tasks.base.ui import UI
from tasks.trail.survival_trail import SurvivalTrail


class Survival(UI):
    def run(self):
        SurvivalTrail(self.config,self.device).handle_survival_trail()
        self.config.task_delay(server_update=True)
        self.config.task_stop()

