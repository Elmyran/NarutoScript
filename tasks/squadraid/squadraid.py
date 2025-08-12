
from tasks.base.ui import UI

from tasks.squadraid.fight import SquadRaidFight

class SquadRaid(UI):
    def run(self):
        self.device.screenshot()
        if self.config.SquadRaid_SquadRaidFight:
            SquadRaidFight(self.config,self.device).handle_squad_raid()
        self.config.task_delay(server_update=True)
        self.config.task_stop()
