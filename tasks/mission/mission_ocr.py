

from module.logger import logger
from module.ocr.ocr import Digit, Ocr, OcrResultButton, OcrWhiteLetterOnComplexBackground
from module.ocr.onnxocr.onnx_paddleocr import ONNXPaddleOcr


class MissionOcr(Ocr):
    def after_process(self, result):
        """对OCR结果进行修正"""
        result = super().after_process(result)
        if '领取' in result:
            result = '可领取'
        
        return result
    def matched_ocr(self, image, keyword_classes, direct_ocr=False, partial_match=False) -> list[OcrResultButton]:  
        results = self.detect_and_ocr(image, direct_ocr=direct_ocr)  
        
        if partial_match:  
            matched_results = []  
            if not isinstance(keyword_classes, list):  
                keyword_classes = [keyword_classes]  
                
            for result in results:  
                for keyword_class in keyword_classes:   
                        # 获取当前语言的关键词文本  
                        keyword_text = getattr(keyword_class, self.lang, '')  
                        if keyword_text and keyword_text in result.ocr_text:  
                            button = OcrResultButton(result, keyword_class)  
                            matched_results.append(button)  
                            break  # 找到匹配就跳出内层循环  
            results = matched_results  
        else:  
            results = [self._product_button(result, keyword_classes) for result in results]  
            results = [result for result in results if result.is_keyword_matched]  
    
        logger.attr(name=f'{self.name} matched', text=results)  
        return results
class MissionDigit(OcrWhiteLetterOnComplexBackground, Digit):  
    min_box = (1, 1)  # 确保小数字也能被检测到  
      
    def pre_process(self, img):  
        result = OcrWhiteLetterOnComplexBackground.pre_process(self, img)
        return result
    def after_process(self, result):
        return Digit.format_result(result)
class MissionWhiteLetterOcr(ONNXPaddleOcr,OcrWhiteLetterOnComplexBackground):
    def pre_process(self, img):
        return OcrWhiteLetterOnComplexBackground.pre_process(self, img)

