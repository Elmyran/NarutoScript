import cv2
from module.ocr.ocr import  Digit, DigitCounter, OcrWhiteLetterOnComplexBackground
import re

class StoreDetailOcr(OcrWhiteLetterOnComplexBackground):
    min_box = (1, 1)
    def after_process(self, result):
        result=result.replace('砖', '卷')
        if '高级通灵' in result:
            result='高级通灵卷轴碎片'
        return super().after_process(result)
class StoreDigitCounter(DigitCounter): 
    def after_process(self, result):  
        result=result.replace('早','限')
        return super().after_process(result)

class StorePriceDigit(Digit,OcrWhiteLetterOnComplexBackground):  
    def after_process(self, result):  
        result=result.replace('A', '')
        result = re.sub(r'^11(000)$', r'1\1', result) 
        if '万' in result:
            match = re.search(r'(\d+)万', result)  
            if match:  
                num = int(match.group(1))  
                # 乘以10000  
                result = result.replace(match.group(0), str(num * 10000))
        return result
    def pre_process(self, img):
        return OcrWhiteLetterOnComplexBackground.pre_process(self, img)
    

    def format_result(self, result):
        return Digit.format_result(self,result)