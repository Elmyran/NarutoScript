from module.logger import logger
from module.ocr.ocr import  Digit, DigitCounter, Ocr, OcrResultButton, OcrWhiteLetterOnComplexBackground
import cv2

import re

from module.ocr.ocr import BoxedResult
class MissionDurationOcr(Ocr):
    def pre_process(self, image):
        return image
    def after_process(self, result):
        """对OCR结果进行修正"""
        result = super().after_process(result)
        if '领取' in result:
            result = '可领取'
        
        return result
    
class MissionDigit(Digit,OcrWhiteLetterOnComplexBackground):  
    
    def filter_detected(self, result: BoxedResult) -> bool:  
        """  
        过滤掉不包含数字的 OCR 结果  
        """  
        # 只保留包含数字的结果  
        print("OCR 结果:", result.ocr_text)
        return bool(re.search(r'\d', result.ocr_text))
    def pre_process(self, image):
 

        return OcrWhiteLetterOnComplexBackground.pre_process(self, image)
    
    def format_result(self, result):  

        return Digit.format_result(self, result)  
    
    
class MissionWhiteLetterOcr(OcrWhiteLetterOnComplexBackground):
    def pre_process(self, image):
    

        
        
      

        return image
class MissionCounter(DigitCounter):
    def pre_process(self, image):
        height, width, _ = image.shape
        min_size = 640
        
        if height < min_size or width < min_size:
           
            top = max(0, (min_size - height) // 2)
            bottom = max(0, min_size - height - top)
            left = max(0, (min_size - width) // 2)
            right = max(0, min_size - width - left)

            
            background_color = [int(x) for x in image[0, 0]]

            image = cv2.copyMakeBorder(
                image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=background_color
            )
        return super().pre_process(image)
    

