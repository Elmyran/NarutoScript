import re

from psutil._pswindows import Priority

from module.base.timer import Timer
from module.exception import GameStuckError
from module.logger.logger import logger
from module.ocr.digit import SimpleDigitOcr
from module.ocr.ocr import Ocr, Digit, Duration, OcrResultButton
from module.ocr.onnxocr.onnx_paddleocr import ONNXPaddleOcr
from module.ocr.utils import pair_buttons
from tasks.base.page import page_main
from tasks.base.ui import UI

from tasks.mission.assets.assets_mission import *
from tasks.mission.filter import TimeFilterOcr
from tasks.mission.keyword import Claimable, Acceptable
from tasks.mission.priority import TaskPriority, MissionTask


class Mission(UI):
    def run(self):
        self.handle_mission()
        self.config.task_delay(server_update=True)
        self.config.task_stop()
    def handle_mission(self):
        self.device.click_record_clear()
        self.ui_ensure(page_main)
        if not self._mission_enter():
            return False
        self._mission_reward_claim()
        for _ in self.loop():
            if self._mission_selected():
                continue
            else:
                break
        self.mission_exit()


    def _mission_enter(self):
        self.device.swipe([0, 322], [1280, 314])
        move = True
        time = Timer(10, count=10).start()
        m = 2
        for _ in self.loop():
            if time.reached():
                if move and m % 2 == 0:
                    self.device.swipe([1200, 314], [0, 322])
                    time.reset()
                    m = m + 1
                elif move and m % 2 == 1:
                    self.device.swipe([0, 322], [1200, 314])
                    m = m + 1
                    time.reset()
                elif m > 5:
                    raise GameStuckError("Mission enter Stucked")
            if self.appear(MISSION_CHECK):
                return True
            MISSION_RED_DOT.load_search((100, 50, 1100, 700))
            if self.appear(MISSION_RED_DOT):
                move = False
                MAIN_GOTO_MISSION.load_search((100, 50, 1100, 700))
                if self.appear_then_click(MAIN_GOTO_MISSION):
                    continue



        logger.info(f"Mission  entered")

    def _mission_reward_claim(self):
        ocr = Ocr(MISSION_TASK_CLAIMED_LIST, lang='cn')
        res = ocr.matched_ocr(self.device.image, Claimable)
        if not res:
            return
        self.device.click(res[0])
        time = Timer(15, count=20).start()
        times=0
        for _ in self.loop():
            if time.reached():
                raise GameStuckError("Mission reward claim")
            if self.appear_then_click(MISSION_REWARD_CLAIM_ALL,interval=0.5):
                continue
            if self.appear_then_click(MISSION_REWARD,interval=0.5):
                continue
            res = ocr.matched_ocr(self.device.image, Claimable)
            if not res and times>2:
                break
            elif not res:
                times += 1
            if res:
                self.device.click(res[0])


    def _mission_selected(self):
        time = Timer(10, count=20).start()
        task_select_time = Timer(4, count=8).start()
        for _ in self.loop():
            if task_select_time.reached():
                return False
            if time.reached():
                raise GameStuckError("Task Selected Stucked")
            TASK_HAVE_ACCEPTED.load_search(TASK_DETECT_AREA.area)
            res=TASK_HAVE_ACCEPTED.match_multi_template(self.device.image)
            if res and len(res)==3:
                return False

            if CHARACTER_UNSELECTED.match_template(self.device.image, direct_match=True):
                break
            task = self._mission_select_priority()
            if task:
                print(task)
                logger.info(f"点击前任务魂玉: {task.soul_jade}")
                self.device.click(task)
                continue


        for _ in self.loop():
            if time.reached():
                raise GameStuckError("Character selected Stucked")
            if THE_TASKBAR_IS_FULL.match_template(self.device.image):
                return False
            else:
                if self.appear(MISSION_CHECK):
                    break
            if self.appear(CHARACTER_SELECTED_AUTO) and CHARACTER_UNSELECTED.match_template(self.device.image, direct_match=True):
                self.device.click(CHARACTER_SELECTED_AUTO)
            elif CHARACTER_UNSELECTED.match_template(self.device.image, direct_match=True):
                self.device.click(CHARACTER_FIRST)
            if CHARACTER_SELECTED.match_template(self.device.image, direct_match=True):
                self.appear_then_click(TASK_ACCEPT,interval=1)

        return True

    def _mission_select_priority(self):
        self.device.screenshot()
        # OCR识别部分保持不变
        ocr =Ocr(TASK_AREA)
        results=ocr.detect_and_ocr(self.device.image)
        task_name = [OcrResultButton(result, matched_keyword=None) for result in results]

        ocr=Ocr(TASK_DETECT_AREA)
        task_buttons=ocr.matched_ocr(self.device.image, Acceptable)
        ocr=Duration(TASK_DETECT_AREA)

        results=ocr.detect_and_ocr(self.device.image)
        # 在创建 OcrResultButton 之前检查 results
        for result in results:
            print(f"OCR result type: {type(result)}, text: {result.ocr_text}")
        task_times= [OcrResultButton(result, matched_keyword=None) for result in results]
        task_time=[]
        for task in task_times:
            time=task.name
            time = time.replace("时间：", "").replace("时间:", "").strip()
            if re.match(r'^\d+时\d+分$', time):
                task_time.append(task)
        # 构建当前任务列表
        # 在创建 OcrResultButton 之前检查 results
        for result in results:
            print(f"OCR result type: {type(result)}, text: {result.ocr_text}")
        currentTask = []
        for name, time in pair_buttons(task_name, task_time, (-100, -50, 800, 50)):
            task=MissionTask(name=name,
                             time=self._parse_time_to_minutes(time.name),
                             area=(name.area[0], name.area[1], time.area[2], time.area[3]),
                             button=(name.area[0], name.area[1], time.area[2], time.area[3]))
            currentTask.append(task)

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

        highest_priority_task = sorted_tasks[0]
        logger.info(f"选择最高优先级任务: {highest_priority_task.name}, "
                    f"箱子类型: {highest_priority_task.box_type.name}, "
                    f"魂玉: {highest_priority_task.soul_jade}")

        return highest_priority_task

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


                from module.base.utils import crop
                cropped_image = crop(self.device.image, number_area)

                ocr = Digit(SOUL_JADE)

                res = ocr.ocr_single_line(cropped_image,direct_ocr=True)
                if res:
                    task.soul_jade_amount = res
                    break
            if time.reached():
                task.soul_jade = 0
                break

    def get_box_type(self, task):
        time = Timer(2, 4).start()
        for _ in self.loop():
            TASK_GREEN_BOX.load_search(task.area)
            if self.appear(TASK_GREEN_BOX):
                task.box_type = TaskPriority.GREEN
                break
            TASK_BLUE_BOX.load_search(task.area)
            if self.appear(TASK_BLUE_BOX):
                task.box_type = TaskPriority.BLUE
                break
            TASK_RED_BOX.load_search(task.area)
            if self.appear(TASK_RED_BOX):
                task.box_type = TaskPriority.RED
                break
            if time.reached():
                task.box_type = TaskPriority.RED
                break

    def _parse_time_to_minutes(self, time_str: str) -> int:
        """解析时间字符串为分钟数，并修正为60的倍数"""
        import re

        # 原有解析逻辑
        hour_match = re.search(r'(\d+)时', time_str)
        minute_match = re.search(r'(\d+)分', time_str)

        hours = int(hour_match.group(1)) if hour_match else 0
        minutes = int(minute_match.group(1)) if minute_match else 0

        total_minutes = hours * 60 + minutes

        # 添加时间修正逻辑 - 调整为最接近的60分钟倍数
        corrected_minutes = round(total_minutes / 60) * 60

        logger.debug(f"时间解析: '{time_str}' -> {total_minutes}分钟 -> 修正为 {corrected_minutes}分钟")
        return corrected_minutes

    def mission_exit(self):
        time = Timer(10, 20).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError('Mission Exite Stucked')
            if self.appear(CHARACTER_SELECT_EXIT):
                self.device.click(CHARACTER_SELECT_EXIT)
                continue
            if self.appear(MISSION_EXIT):
                self.device.click(MISSION_EXIT)
                continue
            if self.ui_page_appear(page_main):
                break

