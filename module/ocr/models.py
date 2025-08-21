import numpy as np
from pponnxcr.predict_system import BoxedResult

from module.ocr.onnxocr.onnx_paddleocr import ONNXPaddleOcr
from module.ocr.onnxocr.predict_system import  TextSystem as TextSystem_

from module.base.decorator import cached_property, del_cached_property
from module.exception import ScriptError

DIC_LANG_TO_MODEL = {
    'cn': 'zhs',
    'en': 'en',
    'jp': 'ja',
    'tw': 'zht',
}


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


class TextSystem:
    def __init__(self, lang='zhs'):
        # 使用您的ONNXPaddleOcr
        self.paddle_ocr = ONNXPaddleOcr(lang=lang,use_angle_cls=True, use_gpu=False)
    def ocr_single_line(self, image):
        """适配StarRailCopilot的ocr_single_line接口"""
        result = self.ocr_lines([image])
        if result and result[0]:
            return result[0]  # 返回(text, score)元组
        return ("", 0.0)

    def ocr_lines(self, image_list):
        """处理多行图像的OCR识别"""
        results = []
        for image in image_list:
            ocr_result = self.paddle_ocr.ocr(image, det=True, rec=True, cls=True)
            if ocr_result and ocr_result[0] and len(ocr_result[0]) > 0:
                # 取置信度最高的结果
                best_result = max(ocr_result[0], key=lambda x: x[1][1])
                text, score = best_result[1]
                results.append((text, score))
            else:
                results.append(("", 0.0))
        return results
    def detect_and_ocr(self, image):
        result = self.paddle_ocr.ocr(image, det=True, rec=True, cls=True)
        boxed_results = []
        if result and result[0]:
            for item in result[0]:
                box = item[0]  # [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
                text = item[1][0]
                score = item[1][1]

                # Store as numpy array in the exact format corner2area expects
                if isinstance(box, list) and len(box) == 4:
                    # Convert to numpy array with shape (4, 2)
                    corner_array = np.array([[float(point[0]), float(point[1])] for point in box])

                    from pponnxcr.predict_system import BoxedResult
                    boxed_result = BoxedResult(
                        box=corner_array,  # Use numpy array format
                        text_img=None,
                        ocr_text=text,
                        score=score
                    )
                    boxed_results.append(boxed_result)

        return boxed_results

class OcrModel:
    def get_by_model(self, model: str) -> TextSystem:
        try:
            return self.__getattribute__(model)
        except AttributeError:
            raise ScriptError(f'OCR model "{model}" does not exists')

    def get_by_lang(self, lang: str) -> TextSystem:
        try:
            model = lang2model(lang)
            return self.__getattribute__(model)
        except AttributeError:
            raise ScriptError(f'OCR model under lang "{lang}" does not exists')

    def resource_release(self):
        del_cached_property(self, 'zhs')
        del_cached_property(self, 'en')
        del_cached_property(self, 'ja')
        del_cached_property(self, 'zht')

    @cached_property
    def zhs(self):
        return TextSystem('zhs')

    @cached_property
    def en(self):
        return TextSystem('en')

    @cached_property
    def ja(self):
        return TextSystem('ja')

    @cached_property
    def zht(self):
        return TextSystem('zht')


OCR_MODEL = OcrModel()
