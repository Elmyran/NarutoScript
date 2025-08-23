import time

from module.base.timer import Timer
from module.base.utils import random_rectangle_point, ensure_int
from module.exception import GameStuckError
from tasks.base.assets.assets_base_skill import CHARACTER_ATTACK, CHARACTER_TI_SHEN, CHARACTER_SKILL_1, \
    CHARACTER_SKILL_2, CHARACTER_SKILL_3, CHARACTER_PSYCHIC, CHARACTER_SECRET_SCROLL
from tasks.base.page import page_ninjutsu, page_main
from tasks.base.ui import UI
from tasks.duel.assets.assets_duel import *

class DuelDaily(UI):
    def handle_duel_daily(self):
        self.device.click_record_clear()
        self.ui_ensure(page_main)
        self.swipe_and_appear_then_click(DUEL_CHECK,MAIN_GOTO_DUEL,left=True)
        self.ui_ensure(page_ninjutsu)
        for _ in  self.loop():
            res=self._duel_task_detect()
            if res==False:
                if self.start_fight()=='Delay 5 Minute':
                    return  'Delay 5 Minute'
            else:
                break

    def _duel_task_detect(self):
        self.device.click_record_clear()
        self.device.stuck_record_clear()
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
        #奖励领取
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
                else:
                    break
            if self.appear_then_click(DUEL_TASK_RECALLED_FAIL,interval=0):
                have_recall_card=False
                continue
            if self.appear_then_click(DUEL_TASK_RECALLED_CONFIRM,interval=0):
                continue
            if self.appear(DUEL_TASK_RECALLED_BUTTON) and have_recall_card:
                self.device.click(DUEL_TASK_RECALLED_BUTTON)
                continue
            if self.appear_then_click(DUEL_TASK_REWARD_CLAIM_BUTTON,interval=0):
                continue
        #任务完成检测
        time_search=Timer(3, count=5).start()
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
                else:
                    break
            #检测到未达成
            if DUEL_TASK_NOT_ACHIEVED_BUTTON.match_template(self.device.image,direct_match=True):
                return False
        return True

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
            if self.appear_then_click(DUEL_TASK_PANEL):
                continue
            if self.appear_then_click(DUEL_START_FIGHT,similarity=0.95,interval=2):
                continue

        buttons = [CHARACTER_TI_SHEN,CHARACTER_SKILL_1, CHARACTER_SKILL_2, CHARACTER_SKILL_3, CHARACTER_PSYCHIC, CHARACTER_SECRET_SCROLL]


        for _ in self.loop():
            self.device.click_record_clear()
            if self.appear_then_click(DUEL_EXCEPTION):
                with self.config.multi_set():
                    self.config.Duel_CurrentVictoryNumber+=1
                print(f'find a exception')
                return 'FIGHT_SUCCESS'
            if self.appear_then_click(DUEL_FIGHT_FAIL):
                print(f'Fight_FAIL')
                return 'FIGHT_FAIL'
            if self.appear_then_click(DUEL_FIGHT_SUCCESS):
                with self.config.multi_set():
                    self.config.Duel_CurrentVictoryNumber+=1
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