from ultralytics import YOLO

from module.base.decorator import cached_property, del_cached_property
from module.exception import ScriptError
class YoloModel:
    def get_model(self):
        return self.yolo_detector

    def resource_release(self):
        """释放模型资源"""
        del_cached_property(self, 'yolo_detector')

    @cached_property
    def yolo_detector(self):
        """
        延迟加载 YOLO 模型，只在首次调用时初始化
        """
        try:
            model=YOLO('module/ocr/best.pt').to("cpu")
            return model
        except Exception as e:
            raise ScriptError(f'YOLO model initialization failed: {e}')
YOLO_MODEL = YoloModel()