from module.ocr.ocr import Digit, DigitCounter, OcrWhiteLetterOnComplexBackground
from module.ocr.onnxocr.onnx_paddleocr import ONNXPaddleOcr
class StoreDetailOcr(ONNXPaddleOcr,OcrWhiteLetterOnComplexBackground):
    min_box = (1, 1)
    def after_process(self, result):
        return OcrWhiteLetterOnComplexBackground.after_process(self, result)
class StoreDigitCounter(DigitCounter):
    def after_process(self, result):  
        result = OcrWhiteLetterOnComplexBackground.after_process(self, result)
        return result

class StorePriceDigit(OcrWhiteLetterOnComplexBackground, Digit):  
    min_box = (1, 1)  # 确保小数字也能被检测到  
      
    def after_process(self, result):  
        result = OcrWhiteLetterOnComplexBackground.after_process(self, result)
        
        return result