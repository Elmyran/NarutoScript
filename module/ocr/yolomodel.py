from module.base.decorator import cached_property, del_cached_property
from module.exception import ScriptError
from module.ocr.yolo import YOLO11


class YoloModel:
    def __init__(self, model_path="module/ocr/claim.onnx",
                 conf_thres=0.8, iou_thres=0.45,classes=None,intput_size=(640,640)):
        self.model_path = model_path
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres
        self.classes = None
        self.input_size = intput_size

    def get_model(self, model_path=None,classes=None,input_size=(640,640)):
        """返回模型对象，可以动态切换模型"""
        if model_path and model_path != self.model_path:
            self.input_size = input_size
            # 如果传入新模型路径，就替换掉旧模型
            self.model_path = model_path
            self.classes = classes
            self.resource_release()  # 删除旧的 cached_property
        return self.yolo_detector

    def resource_release(self):
        """释放模型资源"""
        del_cached_property(self, 'yolo_detector')

    @cached_property
    def yolo_detector(self):
        """延迟加载 YOLO 模型，只在首次调用时初始化"""
        try:
            detector = YOLO11(
                onnx_model=self.model_path,
                classes=self.classes,
                input_size=self.input_size
            )
            return detector
        except Exception as e:
            raise ScriptError(f'YOLO model initialization failed: {e}')


# 使用示例
YOLO_MODEL = YoloModel()


