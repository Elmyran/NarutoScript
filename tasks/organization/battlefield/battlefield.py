
from module.base.timer import Timer
from module.config.utils import get_nearest_weekday_date, get_server_weekday, server_time_offset
from module.exception import GameStuckError
from module.logger import logger
from module.ocr.ocr import Digit
from tasks.base.assets.assets_base_character import *
from tasks.base.page import  page_character_select, page_battle_field_select, page_battle_field,page_manual
from tasks.base.task_tab.draglist import TASK_TAB_LIST
from tasks.base.task_tab.task_keyword import OrganizationKeyword
from tasks.base.ui import UI
import cv2
from tasks.organization.assets.assets_organization_battlefield import *
from tasks.organization.assets.assets_organization_fortress import ORGANIZATION_MAIN_PAGE, ORGANIZATION_ENTER
from tasks.organization.assets.assets_organization_pray import ORGANIZATION_PANEL
from tasks.organization.battlefield.detecor import CharacterCircleDetector
from tasks.organization.battlefield.switch import CHARACTER_TAB
from toolkit.Lib.datetime import datetime
from tasks.organization.battlefield.name_keywords import AccountNameKeyword
from tasks.duel.assets.assets_duel import DUEL_FIGHT_FAIL, DUEL_IS_IN_FIGHT

class BattleField(UI,CharacterCircleDetector):
    def run(self):
        diff = server_time_offset()
        server_now = datetime.now() - diff
        if server_now.weekday() == 2 and server_now.hour < 21:
            wednesday_9_pm = server_now.replace(hour=21, minute=0, second=0, microsecond=0)
        else:
            wednesday = get_nearest_weekday_date(2)
            wednesday_9_pm = wednesday.replace(hour=21, minute=0, second=0, microsecond=0)
        logger.info(wednesday_9_pm)
        if self.config.stored.BattleFieldFinishCount.is_expired():
            self.config.stored.BattleFieldFinishCount.clear()
        if self.config.stored.BattleFieldFinishCount.is_full():
            self.config.task_delay(target=wednesday_9_pm)
            self.config.task_stop()
            return False
        if not self._check_time():
            self.config.task_delay(target=wednesday_9_pm)
            self.config.task_stop()
            return False
        self.handle_battle_field()
        self.config.task_delay(target=wednesday_9_pm)
        self.config.task_call('PanRen')
        self.config.task_stop()
        return True

    def _check_time(self):
        server_weekday = get_server_weekday()
        diff = server_time_offset()
        server_now = datetime.now() - diff
        current_hour = server_now.hour
        current_minute = server_now.minute
        if server_weekday == 2:
            if not (current_hour==21 and  30>current_minute>=0):
                logger.info(f'Not in Wednesday time  21:00 - 21:30 (current hour: {current_hour}), task will stop')
                return False
        else:
            logger.info(f'Not Wednesday (current: {server_weekday}), task will stop')
            return False
        return True
    def handle_battle_field(self):
        self.ui_ensure(page_manual)
        TASK_TAB_LIST.search_rows(self,OrganizationKeyword)
        self.ui_ensure(page_battle_field_select)
        self._battle_field_type_select()
        self._character_select()
        self._handle_inspired()
        try:
            self.device.screenshot_interval_set(1)
            self.device.stuck_timer=Timer(1200,count=1200).start()
            self._check_state()
        finally:
            self.device.screenshot_interval_set()
            self.device.stuck_timer=Timer(60,count=60).start()
        self._handle_reward()
        self.ui_goto_main()

    def _organization_page_enter(self):
        time = Timer(10, count=10).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError("Organization Panel Goto Page Stuck")
            if self.appear(ORGANIZATION_MAIN_PAGE):
                break
            if self.appear(ORGANIZATION_PANEL):
                self.appear_then_click(ORGANIZATION_ENTER,interval=0)
                continue
    def _battle_field_type_select(self):
        if self.config.BattleField_Type=='天之战场':
            BATTLE_FIELD_TYPE=BATTLE_FIELD_SELECT_GOTO_TIAN
        else:
            BATTLE_FIELD_TYPE=BATTLE_FIELD_SELECT_GOTO_DI
        for _ in self.loop():
            if self.ui_page_appear(page_character_select):
                break
            if self.appear_then_click(BATTLE_FIELD_TYPE_CONFIRM,interval=1):
                continue
            if self.match_template_color(BATTLE_FIELD_TYPE,interval=1):
                self.device.click(BATTLE_FIELD_TYPE)
                continue

    def _character_select(self):
        CHARACTER_TAB.set('忍者',main=self)
        for _ in self.loop():
            if self.appear(CHARACTER_SELECTED):
                logger.info('Character Selected')
                break
            if self.appear(CHARACTER_UNSELECTED):
                self.device.click(CHARACTER_FIRST)
        CHARACTER_TAB.set('秘卷',main=self)
        for _ in  self.loop():
            if self.appear(MI_JUAN_SELECTED):
                break
            if self.appear(MI_JUAN_UNSELECTED):
                self.device.click(CHARACTER_FIRST)
        CHARACTER_TAB.set('通灵',main=self)
        for _ in self.loop():
            if self.appear(TONG_LING_FIRST_UNSELECTED):
                self.device.click(TONG_LING_FIRST)
            elif self.appear(TONG_LING_SECOND_UNSELECTED):
                self.device.click(TONG_LING_SECOND)
            elif self.appear(TONG_LING_THIRD_UNSELECTED):
                self.device.click(TONG_LING_THIRD)
            else: break
        for _ in self.loop():
            if self.ui_get_current_page()!=page_character_select:
                break
            if self.appear_then_click(CHARACTER_CONFIRM,interval=1):
                continue

    def _handle_inspired(self):
        time=Timer(3,6).start()
        for _ in self.loop():
            if time.reached():
                break
            if self.appear_then_click(INSPIRED_BUTTON,interval=1):
                continue

    def _check_state(self):
        account_name=self.config.stored.AccountName.value
        AccountNameKeyword.cn=account_name
        OCR=Digit(BATTLE_FIELD_CREDITS)
        ocr_interval=Timer(10).start()
        occupied=False

        for _ in self.loop():
            if self.appear(BATTLE_FIELD_FINISHED):
                break
            if self.appear(DUEL_IS_IN_FIGHT):
                continue
            if self.appear_then_click(DUEL_FIGHT_FAIL,interval=0):
                logger.info('Battle Field Fight End Detected')
                continue
            if self.appear_then_click(CHARACTER_CONFIRM,interval=0):
                logger.info('Character Confirm Detected')
                occupied=False
                continue
            if self.appear(BATTLE_FIELD_CHECK) and ocr_interval.reached():
                credits=OCR.ocr_single_line(self.device.image)
                logger.info(f'Credits: {credits}')
                if credits>1600:
                    logger.info('Credits reached 1600')
                    break
                ocr_interval.reset()
            if occupied==False and self.detect_character_circle(self.device.image):
                occupied=True
                logger.info('Occupied Detected')
                continue
            
            if occupied==False :
                image = cv2.bitwise_and(self.device.image, self.device.image, mask=self.mask_interact) 
                if BATTLE_FIELD_EMPTY.match_template(image,direct_match=True):
                    self.device.click(BATTLE_FIELD_EMPTY)
                    continue
            

    def _handle_reward(self):
        self.ui_ensure(page_battle_field)
        for _ in self.loop():
            if self.appear(BATTLE_FIELD_REWARD_CHECK):
                break
            if self.match_template_color(BATTLE_FIELD_CHECK,interval=1):
                self.device.click(BATTLE_FIELD_CHECK)
                continue
        for _ in self.loop():
            if self.appear_then_click(BATTLE_FIELD_REWARD_CLAIM_DONE,interval=1):
                break
            if self.appear_then_click(BATTLE_FIELD_REWARD_CONFIRM,interval=0.5):
                continue
            if self.appear_then_click(BATTLE_FIELD_REWARD_CLAIM_BUTTON,interval=1):
                continue


