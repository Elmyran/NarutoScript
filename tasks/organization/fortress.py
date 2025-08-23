import time

from module.base.timer import Timer
from module.base.utils import random_rectangle_point, ensure_int
from module.exception import GameStuckError
from module.logger import logger
from module.ocr.ocr import Digit
from tasks.base.assets.assets_base_move import CHOOSE_RIGHT
from tasks.base.assets.assets_base_skill import *
from tasks.base.page import page_main
from tasks.base.ui import UI
from tasks.duel.assets.assets_duel import DUEL_EXCEPTION, DUEL_FIGHT_SUCCESS, DUEL_FIGHT_FAIL, \
    DUEL_FIGHT_END
from tasks.organization.assets.assets_organization_fortress import ORGANIZATION_ENTER, ORGANIZATION_MAIN_PAGE, \
    ORGANIZATION_GOTO_FORTRESS, FORTRESS_LOCAL_SELECT, FORTRESS_FIRE, FORTRESS_ENTER_CONFIRM, FORTRESS_PAGE, \
    FORTRESS_MATCHING, FORTRESS_ROUND_SWITCH, FORTRESS_SCORE
from tasks.organization.assets.assets_organization_pray import ORGANIZATION_RED_DOT, MAIN_GOTO_ORGANIZATION, \
    ORGANIZATION_PANEL



class Fortress(UI):
    def handle_organization_fortress(self):
        self.device.click_record_clear()
        self.ui_ensure(page_main)
        self._organization_panel_enter()
        self._organization_goto_fortress()
        self._fortress_goto_fight()
        self.ui_goto_main()
    def _organization_panel_enter(self):
        self.device.swipe([0, 322], [1280, 314])
        move = True
        time = Timer(10, count=10).start()
        m=2
        for _ in self.loop():
            ORGANIZATION_RED_DOT.load_search((200, 100, 1100, 400))
            if self.appear_then_click(ORGANIZATION_RED_DOT):
                continue
            MAIN_GOTO_ORGANIZATION.load_search((200, 100, 1100, 400))
            if MAIN_GOTO_ORGANIZATION.match_template(self.device.image,direct_match=True):
                move = False
                continue
            if self.appear(ORGANIZATION_MAIN_PAGE):
                break
            if self.appear(ORGANIZATION_PANEL):
                if self.appear(ORGANIZATION_ENTER):
                    self.device.click(ORGANIZATION_ENTER)
                continue
            if time.reached():
                if move and m%2==0:
                    self.device.swipe( [1200, 314],[0, 322])
                    time.reset()
                    m=m+1
                elif move and m%2==1:
                    self.device.swipe([0, 322], [1200, 314])
                    m=m+1
                    time.reset()
                elif m>5:
                    raise GameStuckError("Organization Pray Stucked")
        logger.info(f"Organization Panel entered")

    def _organization_goto_fortress(self):
        for  _ in self.loop():
            if self.appear(FORTRESS_PAGE):
                break
            if self.appear(FORTRESS_ENTER_CONFIRM):
                self.device.click(FORTRESS_ENTER_CONFIRM)
                continue
            if self.appear(FORTRESS_FIRE):
                self.device.click(FORTRESS_FIRE)
                continue
            if self.appear(FORTRESS_LOCAL_SELECT):
                self.device.click(FORTRESS_LOCAL_SELECT)
                continue
            if self.appear(ORGANIZATION_GOTO_FORTRESS):
                self.device.click(ORGANIZATION_GOTO_FORTRESS)
                continue
    def _fortress_goto_fight(self):
        self.device.screenshot()
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
                    self.device.long_click(CHOOSE_RIGHT,duration=2)
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
az=Fortress('alas',task='Alas')
az.ui_goto_main()




