from module.base.button import ButtonWrapper, ClickButton
from module.base.utils.utils import area_offset
from tasks.mission.assets.assets_mission import ACCEPTED_BUTTON, ACCPET_BUTTON, MISSION_JADE, TASK_BOX_BLUE, TASK_BOX_RED
from tasks.mission.mission_ocr import MissionDigit, MissionDurationOcr, MissionWhiteLetterOcr
from tasks.mission.priority import TaskPriority


class Task:
    name:str=""
    time:int=0
    jade:int=0 
    area:tuple[int, int, int, int]
    button:tuple[int, int, int, int]
    priority: TaskPriority=TaskPriority.GREEN
    valid:bool=True
    def __init__(self,area):
        if isinstance(area, ButtonWrapper):
            self.area = area.area
        elif isinstance(area, tuple):
            self.area = area
    def __str__(self):
        return f"任务: {self.name}, 魂玉: {self.jade},时间: {self.time}分钟, 优先级: {self.priority}"

    def task_parse(self,image):
        #name
        name_area = area_offset((0, 0, 100, 124), self.area[0:2])
        button = ClickButton(area=name_area, name='TASK')
        ocr=MissionWhiteLetterOcr(button)
        self.name=ocr.ocr_single_line(image)
        #time
        time_area = (  
        self.area[2] - 140,  
        self.area[1],        
        self.area[2],        
        self.area[3]          
        )  
        button = ClickButton(area=time_area, name='DURATION')
        ocr=MissionDurationOcr(button)
        time=ocr.ocr_single_line(image)
        self.time=self.time_parse(time)
        #button
        ACCPET_BUTTON.load_search(self.area)
        if ACCPET_BUTTON.match_template(image):
            self.button=ACCPET_BUTTON.button
        elif ACCEPTED_BUTTON.match_template(image,similarity=0.7):
            self.button=ACCEPTED_BUTTON.button
            self.valid=False
        #jade
        MISSION_JADE.load_search(self.area)
        if MISSION_JADE.match_template(image,similarity=0.6):
            jade_area=(  
            750,  
            self.area[1],        
            850,        
            self.area[3]          
            )  
            button=ClickButton(area=jade_area, name='JADE')
            ocr=MissionDigit(button)
            self.jade=ocr.ocr_single_line(image)
        #priority
        TASK_BOX_RED.load_search(self.area)
        TASK_BOX_BLUE.load_search(self.area)
        if TASK_BOX_RED.match_template(image,similarity=0.7):
            self.priority=TaskPriority.RED
        elif TASK_BOX_BLUE.match_template(image,similarity=0.7):
            self.priority=TaskPriority.BLUE
        else:
            self.priority=TaskPriority.GREEN
    def time_parse(self, time: str) -> int:
        """解析时间字符串为分钟数"""
        import re
        hour_match = re.search(r'(\d+)时', time)
        minute_match = re.search(r'(\d+)分', time)
        hours = int(hour_match.group(1)) if hour_match else 0
        minutes = int(minute_match.group(1)) if minute_match else 0

        return hours * 60 + minutes