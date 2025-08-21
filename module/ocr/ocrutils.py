import time
from typing import List, Tuple, Union
import cv2
from PIL import Image

from .predict_system import TextSystem
from .utils import infer_args as init_args
from .utils import draw_ocr
import argparse


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
    """OCR 封装类"""
    def __init__(self, use_angle_cls=True, use_gpu=False, **kwargs):
        parser = init_args()
        inference_args_dict = {action.dest: action.default for action in parser._actions}
        params = argparse.Namespace(**inference_args_dict)
        params.rec_image_shape = "3, 48, 320"
        params.__dict__.update(**kwargs)
        self.model = ONNXPaddleOcr(use_angle_cls=use_angle_cls, use_gpu=use_gpu, **params.__dict__)

    def ocr_text(self, img: Union[str, 'np.ndarray'], det=True, rec=True, cls=True):
        """完整 OCR 识别"""
        if isinstance(img, str):
            img = cv2.imread(img)
        return self.model.ocr(img, det=det, rec=rec, cls=cls)

    def ocr_text_region(self, img: Union[str, 'np.ndarray'], region: Tuple[int, int, int, int]):
        """识别图像指定区域文字"""
        if isinstance(img, str):
            img = cv2.imread(img)
        x1, y1, x2, y2 = region
        crop_img = img[y1:y2, x1:x2]
        return self.model.ocr(crop_img)

    def ocr_detect(self, img: Union[str, 'np.ndarray']):
        """只检测文字区域"""
        if isinstance(img, str):
            img = cv2.imread(img)
        return self.model.ocr(img, det=True, rec=False)

    def ocr_detect_region(self, img: Union[str, 'np.ndarray'], region: Tuple[int, int, int, int]):
        """只检测指定区域文字"""
        if isinstance(img, str):
            img = cv2.imread(img)
        x1, y1, x2, y2 = region
        crop_img = img[y1:y2, x1:x2]
        return self.model.ocr(crop_img, det=True, rec=False)




# Example usage
if __name__ == "__main__":
    ocr_tool = OCR(use_angle_cls=True, use_gpu=False)
    img_path = "/data2/liujingsong3/fiber_box/test/img/20230531230052008263304.jpg"

    timer = Timer()
    timer.start()
    result = ocr_tool.ocr_text(img_path)
    print("OCR result:", result)
    print("Elapsed time: {:.3f}s".format(timer.stop()))

    # 保存结果
    ocr_tool.save_result_image(cv2.imread(img_path), result)

    # 数字提取示例
    for line in result[0]:
        text = line[1][0]
        numbers = NumberUtils.extract_numbers(text)
        counter = NumberUtils.extract_counter(text)
        print(f"text: {text}, numbers: {numbers}, counter: {counter}")
