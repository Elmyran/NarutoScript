
from module.base.decorator import cached_property, del_cached_property
from module.ocr.onnxocr.onnx_paddleocr import ONNXPaddleOcr


class CustomOcrModel:
    def __init__(self):
        self._model = None

    @cached_property
    def model(self):
        return ONNXPaddleOcr(use_angle_cls=True, use_gpu=False)

    def resource_release(self):
        """释放OCR模型资源"""
        if hasattr(self, 'model') and self.model is not None:
            self.model.resource_release()
        del_cached_property(self, 'model')

    # 保持与原项目兼容的全局实例名称
OCR_MODEL = CustomOcrModel()