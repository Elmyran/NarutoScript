from module.logger import logger
from module.ocr.ocr import Digit, Ocr

import re
import cv2

class MiJingOcr(Ocr):
    def after_process(self, result: str) -> str:
        result=result.replace("垂","雷")
        result=result.replace("雸","雷")
        result=result.replace("淀","境")
        result=result.replace("密","秘")
        result=result.replace("霆霆","雷霆")
        result=result.replace("雪","雷")
        result=result.replace("显","罡")
        result=result.replace("宰","牢")
        return super().after_process(result)
class MiJingDigit(Digit):
    
    def pre_process(self, image):
        image=cv2.resize(image, (800, 600))
        return super().pre_process(image)
    def after_process(self, result):
        result=super().after_process(result)
        return result
    def format_result(self, result):
        result = super().after_process(result)
        logger.attr(name=self.name, text=str(result))

        res = re.search(r'(\d+)', result)
        if res:
            num=int(res.group(1))
            if num > 35:
                logger.warning(f'Wrong digit detected in {result}')
                return 0
            return num
        else:
            logger.warning(f'No digit found in {result}')
            return 0