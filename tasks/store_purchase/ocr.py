from module.ocr.ocr import Digit, DigitCounter, OcrWhiteLetterOnComplexBackground
from module.ocr.onnxocr.onnx_paddleocr import ONNXPaddleOcr
class StoreDetailOcr(ONNXPaddleOcr,OcrWhiteLetterOnComplexBackground):
    min_box = (1, 1)
    def pre_process(self, img):
        return OcrWhiteLetterOnComplexBackground.pre_process(self, img)
class StoreDigitCounter(DigitCounter):
    def after_process(self, result):  
        return super().after_process(result)

class StorePriceDigit(ONNXPaddleOcr, OcrWhiteLetterOnComplexBackground,Digit):  
    min_box = (1, 1)  # 确保小数字也能被检测到  
      
    def pre_process(self, result):  
        result = OcrWhiteLetterOnComplexBackground.pre_process(self, result)
        return result
    def format_result(self, result):
        return Digit.format_result(self,result)