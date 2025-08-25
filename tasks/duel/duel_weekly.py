import time

from module.base.timer import Timer
from module.base.utils import random_rectangle_point, ensure_int
from module.exception import GameStuckError
from module.logger import logger
from module.ocr.ocr import Digit
from tasks.base.assets.assets_base_skill import *
from tasks.base.page import page_main, page_ninjutsu
from tasks.base.ui import UI
from tasks.duel.assets.assets_duel import *


class DuelWeekly(UI):
    def handle_duel_weekly(self):
        self.device.click_record_clear()
        self.device.stuck_record_clear()
        self.ui_ensure(page_main)
        self.swipe_and_appear_then_click(DUEL_CHECK,MAIN_GOTO_DUEL,left=True)
        self.ui_ensure(page_ninjutsu)
        #上一局输赢
        success=True
        for _ in self.loop():
            #获胜则检查胜场
            if success:
                end_or_not=self._duel_task_detect()
                if end_or_not==False:
                    res=self.start_fight()
                    if res=='FIGHT_SUCCESS':
                        success=True
                    elif res=='FIGHT_FAIL':
                        success=False
                else:
                    break
            else:
                #输了则继续战斗
                self.start_fight()
                res=self.start_fight()
                if res=='FIGHT_SUCCESS':
                    success=True
                elif res=='FIGHT_FAIL':
                    success=False


    def _duel_task_detect(self):
        self.device.click_record_clear()
        self.device.stuck_record_clear()
        self.config.stored.CurrentVictoryCount.total=self.config.Duel_TargetVictoryNumber
        time=Timer(30, count=30).start()
        #进入任务面板
        for _ in self.loop():
            if time.reached():
                raise GameStuckError(' enter duel task stuck')
            if self.appear(DUEL_TASK_PANEL):
                break
            if self.appear(DUEL_IS_IN_FIGHT):
                return False
            if self.appear_then_click(DUEL_TASK,interval=1):
                continue
        for _ in self.loop():
            if time.reached():
                raise GameStuckError(' duel task detected stuck')
            ocr=Digit(DUEL_TASK_WINS_NUMBER)
            res=ocr.ocr_single_line(self.device.image)
            if res is not None and res!=0:
                self.config.stored.CurrentVictoryCount.value=res
                target=self.config.Duel_TargetVictoryNumber
                if res < target:
                    self.appear_then_click(DUEL_TASK_PANEL)
                    return False
                elif res<10:
                    return False
                else:
                    self._weekly_victory_reward_claim()
                    break
        return True
    def _weekly_victory_reward_claim(self):
        self.device.click_record_clear()
        self.device.stuck_record_clear()
        time=Timer(20,30).start()
        for _ in self.loop():
            if time.reached():
                break
            res=DUEL_TASK_WEEKLY_REWARD_HAVE_CLAIMED.match_multi_template(self.device.image)
            if res and len(res)==4:
                logger.info('DUEL_TASK_WEEKLY_REWARD HAVE CLAIMED')
                break
            if self.appear_then_click(DUEL_TASK_WEEKLY_REWARD,similarity=0.88,interval=0.5):
                continue

    def start_fight(self):
        self.device.click_record_clear()
        self.device.stuck_record_clear()
        for _ in self.loop():
            if self.appear(DUEL_ROUND_SWITCH):
                break
            if self.appear(DUEL_IS_IN_FIGHT):
                break
            if self.appear(DUEL_TASK_DELAY):
                return 'Delay 5 Minute'
            if self.appear(DUEL_IS_IN_MATCHING):
                continue
            if self.appear_then_click(DUEL_TASK_PANEL,interval=1):
                continue

            if self.appear_then_click(DUEL_START_FIGHT,similarity=0.95,interval=2):
                continue
        buttons = [CHARACTER_TI_SHEN,CHARACTER_SKILL_1, CHARACTER_SKILL_2, CHARACTER_SKILL_3, CHARACTER_PSYCHIC, CHARACTER_SECRET_SCROLL]
        for _ in self.loop():
            self.device.click_record_clear()
            self.device.stuck_record_clear()
            if self.appear_then_click(DUEL_EXCEPTION):
                self.config.stored.CurrentVictoryCount.add(1)
                print(f'find a exception')
                return 'FIGHT_SUCCESS'
            if self.appear_then_click(DUEL_FIGHT_FAIL):
                print(f'Fight_FAIL')
                return 'FIGHT_FAIL'
            if self.appear_then_click(DUEL_FIGHT_SUCCESS):
                self.config.stored.CurrentVictoryCount.add(1)
                print(f'FIGHT_SUCCESS')
                return 'FIGHT_SUCCESS'
            if self.appear(DUEL_ROUND_SWITCH):
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