from module.base.timer import Timer
from module.exception import GameStuckError
from module.logger import logger
from tasks.base.assets.assets_base_skill import CHARACTER_SKILL_1, CHARACTER_SKILL_2, CHARACTER_ATTACK
from tasks.base.page import page_main, page_feng_rao
from tasks.base.ui import UI
from tasks.fengrao.assets.assets_fengrao import FENG_RAO_RED_DOT, MAIN_GOTO_FENG_RAO, FENG_RAO_CHECK, \
    FENG_RAO_START_FIGHT_BUTTON, FENG_RAO_FIGHT_STATUS, FENG_RAO_FIGHT_SUCCESS, FENG_RAO_HAVE_DONE, FENG_RAO_EXIT
import time

class FengRaoFight(UI):
    def handle_feng_rao(self):
        self.device.click_record_clear()
        self.ui_ensure(page_main)
        self._feng_rao_enter()
        self._feng_rao_fight()
        self.ui_goto_main()


    def _feng_rao_enter(self):
        self.device.swipe([0, 322], [1200, 314])
        move = True
        m = 2
        moving = True           # 是否正在滑动
        last_swipe_time = time.time()
        time_limit = Timer(10, count=10).start()

        for _ in self.loop():
            # 滑动超时处理
            if time_limit.reached():
                if move and m % 2 == 0:
                    self.device.swipe([1200, 314], [0, 322])
                    last_swipe_time = time.time()
                    m += 1
                    time_limit.reset()
                elif move and m % 2 == 1:
                    self.device.swipe([0, 322], [1200, 314])
                    last_swipe_time = time.time()
                    m += 1
                    time_limit.reset()
                elif m > 5:
                    raise GameStuckError("Duel enter Stuck")

            # 滑动刚结束，给动画缓冲
            if time.time() - last_swipe_time < 0.3:
                moving = True
            else:
                moving = False

            # 检查是否进入
            if self.appear(FENG_RAO_CHECK):
                return True

            # 全屏加载搜索区域
            MAIN_GOTO_FENG_RAO.load_search((0, 0, 1280, 720))

            # 滑动时只识别，不点击
            if not moving and self.appear_then_click(MAIN_GOTO_FENG_RAO):
                continue


        logger.info(f"FengRao entered")
    def _feng_rao_fight(self):
        for _ in self.loop():
            if self.appear(FENG_RAO_HAVE_DONE):
                return
            if self.appear_then_click(FENG_RAO_START_FIGHT_BUTTON,interval=1):
                continue
            if self.appear_then_click(FENG_RAO_FIGHT_STATUS,interval=1):
                break
        self.fight()

    def fight(self):
        self.device.screenshot()
        time=Timer(40, count=60).start()
        self.device.click_record_clear()
        time_skill_1 = Timer(10)  # 技能1冷却10秒
        time_skill_2 = Timer(15)  # 技能2冷却15秒
        skill_1_first = True
        skill_2_first = True
        try:
            for _ in self.loop():
                    if time.reached():
                        raise GameStuckError("Feng Rao  Stucked")
                    if self.appear(FENG_RAO_CHECK):
                        return
                    if self.appear(FENG_RAO_HAVE_DONE):
                        return
                    if self.appear_then_click(FENG_RAO_FIGHT_SUCCESS):
                        return
                    # 优先级：技能1 > 技能2 > 普通攻击
                    if time_skill_1.reached() or skill_1_first:
                        skill_1_first = False
                        time_skill_1.clear()
                        self.device.long_click(CHARACTER_SKILL_1, 2)  # 执行2秒
                        time_skill_1.start()
                    elif time_skill_2.reached() or skill_2_first:
                        skill_2_first = False
                        time_skill_2.clear()
                        self.device.long_click(CHARACTER_SKILL_2, 5)  # 执行5秒
                        time_skill_2.start()
                    else:
                        self.device.long_click(CHARACTER_ATTACK, 3)   # 执行3秒
                    if len(self.device.click_record) > 10:
                        self.device.click_record_clear()

        finally:
            self.device.click_record_clear()
            self._force_release_touch()

    def _force_release_touch(self):
        """强制释放所有触摸状态"""
        method = self.config.Emulator_ControlMethod

        if method == 'MaaTouch':
            try:
                builder = self.device.maatouch_builder
                builder.up().commit()
                builder.send()
            except:
                pass
        elif method == 'minitouch':
            try:
                builder = self.device.minitouch_builder
                builder.up().commit()
                builder.send()
            except:
                pass
        elif method == 'scrcpy':
            try:
                # Scrcpy 使用 ACTION_UP 事件释放
                if hasattr(self.device, '_scrcpy_control'):
                    self.device._scrcpy_control.touch(0, 0, 1)  # ACTION_UP
            except:
                pass
        elif method == 'nemu_ipc':
            try:
                if hasattr(self.device, 'nemu_ipc'):
                    self.device.nemu_ipc.up()
            except:
                pass



















