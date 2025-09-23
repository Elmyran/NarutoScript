
import cv2
import numpy as np
import onnxruntime as ort
from module.logger import logger
# 类外定义类别映射关系
CLASS_NAMES = {
    0: 'claimable',
    1: 'unclaim',
    2: 'claimed'
}
class YoloResult:
    def __init__(self, box, score, class_id, image, classes=None):
        self.box = box
        self.score = score
        self.class_id = class_id
        self.image = image
        
        self.classes = classes if classes is not None else {0:'claimable',1:'unclaim',2:'claimed'}
        

    def __repr__(self):
        x1, y1, w, h = self.box
        cls_name = self.classes.get(self.class_id, f'cls{self.class_id}')
        return f"[{cls_name} | Conf: {self.score:.2f} | BBox: ({x1},{y1},{w},{h})]"
class YOLO11:
    """YOLO11 目标检测模型类，可动态传入类别映射。"""
    def __init__(self, onnx_model, classes=None, confidence_thres=0.8, iou_thres=0.45,input_size=(640,640)):
        """
        初始化 YOLO11 类的实例。
        参数：
            onnx_model: ONNX 模型路径
            classes: dict {id: name}，类别映射，可选
            confidence_thres: 置信度阈值
            iou_thres: NMS阈值
        """
        self.onnx_model = onnx_model
        self.confidence_thres = confidence_thres
        self.iou_thres = iou_thres
        self.input_size = input_size
        # 类别映射，可自定义
        if classes is None:
            self.classes = {0: 'claimable', 1: 'unclaim', 2: 'claimed'}
        else:
            self.classes = classes

        self.color_palette = np.random.uniform(0, 255, size=(len(self.classes), 3))
        available_providers = ort.get_available_providers()
        local_provider = []
        if 'DmlExecutionProvider' in available_providers:
            logger.info("Using DmlExecutionProvider")
            local_provider.append('DmlExecutionProvider')
        elif 'CPUExecutionProvider' in available_providers:
            logger.info("Using CPUExecutionProvider")
            local_provider.append('CPUExecutionProvider')
        else:
            logger.warning("No available providers, using CPUExecutionProvider")
            local_provider.append('CPUExecutionProvider')
        self.session = ort.InferenceSession(self.onnx_model, providers=local_provider)

    def predict(self, image=None, conf=None, iou=None):
        if image is not None:
            self.input_image = image
        if conf is not None:
            self.confidence_thres = conf
        if iou is not None:
            self.iou_thres = iou
        img_data = self.preprocess(self.input_image)
        outputs = self.session.run(None, {self.session.get_inputs()[0].name: img_data})
        # 后处理，返回图像和检测框
        return self.postprocess(self.img, outputs)

    def preprocess(self, image):
        if isinstance(image, str):  # 文件路径
            self.img = cv2.imread(image)
            img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        else:  # 已经是图片
            self.img = image
       
        
        img, self.ratio, (self.dw, self.dh) = self.letterbox(self.img, new_shape=self.input_size)
        
        image_data = np.array(img) / 255.0
        image_data = np.transpose(image_data, (2, 0, 1))  # 通道优先
        image_data = np.expand_dims(image_data, axis=0).astype(np.float32)
        return image_data

    def letterbox(self, img, new_shape=(640, 640), color=(114, 114, 114), auto=False, scaleFill=False, scaleup=True):
        shape = img.shape[:2]
        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        if not scaleup:
            r = min(r, 1.0)
        new_unpad = (int(round(shape[1] * r)), int(round(shape[0] * r)))
        dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]
        dw /= 2
        dh /= 2
        if shape[::-1] != new_unpad:
            img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
        top, bottom = int(round(dh)), int(round(dh))
        left, right = int(round(dw)), int(round(dw))
        img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
        return img, (r, r), (dw, dh)

    def postprocess(self, input_image, output):
        outputs = np.squeeze(output[0])  # (300, 6)

        boxes, scores, class_ids = [], [], []

        for i in range(outputs.shape[0]):
            x1, y1, x2, y2, score, class_id = outputs[i]

            if score < self.confidence_thres:
                continue

            # 转回原图尺寸
            x1 = (x1 - self.dw) / self.ratio[0]
            y1 = (y1 - self.dh) / self.ratio[1]
            x2 = (x2 - self.dw) / self.ratio[0]
            y2 = (y2 - self.dh) / self.ratio[1]

            w = x2 - x1
            h = y2 - y1

            boxes.append([int(x1), int(y1), int(w), int(h)])
            scores.append(float(score))
            class_ids.append(int(class_id))

        results_list = []
        for i in range(len(boxes)):
            results_list.append(YoloResult(
                box=boxes[i],
                score=scores[i],
                class_id=class_ids[i],
                image=input_image,
                classes=self.classes
            ))

        return results_list
    def draw_detections(self, img, box, score, class_id):
        x1, y1, w, h = box
        color = self.color_palette[class_id]
        cv2.rectangle(img, (int(x1), int(y1)), (int(x1 + w), int(y1 + h)), color, 2)
        label = f"{self.classes[class_id]}: {score:.2f}"
        (label_width, label_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        label_x = x1
        label_y = y1 - 10 if y1 - 10 > label_height else y1 + 10
        cv2.rectangle(img, (label_x, label_y - label_height),
                      (label_x + label_width, label_y + label_height), color, cv2.FILLED)
        cv2.putText(img, label, (label_x, label_y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 0, 0), 1, cv2.LINE_AA)
