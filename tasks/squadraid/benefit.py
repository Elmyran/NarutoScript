from module.base.timer import Timer
from module.exception import GameStuckError

from tasks.base.page import page_squad_help_battle_mine
from tasks.base.ui import UI
from tasks.squadraid.assets.assets_squadraid_benefit import  *
from tasks.squadraid.assets.assets_squadraid_fight import *

class HelpBattleBenefit(UI):
    def handle_help_battle_benefit(self):
        self.device.click_record_clear()
        time=Timer(10,count=20).start()
        for _ in self.loop():
            if time.reached():
                break
            if self.appear(SQUAD_GOTO_HELP_BATTLE):
                self.device.click(SQUAD_GOTO_HELP_BATTLE)
                continue
            if self.appear(HELP_BATTLE_GOTO_MINE,interval=1):
                self.device.click(HELP_BATTLE_GOTO_MINE)
                continue

            if self.appear(HELP_BATTLE_MINE_BENEFIT_CLAIM_DONE):
                break
            if self.appear(HELP_BATTLE_MINE_BENEFIT_CLAIM):
                self.device.click(HELP_BATTLE_MINE_BENEFIT_CLAIM)
                continue

        return True
