


from module.base.timer import Timer
from module.base.utils import random_rectangle_point, ensure_int
from module.exception import GameStuckError
from module.logger import logger
from module.ocr.digit import SimpleDigitOcr
from tasks.base.assets.assets_base_skill import *
from tasks.base.page import page_main
from tasks.base.ui import UI
from tasks.duel.assets.assets_duel import *
import time


class Duel(UI):
    def run(self):
        self.handle_duel()
        self.config.task_delay(server_update=True)
        self.config.task_stop()
    def handle_duel(self):
        self.device.click_record_clear()
        self.ui_ensure(page_main)
        self.swipe_and_appear_then_click(DUEL_CHECK,MAIN_GOTO_DUEL,left=True)
        self._enter_ninjutsu()
        weekly=False
        success=True
        while True:
            if success:
                if weekly and self.config.Duel_VictoryNumber<=20:
                    self.start_fight()
                    continue
                else:
                    res=self._duel_task_detect()
                    if res:
                        return
                    elif res=='VICTORY_NUMBER_NOT_ENOUGH':
                        weekly=True
                    else:
                        result=self.start_fight()
                        if result=='FIGHT_FAIL':
                            success=False
                            continue
                        elif result=='FIGHT_SUCCESS':
                            success=True
                            continue
            else:
                result=self.start_fight()
                if result=='FIGHT_FAIL':
                    success=False
                    continue
                elif result=='FIGHT_SUCCESS':
                    success=True
                    continue
    def _enter_ninjutsu(self):
        time=Timer(10, count=10).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError('ninjutsu enter stuck')
            if self.appear(DUEL_START_FIGHT,interval=1):
                break
            if self.appear(DUEL_IS_IN_FIGHT,interval=1):
                break
            if self.appear(DUEL_CHECK,interval=1):
                self.device.click(DUEL_CHECK)
                continue

    def _duel_task_detect(self):
        time=Timer(30, count=30).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError(' enter duel task stuck')
            if self.appear(DUEL_TASK_PANEL):
                break
            if self.appear(DUEL_IS_IN_FIGHT):
                return False
            if self.appear(DUEL_TASK,interval=1):
                self.device.click(DUEL_TASK)
                continue
        claim_time=Timer(4, count=5).start()
        first_reach=True
        second_reach=True
        have_recall_card=True
        for _ in self.loop():
            if claim_time.reached():
                if first_reach:
                    self.device.swipe([1002,508],[1002,58])
                    claim_time.reset()
                    first_reach=False
                elif second_reach:
                    self.device.swipe([1002,133],[1002,577])
                    claim_time.reset()
                    second_reach=False
                else: break
            if self.appear(DUEL_TASK_RECALLED_FAIL):
                have_recall_card=False
                self.device.click(DUEL_TASK_RECALLED_FAIL)
                continue
            if self.appear_then_click(DUEL_TASK_RECALLED_CONFIRM):
                continue
            if self.appear(DUEL_TASK_RECALLED_BUTTON) and have_recall_card:
                self.device.click(DUEL_TASK_RECALLED_BUTTON)
                continue
            if self.appear(DUEL_TASK_REWARD_CLAIM_BUTTON):
                self.device.click(DUEL_TASK_REWARD_CLAIM_BUTTON)
                continue
        time_search=Timer(3, count=3).start()
        first_reach=True
        second_reach=True
        for _ in self.loop():
            if time_search.reached():
                if first_reach:
                    self.device.swipe([1002,508],[1002,58])
                    time_search.reset()
                    first_reach=False
                elif second_reach:
                    self.device.swipe([1002,133],[1002,577])
                    claim_time.reset()
                    second_reach=False
                else: break
            if DUEL_TASK_NOT_ACHIEVED_BUTTON.match_template(self.device.image,direct_match=True):
                return False
        for _ in self.loop():
            if time.reached():
                raise GameStuckError(' duel task detected stuck')
            ocr=SimpleDigitOcr()
            res=ocr.extract_digit_simple(self.device.image,DUEL_TASK_WINS_NUMBER)
            if res is not None:
                self.config.Duel_VictoryNumber=res
                if res < 20:
                    self.appear_then_click(DUEL_TASK_PANEL)
                    return 'VICTORY_NUMBER_NOT_ENOUGH'
                else:
                    self._weekly_victory_reward_claim()
                    return True
        return False

    def start_fight(self):
        self.device.click_record_clear()
        for _ in self.loop():
            if self.appear(DUEL_ROUND_SWITCH):
                break
            if self.appear(DUEL_IS_IN_FIGHT):
                break
            if self.appear_then_click(DUEL_TASK_PANEL):
                continue
            if self.appear_then_click(DUEL_START_FIGHT):
                continue

        buttons = [CHARACTER_TI_SHEN,CHARACTER_SKILL_1, CHARACTER_SKILL_2, CHARACTER_SKILL_3, CHARACTER_PSYCHIC, CHARACTER_SECRET_SCROLL]
        original=self.device.stuck_timer
        self.device.stuck_timer=Timer(100,100).start()
        for _ in self.loop():
            if self.appear_then_click(DUEL_EXCEPTION):
                self.config.Duel_VictoryNumber+=1
                print(f'find a exception')
                return 'FIGHT_SUCCESS'
            if self.appear_then_click(DUEL_FIGHT_FAIL):
                self.device.stuck_timer=original
                print(f'Fight_FAIL')
                return 'FIGHT_FAIL'
            if self.appear_then_click(DUEL_FIGHT_SUCCESS):
                self.device.stuck_timer=original
                self.config.Duel_VictoryNumber+=1
                print(f'FIGHT_SUCCESS')
                return 'FIGHT_SUCCESS'
            if self.appear(DUEL_ROUND_SWITCH):
                print('ROUND SWITCH')
                try:
                    self.click_buttons_until_end(CHARACTER_ATTACK,buttons,DUEL_FIGHT_END)
                finally:
                    self.device.stuck_record_clear()



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

    def _weekly_victory_reward_claim(self):
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



