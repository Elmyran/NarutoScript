from module.base.timer import Timer
from module.exception import GameStuckError
from module.logger.logger import logger
from module.ocr.ocr import   DigitCounter, Ocr
from tasks.base.page import page_mission
from tasks.base.taskui import TaskUI
from tasks.mission.assets.assets_mission import *
from tasks.mission.mission_keyword import MissionClaimable
from tasks.mission.task import MissionDurationOcr, Task
class Mission(TaskUI):
    tasks=[]
    value:int=0
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
        
        self.config.task_stop()

    def handle_mission(self):
        self.device.click_record_clear()
        self.ui_ensure(page_mission)
        self._mission_reward_claim()
        try:
            self.device.stuck_timer=Timer(180,count=180).start()
            self._circle_task_select()
        finally:
            self.device.stuck_timer=Timer(60,count=60).start()
        self.ui_goto_main()

    def _circle_task_select(self):
        
        for _ in self.loop():
            res=self._task_select()
            if res:
                break
            self._task_refresh()
        with self.config.multi_set():
            self.config.stored.MissionAccept.write_missions(self.tasks)
            self.config.stored.MissionAccept.value=self.value
    def _task_select(self):
        select=DigitCounter(TASK_SELECT_REAMIN_TIMES)
        current,remain,total=select.ocr_single_line(self.device.image)
        if remain==total:
            return True
        # 清空任务列表
        self.tasks=[]
        self.value=remain
        tasks=self._tasks_recognition()
        tasks=self.sort_tasks(tasks)
        tasks=self._task_strategy(tasks)
        time=Timer(60,count=60).start()
        skip_first_screenshot = True  
        for task in tasks:
            if skip_first_screenshot:  
                skip_first_screenshot = False  
            else:  
                self.device.screenshot()  
            if time.reached():
                raise GameStuckError(' Mission Task  Select Stuck')
            res=self._single_task_select(task)
            if not res:
                break
            else:
                self.value+=1
                self.tasks.append(task.time)           
        return True
    def _single_task_select(self,task):
        click_interval=Timer(1).start()
        for _ in self.loop():
            if CHARACTER_UNSELECTED.match_template(self.device.image,similarity=0.6, direct_match=True):
                if self.character_select():
                    return True
                else:
                    return False
            if click_interval.reached():
                self.device.click(task)
                click_interval.reset()
                continue
            
    def _task_refresh(self):
        refresh=DigitCounter(TASK_REFRESH_REMAIN_TIMES)
        current,_,_=refresh.ocr_single_line(self.device.image)
        pre=current
        for _ in self.loop():
            current,_,_=refresh.ocr_single_line(self.device.image)
            if current!=pre:
                return True
            if self.appear(TASK_REFRESH_TIMES_SHORTAGE):
                return False
            # todo 超影免费刷新button
    def character_select(self):
        character_first_click_interval = Timer(2).start()  
        character_auto_select_interval = Timer(1).start()
        select_auto=False
        for _ in self.loop():  
            if THE_TASKBAR_IS_FULL.match_template(self.device.image):  
                logger.info('Taskbar is full')  
                return False  
            if CHARACTER_SELECTED.match_template(self.device.image,similarity=0.6,direct_match=True):  
                if self.appear_then_click(TASK_ACCEPT, interval=1):  
                    continue
            if self.appear(MISSION_CHECK):  
                logger.info('Mission check appeared')  
                return True  
            if CHARACTER_UNSELECTED.match_template(self.device.image, similarity=0.6,direct_match=True):
                if self.appear(CHARACTER_SELECTED_AUTO):
                    select_auto=True
                    if character_auto_select_interval.reached():  
                        self.device.click(CHARACTER_SELECTED_AUTO)  
                        character_auto_select_interval.reset()
                        continue  
            
                if not select_auto :
                    if character_first_click_interval.reached():  
                        self.device.click(CHARACTER_FIRST)  
                        character_first_click_interval.reset()  
                        continue
            
            
              
            
    def _mission_reward_claim(self):
        ocr = MissionDurationOcr(MISSION_TASK_CLAIMED_LIST, lang='cn')
        res = ocr.matched_ocr(self.device.image, MissionClaimable)
        if not res:
            return
        self.device.click(res[0])
        time = Timer(2, count=3).start()
        click_interval=Timer(1)
        for _ in self.loop():
            if time.reached():
                break
            if self.appear_then_click(MISSION_REWARD_CLAIM_ALL,interval=1):
                time.reset()
                continue
            if self.appear_then_click(MISSION_REWARD,interval=1):
                time.reset()
                continue
            res = ocr.matched_ocr(self.device.image, keyword_classes=MissionClaimable)
            if res:
                if click_interval.reached():
                    self.device.click(res[0])
                    click_interval.reset()
                time.reset()
            if self.match_template_color(TASK_BAR_IS_EMPTY):
                break

            



    def _tasks_recognition(self):
        task_areas=[TASK_1_AREA,TASK_2_AREA,TASK_3_AREA]
        tasks=[]
        skip_first_screenshot=True
        for area in task_areas:
            if skip_first_screenshot:
                skip_first_screenshot=False
            else :
                self.device.screenshot()
            task=Task(area)
            task.task_parse(self.device.image)
            if task.valid:
                tasks.append(task)
        return tasks
       

    def sort_tasks(self, tasks):
        if not tasks:
            logger.warning("没有可任务")
            return []

        # 按优先级排序：先按箱子类型（RED=1, BLUE=2, GREEN=3），再按魂玉数量（降序）
        sorted_tasks = sorted(tasks, key=lambda x: (x.priority.value, -x.jade))

        return sorted_tasks

    def _task_strategy(self, tasks):
        return tasks
az=Mission('ns',task='Alas')
az.device.screenshot()
task=Task(TASK_1_AREA)
task.task_parse(az.device.image)
task=Task(TASK_2_AREA)
task.task_parse(az.device.image)
task=Task(TASK_3_AREA)
task.task_parse(az.device.image)
print(task)