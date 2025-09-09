from module.base.timer import Timer
from module.exception import GameStuckError
from module.logger.logger import logger
from module.ocr.ocr import Ocr, DigitCounter
from module.ocr.ocrutils import DigitOcr
from module.ocr.onnxocr.onnx_paddleocr import ONNXPaddleOcr
from module.ocr.utils import pair_buttons
from tasks.base.page import page_main
from tasks.base.task_tab.draglist import TASK_TAB_LIST
from tasks.base.task_tab.keyword import MissionKeyword
from tasks.base.ui import UI
from tasks.mission.assets.assets_mission import *
from tasks.mission.mission_keyword import Claimable
from tasks.mission.priority import TaskPriority
class Mission(UI):
    def run(self):
        if self.config.stored.MissionAccept.is_expired():
            self.config.stored.MissionAccept.clear()
        self.handle_mission()
        if self.config.stored.MissionAccept.is_full():
            self.config.task_delay(server_update=True)
        else:
            delay_time=self.config.stored.MissionAccept.get_nearest_completion_time()
            if delay_time:
                self.config.task_delay(target=delay_time)
            else:
                self.config.task_delay(server_update=True)
        with self.config.multi_set():
            mission=self.config.stored.MissionAccept.value
            self.config.stored.Mission.value=mission
        self.config.task_stop()

    def handle_mission(self):
        self.device.click_record_clear()
        self.ui_ensure(page_main)
        if not TASK_TAB_LIST.search_rows(main=self,keyword=MissionKeyword):
            raise GameStuckError(' Mission Tab Not Found')
        self._mission_reward_claim()
        try:
            self.device.stuck_timer=Timer(180,count=180).start()
            self._circle_task_select()
        finally:
            self.device.stuck_timer=Timer(60,count=60).start()
        self.ui_goto_main()

    def _circle_task_select(self):
        accepted_tasks=[]
        for _ in self.loop():
            res=self._task_select(accepted_tasks)
            if res:
                break
            self._task_refresh()
        with self.config.multi_set():
            self.config.stored.MissionAccept.write_missions(accepted_tasks)
    def _task_select(self,accepted_tasks):
        tasks=self._mission_select_priority()
        tasks=self._task_strategy(tasks)
        select=DigitCounter(TASK_SELECT_REAMIN_TIMES)
        task_select_number=0
        time=Timer(60,count=60).start()
        for task in tasks:
            if time.reached():
                raise GameStuckError(' Mission Task  Select Stuck')
            current,remain,total=select.ocr_single_line(self.device.image)
            if remain!=0 and total!=0 and remain>task_select_number:
                task_select_number=remain
            if total!=0 and remain==total:
                break
            res=self._single_task_select(task)
            if res:
                break
            else:
                accepted_tasks.append(task.time)
        with self.config.multi_set():
            self.config.stored.MissionAccept.value=task_select_number
        return True
    def _single_task_select(self,task):
        for _ in self.loop():
            if CHARACTER_UNSELECTED.match_template(self.device.image, direct_match=True):
                if self.character_select():
                    return True
                else:
                    return False
            self.device.click(task)
    def _task_refresh(self):
        refresh=DigitCounter(TASK_REFRESH_REMAIN_TIMES)
        current,remain,total=refresh.ocr_single_line(self.device.image)
        pre=current
        for _ in self.loop():
            current,remain,total=refresh.ocr_single_line(self.device.image)
            if current!=pre:
                return True
            if self.appear(TASK_REFRESH_TIMES_SHORTAGE):
                return False
            # todo 超影免费刷新button
    def character_select(self):
        time=Timer(20,count=30).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError("Character selected Stucked")
            if THE_TASKBAR_IS_FULL.match_template(self.device.image):
                return True
            else:
                if self.appear(MISSION_CHECK):
                    return False
            if self.appear(CHARACTER_SELECTED_AUTO) and CHARACTER_UNSELECTED.match_template(self.device.image, direct_match=True):
                self.device.click(CHARACTER_SELECTED_AUTO)
            elif CHARACTER_UNSELECTED.match_template(self.device.image, direct_match=True):
                self.device.click(CHARACTER_FIRST)
            if CHARACTER_SELECTED.match_template(self.device.image, direct_match=True):
                self.appear_then_click(TASK_ACCEPT,interval=2)
    def _mission_reward_claim(self):
        ocr = Ocr(MISSION_TASK_CLAIMED_LIST, lang='cn')
        res = ocr.matched_ocr(self.device.image, Claimable)
        if not res:
            return
        self.device.click(res[0])
        time = Timer(3, count=5).start()
        for _ in self.loop():
            if time.reached():
                break
            if self.appear_then_click(MISSION_REWARD_CLAIM_ALL,interval=0.5):
                continue
            if self.appear_then_click(MISSION_REWARD,interval=0.5):
                continue
            res = ocr.matched_ocr(self.device.image, Claimable)
            if res:
                self.device.click(res[0])
                time.reset()





    def _mission_select_priority(self):
        self.device.screenshot()
        # OCR识别部分保持不变
        ocr = ONNXPaddleOcr(use_angle_cls=True, use_gpu=False)
        result = ocr.ocr(self.device.image)
        # 时间和任务识别
        task_time = ocr.matchTime(result)
        task_name = ocr.matchArea(result, TASK_AREA.search)
        task_buttons = ocr.matchKeys(result, '接取')
        # 构建当前任务列表
        currentTask = []
        for name, time in pair_buttons(task_name, task_time, (-100, -50, 800, 50)):
            name.time = self._parse_time_to_minutes(time.txt)
            currentTask.append(name)

        task_with_button = []
        for task, button in pair_buttons(currentTask, task_buttons, (-100, -50, 800, 110)):
            task.button = button.button
            task.area = (
                task.area[0],
                min(task.area[1], button.area[1]),
                button.area[0],
                max(task.area[3], button.area[3])
            )
            # 获取任务奖励信息
            self.get_soul_jade_amount(task)
            self.get_box_type(task)
            task_with_button.append(task)
            # 直接排序并返回最高优先级任务
        return self._select_highest_priority_task(task_with_button)

    def _select_highest_priority_task(self, tasks):
        """根据箱子类型和魂玉数量选择最高优先级任务"""
        if not tasks:
            logger.warning("没有可用任务")
            return None

            # 按优先级排序：先按箱子类型（RED=1, BLUE=2, GREEN=3），再按魂玉数量（降序）
        sorted_tasks = sorted(tasks, key=lambda x: (x.box_type.value, -x.soul_jade))

        return sorted_tasks

    def get_soul_jade_amount(self, task):
        time = Timer(2, 4).start()
        for _ in self.loop():
            SOUL_JADE.load_search(task.area)
            if SOUL_JADE.match_template(self.device.image, similarity=0.6):
                # 基于匹配位置计算数字区域

                number_area = (
                    SOUL_JADE.button[0],
                    SOUL_JADE.button[1],
                    SOUL_JADE.button[2] + 20,  # 向右扩展包含数字
                    SOUL_JADE.button[3] + 20  # 向下扩展包含数字
                )
                ocr = DigitOcr()
                res = ocr.extract_digit_simple(self.device.image, number_area)
                if res:
                    task.soul_jade = int(res)
                    break
            if time.reached():
                task.soul_jade = 0
                break

    def get_box_type(self, task):
        time = Timer(2, 4).start()
        for _ in self.loop():
            TASK_BOX_GREEN.load_search(task.area)
            if self.appear(TASK_BOX_GREEN):
                task.box_type = TaskPriority.GREEN
                break
            TASK_BOX_BLUE.load_search(task.area)
            if self.appear(TASK_BOX_BLUE):
                task.box_type = TaskPriority.BLUE
                break
            TASK_BOX_BLUE.load_search(task.area)
            if self.appear(TASK_BOX_RED):
                task.box_type = TaskPriority.RED
                break
            if time.reached():
                task.box_type = TaskPriority.RED
                break

    def _parse_time_to_minutes(self, time_str: str) -> int:
        """解析时间字符串为分钟数，并修正为60的倍数"""
        import re
        hour_match = re.search(r'(\d+)时', time_str)
        minute_match = re.search(r'(\d+)分', time_str)
        hours = int(hour_match.group(1)) if hour_match else 0
        minutes = int(minute_match.group(1)) if minute_match else 0
        total_minutes = hours * 60 + minutes
        # 添加时间修正逻辑 - 调整为最接近的60分钟倍数
        corrected_minutes = round(total_minutes / 60) * 60
        return corrected_minutes

    def _task_strategy(self, tasks):
        return tasks
    def test(self):
        self.config.stored.MissionAccept.write_missions([30])
        time=self.config.stored.MissionAccept.get_nearest_completion_time()
        self.config.task_delay(target=time)
az=Mission('src',task='Alas')
az.test()


