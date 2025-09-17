
from pponnxcr.predict_system import BoxedResult


from module.base.button import ButtonWrapper
from module.logger import logger
from module.ocr.ocr import Ocr, OcrResultButton
from module.ocr.ocrutils import OCR
from tasks.base.assets.assets_base_page import MAIN_GOTO_TASK_SEARCH_AREA


class TaskTabOcr(Ocr):
    def __init__(self, button: ButtonWrapper, custom_ocr: OCR, **kwargs):
        super().__init__(button, **kwargs)
        self.custom_ocr = custom_ocr
    def after_process(self, result):
        """对OCR结果进行修正"""
        result = super().after_process(result)
        # 单字符修正
        result = result.replace('寒', '赛')
        result = result.replace('符', '行')
        result = result.replace('寨', '赛')
        result = result.replace('部', '所')
        result = result.replace('狂', '任')
        result = result.replace('践', '战')
        result = result.replace('公', '会')
        # 繁体字修正
        result = result.replace('組', '组')
        result = result.replace('決', '决')
        result = result.replace('鬥', '斗')
        result = result.replace('試', '试')
        result = result.replace('煉', '炼')
        result = result.replace('隊', '队')
        result = result.replace('襲', '袭')
        result = result.replace('豐', '丰')
        result = result.replace('饒', '饶')
        result = result.replace('間', '间')
        result = result.replace('紙', '织')
        result = result.replace('焗', '场')
        result = result.replace('綱','织')
        if '小队突' in result or '小队' in result or '突袭' in result:
            result='小队突袭'
        if '积分'in result or '积' in result or '分' in result:
            result = '积分赛'
        if '排' in result and '榜' in result or '行' in result:
            result = '排行榜'
        if '集会' in result:
            result = '任务集会所'
        if '忍者挑' in result or '挑战' in result:
            result='忍者挑战'
        return result
    def detect_and_ocr(self, image, direct_ocr=False) -> list[BoxedResult]:
        txt_boxes = self.custom_ocr.ocr_text(image, ocr_direct=direct_ocr)
        boxed_results = []
        for txt_box in txt_boxes:
            corrected_text = self.after_process(txt_box.txt)

            # 确保坐标是绝对坐标，不是相对坐标
            if not direct_ocr and self.button is not None:
                # 如果使用了按钮裁剪，需要将相对坐标转换为绝对坐标
                x1, y1, x2, y2 = self.button.area
                box_x1, box_y1, box_x2, box_y2 = txt_box.area
                absolute_area = (box_x1 + x1, box_y1 + y1, box_x2 + x1, box_y2 + y1)
            else:
                absolute_area = txt_box.area

            boxed_result = BoxedResult(
                box=absolute_area,
                text_img=None,
                ocr_text=corrected_text,
                score=txt_box.threadhold
            )
            boxed_results.append(boxed_result)

        return boxed_results
    def matched_ocr(self, image, keyword_classes, direct_ocr=False) -> list[OcrResultButton]:
        results = self.detect_and_ocr(image, direct_ocr=direct_ocr)
        logger.attr(name=f'{self.name} raw', text=results)
        results = [self._product_button(result, keyword_classes) for result in results]
        results = [result for result in results if result.is_keyword_matched]

        logger.attr(name=f'{self.name} matched', text=results)
        return results
TaskOcr=OCR(button=MAIN_GOTO_TASK_SEARCH_AREA, use_angle_cls=True)