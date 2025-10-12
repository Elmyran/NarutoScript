

from module.ocr.onnxocr.onnx_paddleocr import ONNXPaddleOcr


class TaskTabOcr(ONNXPaddleOcr):
    def after_process(self, result):
        result=result.replace('装','袭')
        result=result.replace('秋','秘')

        return super().after_process(result)
