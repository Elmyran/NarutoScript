from module.base.timer import Timer
from module.exception import GameStuckError
from module.logger.logger import logger
from module.ocr.ocr import DigitCounter
from tasks.base.page import page_mission
from tasks.base.taskui import TaskUI
from tasks.mission.assets.assets_mission import *
from tasks.mission.mission_keyword import MissionClaimable
from tasks.mission.mission_strategy import STRATEGIES, NormalAcceptStrategy, RedBoxFirstStrategy, RedBoxOnlyStrategy, StrategyAction
from tasks.mission.task import MissionDurationOcr, Task


class Mission(TaskUI):
    def __init__(self, config, device=None, task=None):
        super().__init__(config, device=device, task=task)
        self.tasks = []  # 本次运行新接取任务的时长(分钟), 用于写入完成时间
        self.value = 0  # 当前已接取的任务数量, 每轮由OCR实时更新
        self.strategy = None  # 接取策略, 进入任务面板后由 _select_strategy() 确定

    def _select_strategy(self):
        """进入任务面板后按实时状态选择策略。

        免费刷新按钮是特权专属元素, 检测到即 mark_active 记录超影有效;
        无超影(normal)按优先级接满; 有超影按 GUI 配置选 red_box / red_box_only。
        """
        stored = self.config.stored.ChaoYingDays
        if self._task_refreshable():
            stored.mark_active()
            logger.info('检测到超影')
        if stored.predict_current() <= 0:
            return NormalAcceptStrategy()
        if self.config.MissionStorage_MissionStrategy == '只拿红箱子':
            return RedBoxOnlyStrategy()
        return RedBoxFirstStrategy()
    # ============================== 调度入口 ==============================

    def run(self):
        if self.config.stored.MissionAccept.is_expired():
            self.config.stored.MissionAccept.clear()
        self.handle_mission()
        if self.config.stored.MissionAccept.is_full():
            self.config.task_delay(server_update=True)
        else:
            delay_time = self.config.stored.MissionAccept.get_nearest_completion_time()
            if delay_time:
                self.config.task_delay(target=delay_time)
            else:
                self.config.task_delay(server_update=True)

        self.config.task_stop()

    # ============================== 主流程 ==============================

    def handle_mission(self):
        self.device.click_record_clear()
        self.ui_ensure(page_mission)
        self.strategy = self._select_strategy()
        self._mission_reward_claim()
        stuck_timer = self.device.stuck_timer
        try:
            self.device.stuck_timer = Timer(180, count=180).start()
            self._accept_tasks()
        finally:
            self.device.stuck_timer = Timer(stuck_timer.limit, count=stuck_timer.count).start()
        self.ui_goto_main()

    # ============================== 领取奖励 ==============================

    def _mission_reward_claim(self):
        ocr = MissionDurationOcr(MISSION_TASK_CLAIMED_LIST, lang='cn')
        res = ocr.matched_ocr(self.device.image, MissionClaimable)
        if not res:
            return
        self.device.click(res[0])
        timeout = Timer(2, count=3).start()
        click_interval = Timer(1).start()
        for _ in self.loop():
            if timeout.reached():
                break
            if self.appear_then_click(MISSION_REWARD_CLAIM_ALL, interval=1):
                timeout.reset()
                continue
            if self.appear_then_click(MISSION_REWARD, interval=1):
                timeout.reset()
                continue
            res = ocr.matched_ocr(self.device.image, keyword_classes=MissionClaimable)
            if res:
                if click_interval.reached():
                    self.device.click(res[0])
                    click_interval.reset()
                timeout.reset()
            if self.match_template_color(TASK_BAR_IS_EMPTY):
                break

    # ============================== 接取任务 ==============================

    def _accept_tasks(self):
        """接取任务主循环: 每轮由策略做出决策(接取/刷新/停止), 本骨架只负责执行。

        策略见 mission_strategy.STRATEGIES:
            normal       普通玩家: 不可刷新, 按优先级接满3个
            red_box      特权玩家: 红箱优先, 无红箱刷新, 刷新耗尽接其他, 直到接满
            red_box_only 特权玩家: 只接红箱, 刷新耗尽即停止, 不要求接满

        次数语义(TASK_SELECT_REAMIN_TIMES 显示为 X/9):
            current = X = 当前可接取的任务数量
            remain = 9 - X = 已接取的任务数量
            remain == total 即 current == 0, 已接满, 结束接取
        """
        self.tasks = []
        select = DigitCounter(TASK_SELECT_REAMIN_TIMES)

        for _ in self.loop():
            current, remain, total = select.ocr_single_line(self.device.image)
            self.value = remain
            if remain == total:
                break
            tasks = self._task_strategy(self._scan_tasks())
            action, task = self.strategy.decide(tasks, self.tasks, self._task_refreshable())
            if action == StrategyAction.STOP:
                break
            if action == StrategyAction.REFRESH:
                if not self._task_refresh():
                    break
                continue
            if not self._accept_one(task):
                break
            self.tasks.append(task.time)
        with self.config.multi_set():
            self.config.stored.MissionAccept.write_missions(self.tasks)
            self.config.stored.MissionAccept.set(self.value)

    def _accept_one(self, task):
        """接取单个任务, 分两个阶段。

        注意 MISSION_CHECK 是任务面板本身的页面标识(page_mission), 裸面板上始终可见,
        不能作为"接取成功"的单一信号, 必须等角色弹窗元素消失后面板重新可见才算完成。

        Args:
            task (Task): 待接取的任务

        Returns:
            bool: 是否接取成功
        """
        timeout = Timer(60, count=60).start()
        click_interval = Timer(1).start()
        # 阶段1: 任务面板上点击任务卡, 直到角色选择弹窗打开
        for _ in self.loop():
            if timeout.reached():
                raise GameStuckError('Mission accept task stuck')
            if self.appear(MISSION_SELECTED_SUCCESS):
                # 任务已被接取过, 不可再接
                return False
            if CHARACTER_UNSELECTED.match_template(self.device.image, similarity=0.6, direct_match=True):
                break
            if click_interval.reached():
                self.device.click(task)
                click_interval.reset()
        # 阶段2: 弹窗内选择角色(优先自动选择)并确认接取
        first_interval = Timer(2).start()
        auto_interval = Timer(1).start()
        for _ in self.loop():
            if timeout.reached():
                raise GameStuckError('Mission accept task stuck')
            if THE_TASKBAR_IS_FULL.match_template(self.device.image):
                logger.info('Taskbar is full')
                return False
            selected = CHARACTER_SELECTED.match_template(self.device.image, similarity=0.6, direct_match=True)
            unselected = CHARACTER_UNSELECTED.match_template(self.device.image, similarity=0.6, direct_match=True)
            if selected:
                if self.appear_then_click(TASK_ACCEPT, interval=1):
                    continue
            if not selected and not unselected and self.appear(MISSION_CHECK):
                # 弹窗元素消失且回到任务面板, 接取完成
                logger.info('Mission check appeared')
                return True
            if unselected:
                # 角色未选中: 自动选择按钮可用则点自动, 否则点第一个角色
                if self.appear(CHARACTER_SELECTED_AUTO):
                    if auto_interval.reached():
                        self.device.click(CHARACTER_SELECTED_AUTO)
                        auto_interval.reset()
                        continue
                else:
                    if first_interval.reached():
                        self.device.click(CHARACTER_FIRST)
                        first_interval.reset()
                        continue
        return False

    # ============================== 任务刷新 ==============================

    def _task_refreshable(self):
        """是否还有免费刷新次数(仅查询按钮状态, 不点击)。

        普通玩家面板没有刷新按钮, 恒为False; 特权玩家次数耗尽后按钮变为金币刷新状态, 也为False。
        """
        return not self.appear(TASK_REFRESH_TIMES_SHORTAGE) and self.appear(TASK_REFRESH_FREE)

    def _task_refresh(self):
        """免费刷新任务列表。

        特权玩家每日免费刷新6次; 次数耗尽后按钮变为金币刷新状态, 不消费金币。

        Returns:
            bool: 是否刷新成功(剩余免费次数减少)
        """
        if self.appear(TASK_REFRESH_TIMES_SHORTAGE):
            logger.info('Free refresh count shortage')
            return False

        refresh = DigitCounter(TASK_REFRESH_REMAIN_TIMES)
        pre, _, _ = refresh.ocr_single_line(self.device.image)
        click_interval = Timer(2)
        for _ in self.loop():
            if self.appear(TASK_REFRESH_TIMES_SHORTAGE):
                logger.info('Free refresh count shortage')
                return False
            if click_interval.reached():
                self.device.click(TASK_REFRESH_FREE)
                click_interval.reset()
            current, _, _ = refresh.ocr_single_line(self.device.image)
            if current < pre:
                logger.info('Mission task refreshed')
                return True
        return False

    # ============================== 任务扫描 ==============================

    def _scan_tasks(self):
        """扫描三个任务位, 识别有效任务。"""
        tasks = []
        skip_first_screenshot = True
        for area in (TASK_1_AREA, TASK_2_AREA, TASK_3_AREA):
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            task = Task(area)
            task.task_parse(self.device.image)
            if task.valid:
                tasks.append(task)
        if not tasks:
            logger.warning('没有可接取的任务')
        return tasks

    def _task_strategy(self, tasks):
        """策略扩展点: 对扫描结果排序, 默认红箱优先(RED>BLUE>GREEN), 同级魂玉降序。"""
        return sorted(tasks, key=lambda x: (x.priority.value, -x.jade))
if __name__ == '__main__':
    mission = Mission(config='ns', device='127.0.0.1:16384',task='Alas')
    mission.device.screenshot()
    mission.strategy = mission._select_strategy()
    mission._accept_tasks()
