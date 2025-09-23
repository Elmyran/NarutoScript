
from module.base.button import ButtonWrapper
from module.ocr.ocr import Ocr


class MissionOcr(Ocr):
    
    def after_process(self, result):
        """对OCR结果进行修正"""
        result = super().after_process(result)
        if '领取' in result:
            result = '已领取'
        
      
        return result
