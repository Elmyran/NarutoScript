import time
import re
from pponnxcr.predict_system import BoxedResult

from module.base.button import ButtonWrapper
from module.base.utils import corner2area

from module.base.utils.utils import area_offset, crop, float2str
from module.exception import ScriptError
from module.logger import logger
from module.ocr.ocr import OcrResultButton
from module.ocr.onnxmodels import CUSTOM_OCR_MODEL

from .utils import infer_args as init_args
from .utils import  draw_ocr


from module.base.decorator import cached_property, del_cached_property




class ONNXPaddleOcr:
    merge_thres_x = 0
    merge_thres_y = 0
    def __init__(self, button: ButtonWrapper, name=None, **kwargs):
        self.button = button
        self.name = name or self.button.name
       

   

    @cached_property
    def model(self):
        
        return CUSTOM_OCR_MODEL.model


    
    def pre_process(self, img):

        return img
    def after_process(self, result):
        return result
    def format_result(self, result):
       
        return result
    def ocr_single_line(self, img, det=True, rec=True, cls=True,direct_ocr=False):
        res=self.ocr_multiple_lines(img, det, rec, cls, direct_ocr)
        if res:
            result=self.format_result(res[0].ocr_text)
            return result
        return res
        
    def ocr_multiple_lines(self, img, det=True, rec=True, cls=True, direct_ocr=False): 
        start_time = time.time()
        if cls == True and self.model.use_angle_cls == False:
            print(
                "Since the angle classifier is not initialized, the angle classifier will not be uesd during the forward process"
            )
        
        if not direct_ocr:
            img=crop(img,self.button.area)
        img=self.pre_process(img)
        if det and rec:
            ocr_res = []
            dt_boxes, rec_res = self.model.__call__(img, cls)
            tmp_res = [[box.tolist(), res] for box, res in zip(dt_boxes, rec_res)]
            ocr_res.append(tmp_res)
            
        elif det and not rec:
            ocr_res = []
            dt_boxes = self.model.text_detector(img)
            tmp_res = [box.tolist() for box in dt_boxes]
            ocr_res.append(tmp_res)
            
        else:
            ocr_res = []
            cls_res = []

            if not isinstance(img, list):
                img = [img]
            if self.model.use_angle_cls and cls:
                img, cls_res_tmp = self.model.text_classifier(img)
                if not rec:
                    cls_res.append(cls_res_tmp)
            rec_res = self.model.text_recognizer(img)
            ocr_res.append(rec_res)

         # 将 ocr_res 转换为 BoxedResult 列表
        detected_results: list[BoxedResult] = self.resultToBoxResult(ocr_res)
     
        # 处理检测结果
        processed_results = []
        for result in detected_results:
            if not direct_ocr:
                result.box = area_offset(result.box, self.button.area[:2])
            processed_results.append(result)
        
        # 过滤和合并结果
        filtered_results = [result for result in processed_results if self.filter_detected(result)]
        #merged_results = merge_buttons(filtered_results, thres_x=self.merge_thres_x, thres_y=self.merge_thres_y)
        merged_results=filtered_results

        for result in merged_results:
            result.ocr_text=self.after_process(result.ocr_text)
        logger.attr(name='%s %ss' % (self.name, float2str(time.time() - start_time)),
                    text=str([result.ocr_text for result in merged_results]))
        
        return merged_results 
    
   
   
    def filter_detected(self, result: BoxedResult) -> bool:
        """
        Return False to drop result.
        """
        return True
    def matched_ocr(self, image, keyword_classes, direct_ocr=False) -> list[OcrResultButton]:
        """
        Args:
            image: Screenshot
            keyword_classes: `Keyword` class or classes inherited `Keyword`, or a list of them.
            direct_ocr: True to ignore `button` attribute and feed the image to OCR model without cropping.

        Returns:
            List of matched OcrResultButton.
            OCR result which didn't matched known keywords will be dropped.
        """
        results = self.ocr_multiple_lines(image, direct_ocr=direct_ocr)

        results = [self._product_button(result, keyword_classes) for result in results]
        results = [result for result in results if result.is_keyword_matched]

        logger.attr(name=f'{self.name} matched',
                    text=results)
        return results
            
    def _product_button(
            self,
            boxed_result: BoxedResult,
            keyword_classes,
            lang: str = None,
            ignore_punctuation=True,
            ignore_digit=True
    ) -> OcrResultButton:
        if not isinstance(keyword_classes, list):
            keyword_classes = [keyword_classes]

        matched_keyword = self._match_result(
            boxed_result.ocr_text,
            keyword_classes=keyword_classes,
            lang=lang,
            ignore_punctuation=ignore_punctuation,
            ignore_digit=ignore_digit,
        )
        button = OcrResultButton(boxed_result, matched_keyword)
        return button
    def _match_result(
            self,
            result: str,
            keyword_classes,
            lang: str = None,
            ignore_punctuation=True,
            ignore_digit=True):
        """
        Args:
            result (str):
            keyword_classes: A list of `Keyword` class or classes inherited `Keyword`

        Returns:
            If matched, return `Keyword` object or objects inherited `Keyword`
            If not match, return None
        """
        if not isinstance(keyword_classes, list):
            keyword_classes = [keyword_classes]

        # Digits will be considered as the index of keyword
        if ignore_digit:
            if result.isdigit():
                return None

        # Try in current lang
        for keyword_class in keyword_classes:
            try:
                matched = keyword_class.find(
                    result,
                    lang=lang,
                    ignore_punctuation=ignore_punctuation
                )
                return matched
            except ScriptError:
                continue

        return None
    
 
    def matchTime(self,boxes):
        boxes_matched_time=[]
        if not boxes:
            return boxes_matched_time
        pattern=r'(0?[0-9]|1[0-9]|2[0-3])时([0-5]?[0-9])分'
        for box in boxes:
            if re.search(pattern,box.txt):
                boxes_matched_time.append(box)
        return boxes_matched_time
  
    def resultToBoxResult(self,ocr_res)-> list[BoxedResult]:
        """
        :param result: ocr method result
        :return: TxtBox list
        """
        boxed_results = []  
        ocr_res = ocr_res[0]
        for item in ocr_res:  
            # 提取坐标点和文本信息  
            points, (text, score) = item  
            # 将四个点转换为边界框 (x1, y1, x2, y2)  
            box=tuple(corner2area(points))
            # 创建 BoxedResult 对象  
            boxed_result = BoxedResult(  
                box=box,  
                text_img=None,  # 通常为 None，除非需要保存文本图像  
                ocr_text=text,  
                score=score  
            )  
            boxed_results.append(boxed_result)  
        return boxed_results







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


