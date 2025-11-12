from module.ocr.ocr import Digit, Ocr
from module.ocr.onnxocr.onnx_paddleocr import ONNXPaddleOcr


class MiJingOcr(Ocr):
    def after_process(self, result: str) -> str:
        result=result.replace("垂","雷")
        result=result.replace("雸","雷")
        result=result.replace("淀","境")
        result=result.replace("密","秘")
        result=result.replace("霆霆","雷霆")
        result=result.replace("显","罡")
        result=result.replace("宰","牢")
        return super().after_process(result)
class MiJingDigit(ONNXPaddleOcr,Digit):
    def after_process(self, result):
        result=super().after_process(result)
        if int(result) > 35:  
            return '0'  
        return result
    def format_result(self, result):
        return Digit.format_result(self, result)