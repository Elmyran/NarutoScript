from functools import cmp_to_key
import time
from datetime import timedelta

import numpy as np

import module.config.server as server
from module.base.button import ButtonWrapper
from module.base.decorator import cached_property
from module.base.utils import *
from module.exception import ScriptError
from module.logger import logger
from module.ocr.keyword import Keyword
from module.ocr.models import OCR_MODEL, RapidOCR

class BoxedResult:
    def __init__(self, box, text_img, ocr_text, score):
        self.box = box
        self.text_img = text_img
        self.ocr_text = ocr_text
        self.score = score

    def __str__(self):
        return 'BoxedResult[%s, %s]' % (self.ocr_text, self.score)

    def __repr__(self):
        return self.__str__()


def sorted_boxes(dt_boxes):
    return sorted(
        dt_boxes,
        key=cmp_to_key(lambda x, y:
            x[0][0] - y[0][0]
            if -10 < x[0][1] - y[0][1] < 10 else
            x[0][1] - y[0][1]
        )
    )
def perspective_crop(img, points):
    w = round(max(
        np.linalg.norm(points[0] - points[1]),
        np.linalg.norm(points[2] - points[3]),
    ))
    h = round(max(
        np.linalg.norm(points[0] - points[3]),
        np.linalg.norm(points[1] - points[2]),
    ))
    return cv2.warpPerspective(
        img,
        cv2.getPerspectiveTransform(
            points,
            np.float32([[0, 0],[w, 0],[w, h],[0, h]])
        ),
        (w, h),
        borderMode=cv2.BORDER_REPLICATE,
        flags=cv2.INTER_CUBIC,
    )


class OcrResultButton:
    def __init__(self, boxed_result: BoxedResult, matched_keyword):
        """
        Args:
            boxed_result: BoxedResult from ppocr-onnx
            matched_keyword: Keyword object or None
        """
        self.area = boxed_result.box
        
        self.search = area_pad(self.area, pad=-20)
        # self.color =
        self.button = boxed_result.box

        if matched_keyword is not None:
            self.matched_keyword = matched_keyword
            self.name = str(matched_keyword)
        else:
            self.matched_keyword = None
            self.name = boxed_result.ocr_text

        self.text = boxed_result.ocr_text
        self.score = boxed_result.score

    def __str__(self):
        return self.name

    __repr__ = __str__

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(self.name)

    def __bool__(self):
        return True

    @property
    def is_keyword_matched(self) -> bool:
        return self.matched_keyword is not None


class Ocr:
    # Merge results with box distance <= thres
    merge_thres_x = 0
    merge_thres_y = 0

    def __init__(self, button: ButtonWrapper, lang='cn', name=None):
        """
        Args:
            button:
            lang: If None, use in-game language
            name: If None, use button.name
        """
        if lang is None:
            lang = server.lang
        if name is None:
            name = button.name

        self.button: ButtonWrapper = button
        self.lang: str = lang
        self.name: str = name

    @cached_property
    def model(self) -> RapidOCR:
        return OCR_MODEL.get_by_lang('cn')

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

    def ocr_single_line(self, image, direct_ocr=False):
        # pre process
        start_time = time.time()
        if not direct_ocr:
            image = crop(image, self.button.area, copy=False)
        image = self.pre_process(image)
        # ocr
        result= self.model(image,use_cls=False)
        if result:
            result = result.txts[0]
        else:
            result = ''        

        # after proces
        result = self._log_change('after', self.after_process, result)
        result = self._log_change('format', self.format_result, result)
        logger.attr(name='%s %ss' % (self.name, float2str(time.time() - start_time)),
                    text=str(result))
        return result

    def ocr_multi_lines(self, image_list):
        # pre process
        start_time = time.time()
        image_list = [self.pre_process(image) for image in image_list]
        # ocr
        result_list=[]
        for image in image_list:
            result= self.model(image,use_cls=False)
            if result:
                result = [result.txts[0],result.scores[0]] 
                result_list.append(result)
        result_list = [(result, score) for result, score in result_list]
        # after process
        result_list = [(self.after_process(result), score) for result, score in result_list]
        result_list = [(self.format_result(result), score) for result, score in result_list]
        logger.attr(name="%s %ss" % (self.name, float2str(time.time() - start_time)),
                    text=str([result for result, _ in result_list]))
        return result_list

    def filter_detected(self, result: BoxedResult) -> bool:
        """
        Return False to drop result.
        """
        return True

    def detect_and_ocr(self, image, direct_ocr=False) -> list[BoxedResult]:
        """
        Args:
            image:
            direct_ocr: True to ignore `button` attribute and feed the image to OCR model without cropping.

        Returns:

        """
        from module.ocr.utils import merge_buttons
        # pre process
        start_time = time.time()
        if not direct_ocr:
            image = crop(image, self.button.area, copy=False)
        image = self.pre_process(image)
        # ocr
        results: list[BoxedResult]=[]
        output= self.model(image)
        if output.txts:
            for i in range(len(output.txts)):
                box = output.boxes[i]
                text = output.txts[i]
                score = output.scores[i]
                boxed_result = BoxedResult(
                    box=box, 
                    text_img=None, # 如果需要子图，您需要在这里实现裁剪逻辑
                    ocr_text=text, 
                    score=score
                )
                results.append(boxed_result)
        # after proces
        for result in results:
            if not direct_ocr:
                result.box += self.button.area[:2]
            result.box = tuple(corner2area(result.box))

        results = [result for result in results if self.filter_detected(result)]
        
        results = merge_buttons(results, thres_x=self.merge_thres_x, thres_y=self.merge_thres_y)
        for result in results:
            result.ocr_text = self.after_process(result.ocr_text)

        logger.attr(name='%s %ss' % (self.name, float2str(time.time() - start_time)),
                    text=str([result.ocr_text for result in results]))
        return results

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

    def matched_single_line(
            self,
            image,
            keyword_classes,
            lang: str = None,
            ignore_punctuation=True
    ) -> Keyword:
        """
        Args:
            image: Image to detect
            keyword_classes: `Keyword` class or classes inherited `Keyword`, or a list of them.
            lang:
            ignore_punctuation:

        Returns:
            Keyword: Or None if it didn't matched known keywords.
        """
        result = self.ocr_single_line(image)

        result = self._match_result(
            result,
            keyword_classes=keyword_classes,
            lang=lang,
            ignore_punctuation=ignore_punctuation,
        )

        logger.attr(name=f'{self.name} matched',
                    text=result)
        return result

    def matched_multi_lines(
            self,
            image_list,
            keyword_classes,
            lang: str = None,
            ignore_punctuation=True
    ) -> list[Keyword]:
        """
        Args:
            image_list:
            keyword_classes: `Keyword` class or classes inherited `Keyword`, or a list of them.
            lang:
            ignore_punctuation:

        Returns:
            List of matched Keyword.
            OCR result which didn't matched known keywords will be dropped.
        """
        results = self.ocr_multi_lines(image_list)

        results = [self._match_result(
            result,
            keyword_classes=keyword_classes,
            lang=lang,
            ignore_punctuation=ignore_punctuation,
        ) for result in results]
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
        results = self.detect_and_ocr(image, direct_ocr=direct_ocr)

        results = [self._product_button(result, keyword_classes) for result in results]
        results = [result for result in results if result.is_keyword_matched]

        logger.attr(name=f'{self.name} matched',
                    text=results)
        return results


class Digit(Ocr):
    def __init__(self, button: ButtonWrapper, lang='cn', name=None):
        super().__init__(button, lang=lang, name=name)
    def pre_process(self, image):

        height, width, _ = image.shape
        min_size = 640
        
        if height < min_size or width < min_size:
           
            top = max(0, (min_size - height) // 2)
            bottom = max(0, min_size - height - top)
            left = max(0, (min_size - width) // 2)
            right = max(0, min_size - width - left)       
            background_color = [int(x) for x in image[0, 0]]

            image = cv2.copyMakeBorder(
                image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=background_color
            )
        return super().pre_process(image)
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


class DigitCounter(Ocr):
    def __init__(self, button: ButtonWrapper, lang='cn', name=None):
        super().__init__(button, lang=lang, name=name)
    def pre_process(self, image):
        
        height, width, _ = image.shape
        min_size = 640
        
        if height < min_size or width < min_size:
           
            top = max(0, (min_size - height) // 2)
            bottom = max(0, min_size - height - top)
            left = max(0, (min_size - width) // 2)
            right = max(0, min_size - width - left)

            
            background_color = [int(x) for x in image[0, 0]]

            image = cv2.copyMakeBorder(
                image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=background_color
            )
        return super().pre_process(image)
    @classmethod
    def is_format_matched(cls, result) -> bool:
        return '/' in result

    def format_result(self, result) -> tuple[int, int, int]:
        """
        Do OCR on a counter, such as `14/15`, and returns 14, 1, 15

        Returns:
            int, int, int: current, remain, total
        """
        result = super().after_process(result)
        logger.attr(name=self.name, text=str(result))

        res = re.search(r'(\d+)\s*/\s*(\d+)', result)
        if res:
            groups = [int(s) for s in res.groups()]
            current, total = int(groups[0]), int(groups[1])
            # current = min(current, total)
            return current, total - current, total
        else:
            logger.warning(f'No digit counter found in {result}')
            return 0, 0, 0


class Duration(Ocr):
    @classmethod
    def timedelta_regex(cls, lang):
        regex_str = {
            'cn': r'^(?P<prefix>.*?)'
                  r'((?P<days>\d{1,2})\s*天\s*)?'
                  r'((?P<hours>\d{1,2})\s*小时\s*)?'
                  r'((?P<minutes>\d{1,2})\s*分钟\s*)?'
                  r'((?P<seconds>\d{1,2})\s*秒)?'
                  r'(?P<suffix>[^天时钟秒]*?)$',
            'en': r'^(?P<prefix>.*?)'
                  r'((?P<days>\d{1,2})\s*d\s*)?'
                  r'((?P<hours>\d{1,2})\s*h\s*)?'
                  r'((?P<minutes>\d{1,2})\s*m\s*)?'
                  r'((?P<seconds>\d{1,2})\s*s)?'
                  r'(?P<suffix>[^dhms]*?)$'
        }[lang]
        return re.compile(regex_str)

    def after_process(self, result):
        result = super().after_process(result)
        result = result.strip('.,。，')
        result = result.replace('Oh', '0h').replace('oh', '0h')
        return result

    def format_result(self, result: str) -> timedelta:
        """
        Do OCR on a duration, such as `18d 2h 13m 30s`, `2h`, `13m 30s`, `9s`

        Returns:
            timedelta:
        """
        matched = self.timedelta_regex(self.lang).search(result)
        if not matched:
            return timedelta()
        days = self._sanitize_number(matched.group('days'))
        hours = self._sanitize_number(matched.group('hours'))
        minutes = self._sanitize_number(matched.group('minutes'))
        seconds = self._sanitize_number(matched.group('seconds'))
        return timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

    @staticmethod
    def _sanitize_number(number) -> int:
        if number is None:
            return 0
        return int(number)


class OcrWhiteLetterOnComplexBackground(Ocr):
    white_preprocess = True
    # 0.6 by default, 0.2 for lower
    box_thresh = 0.2
    # (x, y) Enlarge detected boxes to `min_boxes`
    # So standalone digits can be better detected
    # Note that min_box should be 4px larger than the actual letter
    min_box = None

    def pre_process(self, image):
        if self.white_preprocess:
            image = extract_white_letters(image, threshold=255)
            image = cv2.merge([image, image, image])
        return image

    @staticmethod
    def enlarge_box(box, min_box):
        area = corner2area(box)
        center = (int(x) for x in area_center(area))
        size_x, size_y = area_size(area)
        min_x, min_y = min_box
        if size_x < min_x or size_y < min_y:
            size_x = max(size_x, min_x) // 2
            size_y = max(size_y, min_y) // 2
            area = area_offset((-size_x, -size_y, size_x, size_y), center)
            box = area2corner(area)
            box = np.array([box[0], box[1], box[3], box[2]]).astype(np.float32)
            return box
        else:
            return box

    def enlarge_boxes(self, boxes):
        if self.min_box is None:
            return boxes

        boxes = [self.enlarge_box(box, self.min_box) for box in boxes]
        boxes = np.array(boxes)
        return boxes

    
