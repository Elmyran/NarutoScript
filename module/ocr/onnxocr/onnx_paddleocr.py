import time
import cv2
import re

from module.base.base import ModuleBase
from module.base.button import ButtonWrapper, Button
from module.base.utils import area2corner, corner2area, area_in_area
from module.device.method.utils import HierarchyButton
from tasks.mission.priority import TaskPriority
from .predict_system import TextSystem
from .utils import infer_args as init_args
from .utils import str2bool, draw_ocr
import argparse
import sys
from module.base.decorator import cached_property, del_cached_property
class TxtBox:
    def __init__(self,button,txt,threadhold,time=None,soul_jade=None,box_type=None):
        self.area=corner2area(button)
        self.button=corner2area(button)
        self.txt=txt
        self.time=time
        self.soul_jade=soul_jade
        self.box_type:TaskPriority=box_type
        self.threadhold=threadhold
    def __repr__(self):
        """定义对象的字符串表示形式"""
        return f"TxtBox(txt='{self.txt}', conf={self.threadhold:.4f}, area={self.area}， button={self.button}， time={self.time})"


class ONNXPaddleOcr(TextSystem,ModuleBase):
    def __init__(self, **kwargs):
        # 默认参数
        parser = init_args()
        inference_args_dict = {}
        for action in parser._actions:
            inference_args_dict[action.dest] = action.default
        params = argparse.Namespace(**inference_args_dict)
        # params.rec_image_shape = "3, 32, 320"
        params.rec_image_shape = "3, 48, 320"
        # 根据传入的参数覆盖更新默认参数
        params.__dict__.update(**kwargs)

        # 初始化模型
        super().__init__(params)

    def resource_release(self):
        """
        释放OCR模型占用的资源
        """
        # 释放文本检测器资源
        if hasattr(self, 'text_detector') and self.text_detector is not None:
            if hasattr(self.text_detector, 'predictor'):
                del self.text_detector.predictor
            del self.text_detector
            self.text_detector = None

            # 释放文本识别器资源
        if hasattr(self, 'text_recognizer') and self.text_recognizer is not None:
            if hasattr(self.text_recognizer, 'predictor'):
                del self.text_recognizer.predictor
            del self.text_recognizer
            self.text_recognizer = None

            # 释放角度分类器资源
        if hasattr(self, 'text_classifier') and self.text_classifier is not None:
            if hasattr(self.text_classifier, 'predictor'):
                del self.text_classifier.predictor
            del self.text_classifier
            self.text_classifier = None

            # 强制垃圾回收
        import gc
        gc.collect()
    def ocr(self, img, det=True, rec=True, cls=True):

        if cls == True and self.use_angle_cls == False:
            print(
                "Since the angle classifier is not initialized, the angle classifier will not be uesd during the forward process"
            )

        if det and rec:
            ocr_res = []
            dt_boxes, rec_res = self.__call__(img, cls)
            tmp_res = [[box.tolist(), res] for box, res in zip(dt_boxes, rec_res)]
            ocr_res.append(tmp_res)
            return resultToBox(ocr_res)
        elif det and not rec:
            ocr_res = []
            dt_boxes = self.text_detector(img)
            tmp_res = [box.tolist() for box in dt_boxes]
            ocr_res.append(tmp_res)
            return resultToBox(ocr_res)
        else:
            ocr_res = []
            cls_res = []

            if not isinstance(img, list):
                img = [img]
            if self.use_angle_cls and cls:
                img, cls_res_tmp = self.text_classifier(img)
                if not rec:
                    cls_res.append(cls_res_tmp)
            rec_res = self.text_recognizer(img)
            ocr_res.append(rec_res)

            if not rec:
                return resultToBox(cls_res)
            return ocr_res

    # OCR关键词过滤
    def matchKeys(self,boxes,keys):
        """
        :param boxes: TxtBoxList(ocr results)
        :param keys: keys to filter ocr results
        :return:
        """
        if not isinstance(keys, list):
            keys = [keys]
        boxes_matched_keys = []
        if not boxes  or not keys :
            return boxes_matched_keys
        for box in boxes:
            for key in keys:
                if box.txt==key:
                    boxes_matched_keys.append(box)
                    break
        return boxes_matched_keys
    def matchArea(self,boxes,area):
        matched_boxes = []
        if not boxes:
            return matched_boxes
        for box in boxes:
            if area_in_area(box.button,area):
                matched_boxes.append(box)
        return matched_boxes
    def matchTime(self,boxes):
        boxes_matched_time=[]
        if not boxes:
            return boxes_matched_time
        pattern=r'(0?[0-9]|1[0-9]|2[0-3])时([0-5]?[0-9])分'
        for box in boxes:
            if re.search(pattern,box.txt):
                boxes_matched_time.append(box)
        return boxes_matched_time
    def ocr_with_area(self, img, button=None):
        area = button
        if isinstance(button, (Button, ButtonWrapper)):
            area = button.area

        image = img  # img is already a numpy array

        # Crop the region of interest
        x1, y1, x2, y2 = area
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(image.shape[1], x2), min(image.shape[0], y2)
        roi = image[y1:y2, x1:x2]  # Keep original 3-channel format

        # Use the original ROI for OCR (maintains 3 channels)
        result = self.ocr(roi)
        return result

# 创建全局OCR模型实例
class CustomOcrModel:
    def __init__(self):
        self._model = None

    @cached_property
    def model(self):
        return ONNXPaddleOcr(use_angle_cls=True, use_gpu=False)

    def resource_release(self):
        """释放OCR模型资源"""
        if hasattr(self, '_model') and self._model is not None:
            self._model.resource_release()
        del_cached_property(self, 'model')
    # 全局OCR模型实例
CUSTOM_OCR_MODEL = CustomOcrModel()
def resultToBox(result):
    """
    :param result: ocr method result
    :return: TxtBox list
    """
    box=[]
    if result is None:
        return box
    items=result[0]
    for item in items:
        area=item[0]
        txt=item[1]
        box.append(TxtBox(button=area,txt=txt[0],threadhold=txt[1]))

    return box


def sav2Img(org_img, result, name="draw_ocr.jpg"):
    # 显示结果
    from PIL import Image

    result = result[0]
    # image = Image.open(img_path).convert('RGB')
    # 图像转BGR2RGB
    image = org_img[:, :, ::-1]
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    scores = [line[1][1] for line in result]
    im_show = draw_ocr(image, boxes, txts, scores)
    im_show = Image.fromarray(im_show)
    im_show.save(name)


if __name__ == "__main__":
    import cv2

    model = ONNXPaddleOcr(use_angle_cls=True, use_gpu=False)

    img = cv2.imread(
        "/data2/liujingsong3/fiber_box/test/img/20230531230052008263304.jpg"
    )
    s = time.time()
    result = model.ocr(img)
    e = time.time()
    print("total time: {:.3f}".format(e - s))
    print("result:", result)
    for box in result[0]:
        print(box)

    sav2Img(img, result)