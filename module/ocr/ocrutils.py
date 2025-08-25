import re
import time
from typing import List, Tuple, Union
import cv2



import argparse

from loguru._logger import start_time

from module.base.button import Button, ButtonWrapper
from module.base.utils import float2str, crop
from module.logger import logger
from module.ocr.onnxocr.onnx_paddleocr import ONNXPaddleOcr
from tasks.ren_zhe_tiao_zhan.assets.assets_ren_zhe_tiao_zhan import MI_JING_TYPE


class Timer:
    """简单计时类"""
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.end_time = time.time()
        return self.elapsed()

    def elapsed(self):
        if self.start_time is None:
            return 0
        if self.end_time is None:
            return time.time() - self.start_time
        return self.end_time - self.start_time


class NumberUtils:
    """数字处理工具"""
    @staticmethod
    def extract_numbers(text: str) -> List[float]:
        import re
        return [float(x) for x in re.findall(r"\d+\.?\d*", text)]

    @staticmethod
    def extract_counter(text: str) -> Tuple[int, int]:
        """提取 X/X 格式"""
        import re
        match = re.match(r"(\d+)\s*/\s*(\d+)", text)
        if match:
            return int(match.group(1)), int(match.group(2))
        return 0, 0


class OCR:
    """OCR 封装类，支持 Button 区域"""
    def __init__(self, button: ButtonWrapper , use_angle_cls=True, use_gpu=False,name=None, **kwargs):
        """
        Args:
            button (Button): 如果传入 Button，则默认 OCR 该 Button 的 area 区域
        """
        if name is None:
            name = button.name
        self.button: ButtonWrapper = button
        self.name: str = name
        self.model = ONNXPaddleOcr(use_angle_cls=use_angle_cls, use_gpu=use_gpu, **kwargs)
    def pre_process(self, image):
        """
        Args:
            image (np.ndarray): Shape (height, width, channel)

        Returns:
            np.ndarray: Shape (width, height)
        """
        return image

    def after_process(self, result):
        """
        Args:
            result (str): '第二行'

        Returns:
            str:
        """

        return result

    def format_result(self, result):
        """
        Will be overriden.
        """
        return result

    def _log_change(self, attr, func, before):
        after = func(before)
        if after != before:
            logger.attr(f'{self.name} {attr}', f'{before} -> {after}')
        return after
    def _prepare_img(self, img, ocr_direct=False):
        """根据是否传入 Button 来裁剪图像"""
        if isinstance(img, str):
            img = cv2.imread(img)

        if self.button is not None and not ocr_direct:
            x1, y1, x2, y2 = self.button.area
            return img[y1:y2, x1:x2]

        return img

    def ocr_text(self, img, det=True, rec=True, cls=True, ocr_direct=False):
        """完整 OCR 识别，返回 TxtBox 列表"""
        img = self._prepare_img(img, ocr_direct)
        return self.model.ocr(img, det=det, rec=rec, cls=cls)

    def ocr_single_line(self, img, ocr_direct=False):
        """OCR 识别，返回纯文字列表"""
        start_time = time.time()
        img = self._prepare_img(img, ocr_direct)
        results = self.model.ocr(img, det=False, rec=True, cls=True)
        print(results)

        # 正确解析嵌套结构 [[('剩余挑战券：1', 0.9669168591499329)]]
        if isinstance(results, list) and len(results) > 0:
            result = results[0]  # 获取第一层列表
            if isinstance(result, list) and len(result) > 0:
                first_item = result[0]  # 获取第二层的第一个元素
                if isinstance(first_item, tuple) and len(first_item) > 0:
                    text_result = first_item[0]  # 提取元组中的文本部分
                else:
                    text_result = str(first_item)
            else:
                text_result = str(result)
        else:
            text_result = ""

        text_result = self._log_change('after', self.after_process, text_result)
        text_result = self._log_change('format', self.format_result, text_result)
        logger.attr(name='%s %ss' % (self.name, float2str(time.time() - start_time)),
                    text=str(text_result))
        return text_result

    def ocr_detect(self, img, ocr_direct=False):
        """只检测文字区域"""
        img = self._prepare_img(img, ocr_direct)
        return self.model.ocr(img, det=True, rec=False)

    def ocr_detect_region(self, img, region, ocr_direct=False):
        """检测指定区域文字"""
        if isinstance(img, str):
            img = cv2.imread(img)
        x1, y1, x2, y2 = region
        crop_img = img[y1:y2, x1:x2]
        return self.model.ocr(crop_img, det=True, rec=False)



class DigitOCR(OCR):
    def __init__(self, button: ButtonWrapper, lang='cn', name=None):
        super().__init__(button, lang=lang, name=name)
    def after_process(self, result):
        result = super().after_process(result)
        # 修正常见的数字识别错误
        result = result.replace('Bt', '3')
        result = result.replace('B', '3')
        return result

    def format_result(self, result) -> int:
        """
        Returns:
            int:
        """
        result = super().after_process(result)
        logger.attr(name=self.name, text=str(result))

        res = re.search(r'(\d+)', result)
        if res:
            return int(res.group(1))
        else:
            logger.warning(f'No digit found in {result}')
            return 0






