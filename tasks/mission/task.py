from module.base.button import ButtonWrapper
from module.ocr.ocr import RecOCR,OcrWhiteLetterOnComplexBackground
from tasks.mission.assets.assets_mission import  ACCPET_BUTTON, MISSION_JADE, TASK_BOX_BLUE, TASK_BOX_RED
from tasks.mission.mission_ocr import MissionOcr
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

    def task_parse(self, image, name, time, jade):
        """识别单个任务位, 各识别区域使用截取好的固定位置素材。

        Args:
            image: 截屏
            name: 任务名素材 (竖排, 切字逐字识别)
            time: 时限素材 (横排)
            jade: 魂玉数量素材
        """
        #name: 任务名竖排, 切字逐字识别
        ocr=OcrWhiteLetterOnComplexBackground(name)
        self.name=ocr.ocr_single_line(image, vertical=True)
        #button
        ACCPET_BUTTON.load_search(self.area)
        if ACCPET_BUTTON.match_template(image,similarity=0.7):
            self.button=ACCPET_BUTTON.button
        else:
            self.valid=False
            return
        #time
        ocr=RecOCR(time)
        self.time=self.time_parse(ocr.ocr_single_line(image))
        #jade
        MISSION_JADE.load_search(self.area)
        if MISSION_JADE.match_template(image,similarity=0.6):
            ocr=MissionOcr(jade)
            self.jade=self.jade_parse(ocr.ocr_single_line(image))
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

    def jade_parse(self, jade: str) -> int:
        """解析魂玉数量字符串为整数, 识别失败时返回0"""
        import re
        match = re.search(r'\d+', jade)
        return int(match.group()) if match else 0