import re

from module.ocr.ocr import Ocr


class OcrQuizTitle(Ocr):
    def after_process(self, result):
        # 添加题目特定的文本修正规则
        result = super().after_process(result)
        # 修正常见OCR错误
        result = result.replace('丁次', '丁次')
        result = result.replace('查克拉', '查克拉')
        return result
class OcrQuizOption(Ocr):
    def after_process(self, result):
        result = super().after_process(result)
        result = re.sub(r'[^\u4e00-\u9fff]', '', result)
        # 修正选项文本的常见错误
        return result