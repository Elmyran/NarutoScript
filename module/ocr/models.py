
from module.base.decorator import cached_property, del_cached_property, has_cached_property
from module.exception import ScriptError
from module.logger import logger


import onnxruntime as ort
from rapidocr import EngineType, LangDet, ModelType, OCRVersion, RapidOCR,LangRec
DIC_LANG_TO_MODEL = {
    'cn': 'ch',
    'en': 'en',
    'jp': 'japan',
    'tw': 'cht',
}


def _is_dml_available() -> bool:
    """检测 DirectML 是否可用。"""
    try:
        available = ort.get_available_providers()
        return 'DmlExecutionProvider' in available
    except Exception:
        return False


def lang2model(lang: str) -> str:
    """
    Args:
        lang: In-game language name, defined in VALID_LANG

    Returns:
        str: Model name, defined in pponnxcr.utility
    """
    return DIC_LANG_TO_MODEL.get(lang, lang)


def model2lang(model: str) -> str:
    """
    Args:
        model: Model name, defined in pponnxcr.utility

    Returns:
        str: In-game language name, defined in VALID_LANG
    """
    for k, v in DIC_LANG_TO_MODEL.items():
        if model == v:
            return k
    return model


class TextSystem(RapidOCR):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       


class OcrModel:
    _model_init_thread = None
    def get_by_model(self, model: str) -> RapidOCR:
        try:
            return self.__getattribute__(model)
        except AttributeError:
            raise ScriptError(f'OCR model "{model}" does not exists')

    def get_by_lang(self, lang: str) -> RapidOCR:
        try:
            model = lang2model('cn')
            return self.__getattribute__(model)
        except AttributeError:
            raise ScriptError(f'OCR model under lang "{lang}" does not exists')

    def resource_release(self):
        del_cached_property(self, 'ch')
        del_cached_property(self, 'en')
        del_cached_property(self, 'japan')
        del_cached_property(self, 'cht')

    @cached_property
    def ch(self):
        use_dml = _is_dml_available()
        logger.info(f'DML available: {use_dml}')
        params={
        "EngineConfig.onnxruntime.use_dml": use_dml,
        "EngineConfig.enable_cpu_mem_arena": True,
        "Det.ocr_version": OCRVersion.PPOCRV4,
        "Det.engine_type": EngineType.ONNXRUNTIME,
        "Det.lang_type": LangDet.CH,
        "Det.unclip_ratio": 1.9,
        "Det.box_thresh": 0.5,
        "Global.max_side_len": 2000,
        "Global.text_score": 0.5,
        "Det.model_type": ModelType.MOBILE,
        "Rec.ocr_version": OCRVersion.PPOCRV5


        
    }
        return RapidOCR(params=params)

    @cached_property
    def en(self):
        use_dml = _is_dml_available()
        params={
         "EngineConfig.onnxruntime.use_dml": use_dml,
        "EngineConfig.enable_cpu_mem_arena": True,
        "Det.engine_type": EngineType.ONNXRUNTIME,
        "Det.lang_type": LangDet.EN,
        "Det.model_type": ModelType.MOBILE,
        "Det.ocr_version": OCRVersion.PPOCRV5
    }
        return RapidOCR(params=params)

    @cached_property
    def japan(self):
        params={
        "Det.engine_type": EngineType.ONNXRUNTIME,
        "Det.lang_type": LangDet.MULTI,
        "Det.model_type": ModelType.MOBILE,
        "Det.ocr_version": OCRVersion.PPOCRV4
    }
        return RapidOCR(params=params)

    @cached_property
    def cht(self):
        params={
        "Det.engine_type": EngineType.ONNXRUNTIME,
        "Det.lang_type": LangDet.MULTI,
        "Det.model_type": ModelType.MOBILE,
        "Det.ocr_version": OCRVersion.PPOCRV4
    }
        return RapidOCR(params=params)

  


OCR_MODEL = OcrModel()