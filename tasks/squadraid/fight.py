

from module.base.timer import Timer
from module.exception import GameStuckError
from module.ocr.ocr import  DigitCounter
from tasks.base.page import page_squad, page_squad_help_battle, page_main
from tasks.base.task_tab.draglist import TASK_TAB_LIST
from tasks.base.task_tab.task_keyword import SquadRaidKeyword
from tasks.base.ui import UI
from tasks.squadraid.assets.assets_squadraid_fight import *
from tasks.squadraid.benefit import HelpBattleBenefit

class SquadRaidFight(UI):
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
        time=Timer(10,count=20).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError("HELP_BATTLE_SELECT_STUCK")
            if self.appear_then_click(SQUAD_GOTO_HELP_BATTLE,interval=2):
                continue
            HELP_BATTLE_SELECTED.load_search(HELP_BATTLE_LIST.area)
            if HELP_BATTLE_SELECTED.match_template(self.device.image):
                break
            HELP_BATTLE_NOT_BE_SELECTED.load_search(HELP_BATTLE_LIST.area)
            wrong_buttons=HELP_BATTLE_NOT_BE_SELECTED.match_multi_template(self.device.image)
            if wrong_buttons and len(wrong_buttons)==5:
                self.device.swipe( [263,594],[270,182])
                time.reset()
                continue
            if self.appear_then_click(HELP_BATTLE_SELECT_BUTTON,interval=1):
                continue


    def _start_fight(self):
        self.device.click_record_remove(HELP_BATTLE_START_FIGHT)
        self.device.click_record_remove(SQUAD_RAID_FIGHT_SUCCESS)
        time=Timer(60,8).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError("SQUAD_RAID_FIGHT_STUCK")
            if self.appear_then_click(HELP_BATTLE_START_FIGHT,interval=0):
                continue
            if self.appear(SQUAD_RAID_FIGHTING):
                continue
            if self.appear_then_click(SQUAD_RAID_FIGHT_SUCCESS,interval=1):
                continue
            if self.appear(SQUAD_RAID_CHECK):
                return True


        return True




