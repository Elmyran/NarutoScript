
import argparse
from module.base.decorator import cached_property, del_cached_property
from module.ocr.onnxocr.predict_system import TextSystem as TextSystem_
from module.ocr.onnxocr.utils import infer_args as init_args 
class TextSystem(TextSystem_):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_recognizer.rec_batch_num=1

class CustomOcrModel:
   

    @cached_property
    def model(self):
         # 默认参数
       # 默认参数
   
        parser = init_args()
        inference_args_dict = {action.dest: action.default for action in parser._actions}
        params = argparse.Namespace(**inference_args_dict)

        # 修改默认参数
        params.rec_image_shape = "3, 48, 320"
        params.use_angle_cls = True

        # 初始化 TextSystem
        return TextSystem(params)

    def resource_release(self):
        """释放OCR模型资源"""
        del_cached_property(self, 'model')

    # 保持与原项目兼容的全局实例名称
CUSTOM_OCR_MODEL = CustomOcrModel()