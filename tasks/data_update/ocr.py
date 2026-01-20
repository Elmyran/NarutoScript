import re

from module.logger import logger
from module.ocr.ocr import Digit, OcrWhiteLetterOnComplexBackground


class DataDigit(Digit,OcrWhiteLetterOnComplexBackground):
    def after_process(self, result):
        result = re.sub(r'[l|]', '1', result)
        result = re.sub(r'[oO]', '0', result)
        return super().after_process(result)
    def format_result(self, result) -> int:
        """
        将带有万、亿后缀的中文数字转换为纯数字
        """

        if '万' in result:
            match = re.search(r'([\d.]+)万', result)
            if match:
                number = float(match.group(1))
                return int(number * 10000)
        if '亿' in result:
            match = re.search(r'([\d.]+)亿', result)
            if match:
                number = float(match.group(1))
                return int(number * 100000000)
        return super().format_result(result)