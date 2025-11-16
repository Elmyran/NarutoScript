from module.ocr.onnxocr.onnx_paddleocr import ONNXPaddleOcr


class JiFenSaiOcr(ONNXPaddleOcr):
    def after_process(self, result):
        return super().after_process(result)
    