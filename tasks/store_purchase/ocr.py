from module.ocr.ocr import Digit, DigitCounter, OcrWhiteLetterOnComplexBackground
from module.ocr.onnxocr.onnx_paddleocr import ONNXPaddleOcr
import re
class StoreDetailOcr(ONNXPaddleOcr,OcrWhiteLetterOnComplexBackground):
    min_box = (1, 1)
    def pre_process(self, img):
        return OcrWhiteLetterOnComplexBackground.pre_process(self, img)
class StoreDigitCounter(DigitCounter):
    def after_process(self, result):  
        return super().after_process(result)

class StorePriceDigit(ONNXPaddleOcr,Digit):  

      

    def after_process(self, result):  
        result=result.replace('A', '')
        result = re.sub(r'^11(000)$', r'1\1', result) 
        return result
    def format_result(self, result):
        return Digit.format_result(self,result)