from datetime import datetime

from module.base.timer import Timer
from module.config.utils import get_nearest_weekday_date, get_server_weekday, server_time_offset
from module.exception import GameStuckError
from module.logger import logger
from module.ocr.ocr import Digit
from tasks.base.assets.assets_base_code_second import CODE_SECOND_PASSWORD
from tasks.base.page import page_main
from tasks.base.task_tab.draglist import TASK_TAB_LIST
from tasks.base.task_tab.keyword import OrganizationKeyword
from tasks.organization.assets.assets_organization import *
from tasks.organization.assets.assets_organization_pan_ren import *
from tasks.organization.assets.assets_organization_pray import *
from tasks.ren_zhe_tiao_zhan.joystick import GameControl
class OrganizationPanRen(GameControl):
    def run(self):
        next_wednesday = get_nearest_weekday_date(2)
        next_saturday = get_nearest_weekday_date(5)
        wednesday_target_time = next_wednesday.replace(hour=21, minute=0, second=0, microsecond=0)
        saturday_target_time = next_saturday.replace(hour=20, minute=0, second=0, microsecond=0)
        if self.config.stored.PanRenFinishCount.is_expired():
            self.config.stored.PanRenFinishCount.clear()
        if self.config.stored.PanRenFinishCount.is_full():
            self.config.task_delay(target=[wednesday_target_time, saturday_target_time])
            self.config.task_stop()
            return
        if not self._check_time():
            self.config.task_delay(target=[wednesday_target_time, saturday_target_time])
            self.config.task_stop()
            return
        self.handle_organization_pan_ren()
        self.config.stored.PanRenFinishCount.add()
        self.config.task_delay(target=[wednesday_target_time, saturday_target_time])
        self.config.task_stop()
    def _check_time(self):
        server_weekday = get_server_weekday()
        diff = server_time_offset()
        server_now = datetime.now() - diff
        current_hour = server_now.hour
        if server_weekday == 2:  # Wednesday
            if not (21 <= current_hour < 22):
                logger.info(f'Not in Wednesday time  21-22 (current hour: {current_hour}), task will stop')
                return False
        elif server_weekday == 5:  # Saturday
            if not (20 <= current_hour < 21):
                logger.info(f'Not in Saturday time  20-21 (current hour: {current_hour}), task will stop')
                return False
        else:
            logger.info(f'Not Wednesday Or Saturday (current: {server_weekday}), task will stop')
            return False
        return True
    def handle_organization_pan_ren(self):
        self.device.click_record_clear()
        self.device.stuck_record_clear()
        self.ui_ensure(page_main)
        if not TASK_TAB_LIST.search_rows(main=self,keyword=OrganizationKeyword):
            raise GameStuckError(' Organization Not Found')
        self._organization_enter()
        self.device.stuck_timer = Timer(420, count=420).start()
        try:
            self._wait_pan_ren_start()
        finally:
            self.device.stuck_timer = Timer(60, count=60).start()
        self._pan_ren_goto_fight()
        self._start_auto_fight()
        self.device.screenshot_interval_set(1)
        self.device.stuck_timer=Timer(120, count=120).start()
        try:
            self._check_credit()
        finally:
            self.device.screenshot_interval_set()
            self.device.stuck_timer=Timer(60, count=60).start()
        self.ui_goto_main()

    def _organization_enter(self):
        time = Timer(10, count=10).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError("Organization Page Enter Stucked")
            if self.appear_then_click(ORGANIZATION_PANEL_GOTO_PAGE,interval=0):
                continue
            if self.appear(ORGANIZATION):
                return True

    def _wait_pan_ren_start(self):
        for _ in self.loop():
            ORGANIZATION_GOTO_PAN_REN.load_search((0,0,1280,720))
            if self.appear(ORGANIZATION_GOTO_PAN_REN):
                self.stop_movement()
                break
            if self.appear(ORGANIZATION):
                self.move_to_direction(270,0.2)
        time=Timer(30).start()
        for _ in self.loop():
            if time.reached():
                logger.info("Waiting for Pan Ren to start")
                time.reset()
            PAN_REN_HAVE_START.load_search((0,0,1280,720))
            if self.appear(PAN_REN_HAVE_START):
                break
    def _pan_ren_goto_fight(self):
        for _ in self.loop():
            if self.appear(PAN_REN_AUTO_FIGHT):
                break
            if self.appear_then_click(CHARACTER_SELECT_CONFIRM,interval=0):
                continue
            if self.appear_then_click(PAN_REN_JOIN_BUTTON,interval=0):
                continue
            ORGANIZATION_GOTO_PAN_REN.load_search((0, 0, 1280, 720))
            if self.appear_then_click(ORGANIZATION_GOTO_PAN_REN,interval=0):
                continue

    def _start_auto_fight(self):
        time=Timer(30, count=30).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError("Pan Ren Start Auto Fight Stuck")
            if self.appear(PAN_REN_AUTO_FIGHT_SUCCESS):
                break
            if self.appear_then_click(PAN_REN_AUTO_FIGHT_CONFIRM, interval=0):
                continue
            if self.appear(CODE_SECOND_PASSWORD):
                self.handle_second_password()
                continue
            if self.appear_then_click(PAN_REN_AUTO_FIGHT):
                continue
    def _check_credit(self):
        ocr=Digit(PAN_REN_CREDITS)
        target_credit = 45
        time=Timer(60).start()
        pre_credit=0
        for _ in self.loop():
            if time.reached():
                credit=ocr.ocr_single_line(self.device.image)
                logger.info(f'Current credit: {credit}')
                if credit > pre_credit:
                    pre_credit=credit
                    self.device.stuck_record_clear()
                if  credit>=target_credit:
                    logger.info(f'Target credit {target_credit} reached!')
                    break
                time.reset()












