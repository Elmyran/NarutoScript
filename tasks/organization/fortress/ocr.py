from module.base.utils.utils import area_offset, color_similarity_2d, crop, float2str
from module.logger import logger
from module.ocr.ocr import  BoxedResult, Ocr, OcrWhiteLetterOnComplexBackground

import time
import re
import cv2
import numpy as np
class FortressOcr(Ocr,OcrWhiteLetterOnComplexBackground):
    box_thresh=0.2
    def pre_process(self, image):
        image = cv2.resize(image, (2560, 1920), interpolation=cv2.INTER_CUBIC)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array([20,100,100]), np.array([40,255,255]))
        image[mask > 0] = [255,255,255]
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        image = clahe.apply(gray)
        image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        return OcrWhiteLetterOnComplexBackground.pre_process(self,image)
    def after_process(self, result):
        result=result.replace('商','汤')
        result=result.replace('溺','汤')
        result=result.replace('锅','涡')
        result=result.replace('日','田')
        result=result.replace('防','汤')
        result=result.replace('尚','汤')
        result=result.replace('福','雷')    
        result=result.replace('凤','风')
        result=result.replace('安','要')
        result=result.replace('装','塞')
        result=result.replace('勇','雷')
        result=result.replace('洗','泷')
        result=result.replace('杨','汤')
        result=result.replace('菜','草')
        result=result.replace('小','川')
        result = re.sub('^大.*', '大之要塞', result)
        result = re.sub('^铁.*', '铁之要塞', result)  
        result = re.sub('^田.*', '田之要塞', result)  
        result = re.sub('^土.*', '土之要塞', result)  
        result = re.sub('^熊.*', '熊之要塞', result)  
        result = re.sub('^汤.*', '汤之要塞', result)  
        result = re.sub('^涡.*', '涡之要塞', result)  
        result = re.sub('^霜.*', '霜之要塞', result)  
        result = re.sub('^水.*', '水之要塞', result)  
        result = re.sub('^火.*', '火之要塞', result)  
        result = re.sub('^雨.*', '雨之要塞', result)  
        result = re.sub('^草.*', '草之要塞', result)  
        result = re.sub('^川.*', '川之要塞', result)  
        result = re.sub('^雷.*', '雷之要塞', result)  
        result = re.sub('^风.*', '风之要塞', result)  
        result = re.sub('^海.*', '海之要塞', result)  
        result = re.sub('^泷.*', '泷之要塞', result)  
        result = re.sub('^云.*', '云之要塞', result)  
        result = re.sub('^鸟.*', '鸟之要塞', result)  
        return super().after_process(result)
    def ocr_multiple_lines(self, img, det=True, rec=True, cls=True, direct_ocr=False): 
        
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
        for result in merged_results:  
            if result.ocr_text == '大之要塞':  
                # 裁剪图标区域检测颜色  
                icon_area = (result.box[0] - 10, result.box[1]-10, result.box[0]+10, result.box[3]+10)  
                icon_image = crop(img, icon_area, copy=False)  
                earth_color = (176, 64, 25)  
                fire_color = (90, 64, 139)  
                earth_similarity = color_similarity_2d(icon_image, color=earth_color)  
                fire_similarity = color_similarity_2d(icon_image, color=fire_color)  
                  
                earth_count = cv2.countNonZero(cv2.inRange(earth_similarity, 100, 255))  
                fire_count = cv2.countNonZero(cv2.inRange(fire_similarity, 100, 255)) 
                before = result.ocr_text
                if earth_count > fire_count: 
                    result.ocr_text = '土之要塞'  
                     
                else:
                    result.ocr_text = '火之要塞'  
                logger.attr(name=f'{self.name} after_process',  
                            text=f'{before} -> {result.ocr_text}')
        return merged_results 
    def matched_ocr(self, image, keyword_classes, direct_ocr=False):
        start_time = time.time()
        results=self.ocr_multiple_lines(image, det=True, rec=True, cls=False, direct_ocr=direct_ocr)

        results = [self._product_button(result, keyword_classes) for result in results]
        logger.attr(name='%s %ss' % (self.name, float2str(time.time() - start_time)),
                    text=str([result.text for result in results]))
        results = [result for result in results if result.is_keyword_matched]    
        
        return results