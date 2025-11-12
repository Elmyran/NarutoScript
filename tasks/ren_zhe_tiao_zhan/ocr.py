from module.logger import logger
from module.ocr.ocr import Digit, Ocr
from module.ocr.onnxocr.onnx_paddleocr import ONNXPaddleOcr


class MiJingOcr(Ocr):
    def __init__(self, button, lang='cn', name=None):
        super().__init__(button, lang=lang, name=name)
        self.correction_map = {
            "垂霆秘境": "雷霆秘境",
            "雸霆秘境": "雷霆秘境",
            "雷霆秘淀": "雷霆秘境",
            "雷霆密境": "雷霆秘境",
            "霆霆秘境": "雷霆秘境",
            "显体秘境": "罡体秘境",
            "水宰秘境":"水牢秘境"
        }

    def after_process(self, result: str) -> str:
        if result in self.correction_map:
            corrected = self.correction_map[result]
            logger.attr(f"{self.name} correction", f"{result} -> {corrected}")
            return corrected
        target = "雷霆秘境"
        if len(result) == len(target):
            diff = sum(1 for a, b in zip(result, target) if a != b)
            if diff <= 1: 
                logger.attr(f"{self.name} correction", f"{result} -> {target}")
                return target

        return super().after_process(result)
class MiJingDigit(ONNXPaddleOcr,Digit):
    def after_process(self, result):
        result=super().after_process(result)
        if int(result) > 35:  
            return '0'  
        return result
    def format_result(self, result):
        return Digit.format_result(self, result)