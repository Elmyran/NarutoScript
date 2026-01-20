from module.base.timer import Timer
from module.exception import GameStuckError
from module.logger import logger
from module.ocr.ocr import  DigitCounter
from tasks.base.assets.assets_base_code_second import CODE_SECOND_PASSWORD
from tasks.base.page import page_squad_help_battle,page_squad
from tasks.base.taskui import TaskUI
from tasks.combat.assets.assets_combat_support import  COMBAT_SUPPORT_SAME_CHARACTER_NOTIFY
from tasks.combat.support import SUPPORT_LIST
from tasks.squadraid.assets.assets_squadraid_fight import *
from tasks.squadraid.ocr import SquadRaidOCR

class SquadRaidFight(TaskUI):
    def run(self):
        if self.config.stored.SquadRaidFinishedCount.is_expired():
            self.config.stored.SquadRaidFinishedCount.clear()
        if self.config.stored.SquadRaidFinishedCount.is_full():
            return True
        self.device.click_record_clear()
        self.handle_squad_raid()
        self.handle_squad_raid()
        self.config.stored.SquadRaidFinishedCount.add()
        
    def handle_squad_raid(self):
        self.ui_ensure(page_squad)
        if not self.have_sufficient_times():
            logger.info('SquadRaid Have Done')
            return False
        self._quadruple_reward()
        if self.config.SquadRaid_SquadRaidFight == 'SquadMatch':
            self._squad_raid_match()
        elif self.config.SquadRaid_SquadRaidFight == 'SquadSupport':
            self._squad_raid_support()
        try:
            self.device.stuck_timer=Timer(120,count=120).start()
            self.waiting_fight_end()
        finally:
            self.device.stuck_timer=Timer(60,count=60).start()
        return True
    def have_sufficient_times(self):
        ocr=SquadRaidOCR(SQUAD_RAID_TIMES_COUNTER)
        time=Timer(10,count=20).start()
        for _ in  self.loop():
            if time.reached():
                raise GameStuckError('SQUAD_RAID_REMAIN_TIMES DETECTED ERROR')
            current,remain,total=ocr.ocr_single_line(self.device.image)
            if current!=0 and total!=0:
                break
            if self.appear(SQUAD_RAID_HAVE_DONE):
                return False
        return True
    def _quadruple_reward(self):
        if self.config.SquadRaid_SquadQuadrupleReward:
            for _ in self.loop():
                if self.appear(SQUAD_RAID_QUADRUPLE_REWARD_CHECK):
                    break
                if self.appear_then_click(SQUAD_RAID_QUADRUPLE_REWARD_BUTTON,interval=1):
                    continue
        return True

    def _squad_raid_match(self):
        logger.info('SquadRaidMethod:Match')
        self.device.click_record_remove(HELP_BATTLE_START_FIGHT)
        self.device.click_record_remove(SQUAD_RAID_FIGHT_SUCCESS)
        for _ in self.loop():
            if self.appear(CODE_SECOND_PASSWORD):
                self.handle_second_password()
                continue
            if self.appear_then_click(SQUAD_RAID_FIGHT_CONFIRM,interval=1):
                continue
            if self.match_template_color(SQUAD_RAID_MATCH_BUTTON,interval=1):
                self.device.click(SQUAD_RAID_MATCH_BUTTON)
                continue
            if self.appear(SQUAD_RAID_FIGHTING):
                break
            if self.appear(SQUAD_RAID_FIGHT_SUCCESS):
                break
        
    def waiting_fight_end(self):
        for _ in self.loop():
            if self.appear(SQUAD_RAID_CHECK):
                break
            if self.appear_then_click(SQUAD_RAID_FIGHT_SUCCESS,interval=1):
                continue
        return True
    def _squad_raid_support(self):
        logger.info('SquadRaidMethod:Support')
        self.ui_ensure(page_squad_help_battle)
        SUPPORT_LIST.select_first_support_character(self)
        self._start_fight_with_support()
        return True

        
    def _start_fight_with_support(self):
        self.device.click_record_remove(HELP_BATTLE_START_FIGHT)
        self.device.click_record_remove(SQUAD_RAID_FIGHT_SUCCESS)
        for _ in self.loop():
            if self.appear(COMBAT_SUPPORT_SAME_CHARACTER_NOTIFY):
                SUPPORT_LIST.select_next_support_character(self)
            if self.appear(CODE_SECOND_PASSWORD):
                self.handle_second_password()
                continue
            if self.appear_then_click(SQUAD_RAID_FIGHT_CONFIRM,interval=1):
                continue
            if self.appear_then_click(HELP_BATTLE_START_FIGHT,interval=1):
                continue
            if self.appear(SQUAD_RAID_FIGHTING):
                break
            if self.appear_then_click(SQUAD_RAID_FIGHT_SUCCESS,interval=1):
                continue
            if self.appear(SQUAD_RAID_CHECK):
                return True
        return True



