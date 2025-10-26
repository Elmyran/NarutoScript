from module.base.timer import Timer
from module.exception import GameStuckError
from module.ocr.ocr import  DigitCounter
from tasks.base.page import page_squad_help_battle,page_squad
from tasks.base.taskui import TaskUI
from tasks.combat.assets.assets_combat_support import  COMBAT_SUPPORT_SAME_CHARACTER_NOTIFY
from tasks.combat.support import SUPPORT_LIST
from tasks.squadraid.assets.assets_squadraid_fight import *
from tasks.squadraid.benefit import HelpBattleBenefit

class SquadRaidFight(TaskUI):
    def handle_squad_raid(self):
        self.device.click_record_clear()
        self.ui_ensure(page_squad)
        for _ in self.loop():
           if not self._squad_raid_fight():
               break
        if self.config.SquadRaid_SquadRaidBenefit:
            HelpBattleBenefit(self.config,self.device).handle_help_battle_benefit()

    def _squad_raid_fight(self):
        time=Timer(10,count=20).start()
        for _ in  self.loop():
            if time.reached():
                raise GameStuckError('SQUAD_RAID_REMAIN_TIMES DETECTED ERROR')
            ocr=DigitCounter(SQUAD_RAID_TIMES_COUNTER)
            current,remain,total=ocr.ocr_single_line(self.device.image)
            if remain!=2 and total!=0:
                break
            if self.appear(SQUAD_RAID_HAVE_DONE):
                 return False
        self._help_battle_select()
        self._start_fight()

        return True
    def _help_battle_select(self):
        self.ui_ensure(page_squad_help_battle)
        SUPPORT_LIST.select_first_support_character(self)
    def _start_fight(self):
        self.device.click_record_remove(HELP_BATTLE_START_FIGHT)
        self.device.click_record_remove(SQUAD_RAID_FIGHT_SUCCESS)
        time=Timer(60,8).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError("SQUAD_RAID_FIGHT_STUCK")
            if self.appear(COMBAT_SUPPORT_SAME_CHARACTER_NOTIFY):
                SUPPORT_LIST.select_next_support_character(self)
            if self.appear_then_click(HELP_BATTLE_START_FIGHT,interval=1):
                continue
            if self.appear(SQUAD_RAID_FIGHTING):
                continue
            if self.appear_then_click(SQUAD_RAID_FIGHT_SUCCESS,interval=1):
                continue
            if self.appear(SQUAD_RAID_CHECK):
                return True


        return True




