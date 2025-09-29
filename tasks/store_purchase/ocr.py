from module.ocr.ocr import Digit, DigitCounter, OcrWhiteLetterOnComplexBackground
from module.ocr.onnxocr.onnx_paddleocr import ONNXPaddleOcr
class StoreDetailOcr(ONNXPaddleOcr,OcrWhiteLetterOnComplexBackground):
    min_box = (1, 1)
    def pre_process(self, result):
        return OcrWhiteLetterOnComplexBackground.pre_process(self, result)
class StoreDigitCounter(DigitCounter):
    def after_process(self, result):  
        return super().after_process(result)

class StorePriceDigit(OcrWhiteLetterOnComplexBackground, Digit):  
    min_box = (1, 1)  # 确保小数字也能被检测到  
      
    def pre_process(self, result):  
        result = OcrWhiteLetterOnComplexBackground.pre_process(self, result)
        return result
    def after_process(self, result):  
        return Digit.format_result(self, result)