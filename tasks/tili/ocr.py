import re

from module.logger import logger
from module.ocr.ocr import DigitCounter, OcrWhiteLetterOnComplexBackground


class TiLiOcr(OcrWhiteLetterOnComplexBackground,DigitCounter):
    # 降低检测阈值以提高敏感度
    box_thresh = 0.05
    # 设置最小框大小确保小数字能被检测到
    min_box = (12, 16)
    def pre_process(self, image):
        # 先应用白色字母提取
        image = super().pre_process(image)
        return image
    def after_process(self, result):
        result = super().after_process(result)
        logger.info(f"Raw OCR result: '{result}'")
        result = re.sub(r'获取途径', '', result)  # 移除"获取途径"文本
        result = re.sub(r'双途径', '', result)   # 移除"双途径"文本
        result = re.sub(r'[：:]', '', result)   # 移除冒号


        return result
class StuffOcr(OcrWhiteLetterOnComplexBackground,DigitCounter):
    # 降低检测阈值以提高敏感度
    box_thresh = 0.05
    # 设置最小框大小确保小数字能被检测到
    min_box = (12, 16)
    def pre_process(self, image):
        # 先应用白色字母提取
        image = super().pre_process(image)
        return image
    def after_process(self, result):
        result = super().after_process(result)
        logger.info(f"Raw OCR result: '{result}'")
        result = re.sub(r'V', '/', result)
        result = re.sub(r'(\d)1(\d+)$', r'\1/\2', result)



        return result