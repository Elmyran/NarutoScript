
import time
from datetime import datetime

from module.base.timer import Timer
from module.base.utils import random_rectangle_point, ensure_int
from module.config.utils import get_nearest_weekday_date, get_server_weekday, server_time_offset
from module.exception import GameStuckError
from module.logger import logger
from module.ocr.ocr import Digit
from tasks.base.assets.assets_base_move import CHOOSE_RIGHT
from tasks.base.assets.assets_base_skill import *
from tasks.base.page import page_main, page_fortress_select
from tasks.base.task_tab.draglist import TASK_TAB_LIST
from tasks.base.task_tab.task_keyword import OrganizationKeyword

from tasks.duel.assets.assets_duel import DUEL_EXCEPTION, DUEL_FIGHT_SUCCESS, DUEL_FIGHT_FAIL, \
    DUEL_FIGHT_END
from tasks.organization.assets.assets_organization_fortress import *
from tasks.organization.assets.assets_organization_pray import  ORGANIZATION_PANEL
from tasks.ren_zhe_tiao_zhan.joystick import GameControl


class Fortress(GameControl):
    def run(self):
        next_saturday = get_nearest_weekday_date(5)
        saturday_8pm = next_saturday.replace(hour=20, minute=0, second=0, microsecond=0)
        diff = server_time_offset()
        server_now = datetime.now() - diff
        if server_now.weekday() == 5 and server_now.hour < 20:
            saturday_8pm=server_now.replace(hour=20, minute=0, second=0, microsecond=0)
        if not self._check_time():
            self.config.task_delay(target=saturday_8pm)
            self.config.task_stop()
            return
        self.handle_organization_fortress()
        self.config.task_delay(target=saturday_8pm)
        self.config.task_call('PanRen')
        self.config.task_stop()
    def _check_time(self):
        server_weekday = get_server_weekday()
        diff = server_time_offset()
        server_now = datetime.now() - diff
        current_hour = server_now.hour
        current_minute = server_now.minute
        if server_weekday == 5:
            if not (current_hour==20 and  30>current_minute>=0):
                logger.info(f'Not in Saturday time  20:00 - 20:30 (current hour: {current_hour}), task will stop')
                return False
        else:
            logger.info(f'Not  Saturday (current: {server_weekday}), task will stop')
            return False
        return True
    def handle_organization_fortress(self):
        self.device.click_record_clear()
        self.ui_ensure(page_main)
        if not TASK_TAB_LIST.search_rows(main=self,keyword=OrganizationKeyword):
            raise GameStuckError(' Organization Not Found')
        self._organization_page_enter()
        self.ui_ensure(page_fortress_select)
        self._fortress_select()
        self._fortress_goto_fight()
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

        logger.info(f"Organization Page entered")
    def _fortress_select(self):
        for  _ in self.loop():
            if self.appear(FORTRESS_PAGE):
                break
            if self.appear(FORTRESS_ENTER_CONFIRM):
                self.device.click(FORTRESS_ENTER_CONFIRM)
                continue
            if self.appear(FORTRESS_FIRE):
                self.device.click(FORTRESS_FIRE)
                continue

    def _fortress_goto_fight(self):
        ocr=Digit(FORTRESS_SCORE)
        for _ in self.loop():
            self.device.click_record_clear()
            self.device.stuck_record_clear()
            if self.appear(FORTRESS_MATCHING):
                continue
            if self.appear(FORTRESS_PAGE):
                score=ocr.ocr_single_line(self.device.image)
                if score and score>=40:
                    break
                else:
                    self.move_to_direction(90,2)
            if self.appear(FORTRESS_ROUND_SWITCH):
                self._start_fight()

    def _start_fight(self):
        buttons = [CHARACTER_TI_SHEN,CHARACTER_SKILL_1, CHARACTER_SKILL_2, CHARACTER_SKILL_3, CHARACTER_PSYCHIC, CHARACTER_SECRET_SCROLL]
        for _ in self.loop():
            self.device.click_record_clear()
            if self.appear_then_click(DUEL_EXCEPTION):
                print(f'find a exception')
                return 'FIGHT_SUCCESS'
            if self.appear_then_click(DUEL_FIGHT_FAIL):
                print(f'Fight_FAIL')
                return 'FIGHT_FAIL'
            if self.appear_then_click(DUEL_FIGHT_SUCCESS):
                print(f'FIGHT_SUCCESS')
                return 'FIGHT_SUCCESS'
            if self.appear(FORTRESS_ROUND_SWITCH):
                print('ROUND SWITCH')
                try:
                    self.click_buttons_until_end(CHARACTER_ATTACK,buttons,DUEL_FIGHT_END)
                finally:
                    self.device.stuck_record_clear()
                    self.device.click_record_clear()
    def click_buttons_until_end(self, attack_button, other_buttons, fail_check, timeout=390, check_interval=0.5):
        """
        普通攻击按钮一直快速点击，其他按钮轮询点击，减少失败检测频率提升流畅度。

        Args:
            attack_button: ClickButton 对象，普通攻击按钮
            other_buttons: list，其他按钮 ClickButton 列表
            fail_check: 失败检测标识
            timeout (int): 超时时间（秒）
            check_interval (float): 失败检测间隔（秒）
        """

        start_time = time.time()
        last_check = time.time()
        idx = 0
        other_count = len(other_buttons)

        original=self.device.stuck_timer
        self.device.stuck_timer=Timer(100,100).start()
        while True:
            self.device.click_record_clear()
            self.device.stuck_record_clear()
            # 超时退出
            if time.time() - start_time > timeout:
                print(f"超时 {timeout} 秒，停止点击。")
                break

            # 每隔 check_interval 检测失败条件，减少阻塞
            if time.time() - last_check > check_interval:
                self.device.screenshot()
                if self.appear(fail_check):
                    print(f"检测到 {fail_check}，停止点击。")
                    break
                if self.appear(DUEL_EXCEPTION):
                    print(f"检测到 {DUEL_EXCEPTION}，停止点击。")
                    break
                last_check = time.time()

            # 先点击普通攻击按钮，快速无间断
            x, y = random_rectangle_point(attack_button.button)
            x, y = ensure_int(x, y)
            self.device.click_maatouch(x, y)
            # 每循环一次点击一个其他按钮，轮询切换
            if other_count > 0:
                button = other_buttons[idx]
                x, y = random_rectangle_point(button.button)
                x, y = ensure_int(x, y)
                self.device.click_maatouch(x, y)
                idx = (idx + 1) % other_count
        self.device.stuck_record_clear()
        self.device.stuck_timer=original





