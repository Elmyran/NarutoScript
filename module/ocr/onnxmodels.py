import threading 
import argparse
from module.base.decorator import cached_property, del_cached_property, has_cached_property
from module.logger import logger
from module.ocr.onnxocr.predict_system import TextSystem as TextSystem_
from module.ocr.onnxocr.utils import infer_args as init_args 
class TextSystem(TextSystem_):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_recognizer.rec_batch_num=1

class CustomOcrModel:
    box_tresh=None
    _model_init_thread = None

    @cached_property
    def model(self):

       # 默认参数
   
        parser = init_args()
        inference_args_dict = {action.dest: action.default for action in parser._actions}
        params = argparse.Namespace(**inference_args_dict)
        if  self.box_tresh is not  None: 
            params.drop_score = self.box_tresh
        # 修改默认参数
        params.rec_image_shape = "3, 48, 320"
        params.use_angle_cls = True

        # 初始化 TextSystem
        return TextSystem(params)
    def early_model_init(self):  
        """在任务开始时调用,在后台线程中预热模型"""  
        if has_cached_property(self, 'model'):  
            return  
        logger.info('Early custom ocr model init...') 
        def early_model_init_func():  
            model = self.model 
            try:
                import numpy as np
                dummy_img = np.zeros((48, 320, 3), dtype=np.uint8)
                _ = model.__call__(dummy_img)
                logger.info('Early custom ocr model init success.') 
            except Exception as e:
                logger.info('Early custom ocr model init failed.') 
  
        thread = threading.Thread(target=early_model_init_func, daemon=True)  
        self._model_init_thread = thread  
        thread.start()  
  
    @property  
    def model_ready(self):  
        """访问模型前等待预热完成"""  
        if self._model_init_thread is not None:  
            self._model_init_thread.join()
            self._model_init_thread = None 

        return self
    def resource_release(self):
        """释放OCR模型资源"""
        del_cached_property(self, 'model')

    # 保持与原项目兼容的全局实例名称
CUSTOM_OCR_MODEL = CustomOcrModel()