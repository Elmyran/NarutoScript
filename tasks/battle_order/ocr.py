from module.ocr.ocr import Digit
from module.ocr.onnxocr.onnx_paddleocr import ONNXPaddleOcr


class BattleOrderOcr(ONNXPaddleOcr,Digit):
    def format_result(self, result):
        return Digit.format_result(self, result)
