
import os

from module.base.decorator import cached_property, del_cached_property
from module.logger import logger


import onnxruntime as ort
from rapidocr import EngineType, ModelType, RapidOCR


# 以本文件位置定位模型目录, 与运行时工作目录无关
_MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'models'))
ppocrv6_small_det_onnx = os.path.join(_MODEL_DIR, 'ppocrv6_small_det.onnx')
ppocrv6_small_rec_onnx = os.path.join(_MODEL_DIR, 'ppocrv6_small_rec.onnx')
ppocrv6_small_rec_keys_path = os.path.join(_MODEL_DIR, 'dict.txt')


def _is_dml_available() -> bool:
    """检测 DirectML 是否可用。"""
    try:
        available = ort.get_available_providers()
        return 'DmlExecutionProvider' in available
    except Exception:
        return False


class OcrModel:
    def resource_release(self):
        del_cached_property(self, 'ch')
        del_cached_property(self, 'rec')

    @cached_property
    def ch(self):
        use_dml = _is_dml_available()
        logger.info(f'DML available: {use_dml}')
        return RapidOCR(params={
            "Global.min_side_len": 1,
            "EngineConfig.onnxruntime.use_dml": use_dml,
            "Det.model_path": ppocrv6_small_det_onnx,
            "Rec.model_path": ppocrv6_small_rec_onnx,
            "Rec.rec_keys_path": ppocrv6_small_rec_keys_path,
            "Det.engine_type": EngineType.ONNXRUNTIME,
            "Rec.engine_type": EngineType.ONNXRUNTIME,
        })

    @cached_property
    def rec(self):
        use_dml = _is_dml_available()
        logger.info(f'DML available: {use_dml}')
        return RapidOCR(params={
            'Global.use_det': False,
            'Global.use_cls': False,
            "Global.min_side_len": 1,
            "EngineConfig.onnxruntime.use_dml": use_dml,
            "Rec.model_path": ppocrv6_small_rec_onnx,
            "Rec.rec_keys_path": ppocrv6_small_rec_keys_path,
            "Rec.engine_type": EngineType.ONNXRUNTIME,
        })

 
OCR_MODEL = OcrModel()
