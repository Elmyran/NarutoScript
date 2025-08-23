import time
from typing import List, Tuple, Union
import cv2



import argparse

from module.base.button import Button
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
    def __init__(self, button: Button = None, use_angle_cls=True, use_gpu=False, **kwargs):
        """
        Args:
            button (Button): 如果传入 Button，则默认 OCR 该 Button 的 area 区域
        """
        self.button = button
        self.model = ONNXPaddleOcr(use_angle_cls=use_angle_cls, use_gpu=use_gpu, **kwargs)

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

    def ocr_single_line(self, img, det=True, rec=True, cls=True, ocr_direct=False):
        """OCR 识别，返回纯文字列表"""
        results = self.ocr_text(img, det=det, rec=rec, cls=cls, ocr_direct=ocr_direct)

        # results 可能是 [TxtBox,...] 或 [[TxtBox,...]]
        if len(results) > 0 and hasattr(results[0], "txt"):
            return [box.txt for box in results]
        elif len(results) > 0 and isinstance(results[0], list):
            return [box.txt for box in results[0]]
        return []

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










