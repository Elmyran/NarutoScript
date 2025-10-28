import re
from module.logger import logger
from module.ocr.ocr import DigitCounter, OcrWhiteLetterOnComplexBackground


class TiLiOcr(OcrWhiteLetterOnComplexBackground,DigitCounter):
    box_thresh = 0.05
    min_box = (12, 16)
    def pre_process(self, image):
        image = super().pre_process(image)
        return image
    def after_process(self, result):
        result = super().after_process(result)
        logger.info(f"Raw OCR result: '{result}'")
        result = re.sub(r'获取途径', '', result)  
        result = re.sub(r'双途径', '', result)  
        result = re.sub(r'[：:]', '', result) 


        return result
class StuffOcr(OcrWhiteLetterOnComplexBackground,DigitCounter):
    box_thresh = 0.05
    min_box = (12, 16)
    def pre_process(self, image):
        image = super().pre_process(image)
        return image
    def after_process(self, result):
        result = super().after_process(result)
        result = re.sub(r'V', '/', result)
        result = re.sub(r'(\d)1(\d+)$', r'\1/\2', result)
        result=result.replace('装', '荡')
        result=result.replace('满', '荡')
        result=result.replace('芳', '荡')
        result=result.replace('荐', '荡')
        result=result.replace('关', '荡')
        


        return result