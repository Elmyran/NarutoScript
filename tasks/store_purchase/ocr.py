from module.ocr.ocr import Digit, OcrWhiteLetterOnComplexBackground


class StorePriceDigit(OcrWhiteLetterOnComplexBackground, Digit):  
    min_box = (1, 1)  # 确保小数字也能被检测到  
      
    def after_process(self, result):  
        result = super(OcrWhiteLetterOnComplexBackground, self).after_process(result)  
        
        return result