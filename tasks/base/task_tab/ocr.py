
from pponnxcr.predict_system import BoxedResult


from module.base.button import ButtonWrapper
from module.logger import logger
from module.ocr.ocr import Ocr
from module.ocr.ocrutils import OCR
from module.ocr.onnxocr.onnx_paddleocr import ONNXPaddleOcr
from tasks.base.assets.assets_base_page import MAIN_GOTO_TASK_SEARCH_AREA


class TaskTabOcr(ONNXPaddleOcr):
    def __init__(self, button: ButtonWrapper, **kwargs):
        super().__init__(button, **kwargs)
    def after_process(self, result):
        """对OCR结果进行修正"""
        result = super().after_process(result)
        # 单字符修正
        result = result.replace('寒', '赛')
        result = result.replace('符', '行')
        result = result.replace('寨', '赛')
        result = result.replace('部', '所')
        result = result.replace('狂', '任')
        result = result.replace('践', '战')
        result = result.replace('公', '会')
        # 繁体字修正
        result = result.replace('組', '组')
        result = result.replace('決', '决')
        result = result.replace('鬥', '斗')
        result = result.replace('試', '试')
        result = result.replace('煉', '炼')
        result = result.replace('隊', '队')
        result = result.replace('襲', '袭')
        result = result.replace('豐', '丰')
        result = result.replace('饒', '饶')
        result = result.replace('間', '间')
        result = result.replace('紙', '织')
        result = result.replace('焗', '场')
        result = result.replace('綱','织')
        if '小队突' in result or '小队' in result or '突袭' in result:
            result='小队突袭'
        if '积分'in result or '积' in result or '分' in result:
            result = '积分赛'
        if '排' in result or '榜' in result or '行' in result:
            result = '排行榜'
        if '集会' in result or '任务' in result:
            result = '任务集会所'
        if '忍者挑' in result or '挑战' in result:
            result='忍者挑战'
        return result
    
TaskOcr=OCR(button=MAIN_GOTO_TASK_SEARCH_AREA, use_angle_cls=True,use_gpu=True)