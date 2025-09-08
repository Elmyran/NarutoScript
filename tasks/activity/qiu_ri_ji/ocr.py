import re

from module.ocr.ocr import Ocr


class OcrQuizTitle(Ocr):
    def after_process(self, result):
        result = super().after_process(result)
        result = result.replace('走', '志')
        result=result.replace('町','盯')
        return result
class OcrQuizOption(Ocr):
    def after_process(self, result):
        result = super().after_process(result)
        result = re.sub(r'[^\u4e00-\u9fff]', '', result)
        return result