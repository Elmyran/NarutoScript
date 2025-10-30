from module.ocr.ocr import  Digit, DigitCounter,OcrWhiteLetterOnComplexBackground
import re

from module.ocr.onnxocr.onnx_paddleocr import ONNXPaddleOcr
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

class StorePriceDigit(ONNXPaddleOcr,Digit,OcrWhiteLetterOnComplexBackground):  
    def after_process(self, result):  
        result=result.replace('A', '')
        result = re.sub(r'^11(000)$', r'1\1', result) 
        return result
    def pre_process(self, img):
        return OcrWhiteLetterOnComplexBackground.pre_process(self, img)
    

    def format_result(self, result):
        return Digit.format_result(self,result)