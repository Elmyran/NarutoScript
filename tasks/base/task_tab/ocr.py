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

        # 针对识别到的文字进行修正
        corrections = {
            '积分寒': '积分赛',
            '排符榜': '排行榜',
            '忍者大寨': '忍者大赛',
            '任务集会部': '任务集会所',
            '忍者挑践': '忍者挑战',
            '組织': '组织',
            '決鬥場': '决斗场',
            '試煉之地': '试炼之地',
            '小隊突襲': '小队突袭',
            '豐饒之間': '丰饶之间'
        }
        for wrong, correct in corrections.items():
            if wrong in result:
                result = result.replace(wrong, correct)
        if '小队突' in result:
            result='小队突袭'
        if '积分' in result :
            result = '积分赛'
        if '排' in result and '榜' in result:
            result = '排行榜'
        if '任务集会' in result:
            result = '任务集会所'
        if '忍者挑' in result:
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
        print('Matched OCR')
        print(results)
        results = [self._product_button(result, keyword_classes) for result in results]
        results = [result for result in results if result.is_keyword_matched]

        logger.attr(name=f'{self.name} matched', text=results)
        return results
TaskOcr=OCR(button=MAIN_GOTO_TASK_SEARCH_AREA, use_angle_cls=True)