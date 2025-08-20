import re
import time
from datetime import timedelta

from pponnxcr.predict_system import BoxedResult

from module.base.button import ButtonWrapper
from module.exception import ScriptError
from module.logger import logger

import re
from module.base.utils import area_in_area, crop, float2str, area_pad, corner2area
from module.ocr.keyword import Keyword
from module.ocr.onnxmodels import OCR_MODEL
from module.ocr.onnxocr.onnx_paddleocr import TxtBox
from module.ocr.utils import merge_buttons


class OcrResultButton:
    def __init__(self, boxed_result: TxtBox, matched_keyword):
        """
        Args:
            boxed_result: BoxedResult from ppocr-onnx
            matched_keyword: Keyword object or None
        """
        self.area = boxed_result.area
        self.search = area_pad(self.area, pad=-20)
        # self.color =
        self.button = boxed_result.button

        if matched_keyword is not None:
            self.matched_keyword = matched_keyword
            self.name = str(matched_keyword)
        else:
            self.matched_keyword = None
            self.name = boxed_result.txt

        self.text = boxed_result.txt
        self.score = boxed_result.threadhold

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
class CustomOCR:
    merge_thres_x = 0
    merge_thres_y = 0
    def __init__(self, button, lang=None, name=None):
        """
        Args:
            button: ButtonWrapper or area tuple
            lang: If None, use 'cn'
            name: If None, use button.name or generate one
        """
        self.button = button
        self.lang = lang or 'cn'
        self.name = name or getattr(button, 'name', f"CustomOCR_{id(self)}")
        self.model = OCR_MODEL

    def ocr_single_line(self, image,direct_ocr=False):
        """Perform OCR on single line - follows StarRailCopilot naming"""
        start_time = time.time()
        if not direct_ocr:
            image = crop(image, self.button.area, copy=False)
        image = self.pre_process(image)
        # ocr
        result, _ = self.model.ocr(image)
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
        result_list = self.model.ocr_lines(image_list)
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
        # pre process
        start_time = time.time()
        if not direct_ocr:
            image = crop(image, self.button.area, copy=False)
        image = self.pre_process(image)
        # ocr
        results: list[BoxedResult] = self.model.detect_and_ocr(image)
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
        if result.startswith('UID'):
            result = 'UID'
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

class CustomDigitCounter(CustomOCR):
    def __init__(self, button, lang='cn', name=None):
        super().__init__(button, lang, name)
        # Remove duplicate assignments - they're already handled by parent class

    def after_process(self, result):
        """Override this method to clean OCR results before parsing"""
        if re.match(r'^V\d+$', result):
            result = result.replace('V', '1/')
        result = result.replace('O', '0')  # O -> 0
        result = result.replace('o', '0')  # o -> 0
        result = result.replace('l', '1')  # l -> 1
        result = result.replace('I', '1')  # I -> 1
        return result

    @classmethod
    def is_format_matched(cls, result) -> bool:
        """Check if the result matches fraction format"""
        return '/' in str(result)

    def format_result(self, result) -> tuple[int, int, int]:
        """Parse OCR result like '14/15' and return (current, remain, total)"""
        result = self.after_process(result)

        match = re.search(r'(\d+)\s*/\s*(\d+)', result)
        if match:
            current, total = int(match.group(1)), int(match.group(2))
            remain = total - current
            return current, remain, total
        else:
            print(f'No digit counter found in {result}')
            return 0, 0, 0

    def ocr_single_line(self, image):
        """Perform OCR and parse the result - now properly crops using button area"""
        # Use parent class method to get cropped OCR text
        text = super().ocr_single_line(image)
        # Then format the result as a digit counter
        return self.format_result(text)
class CustomDigit(CustomOCR):
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
class CustomDuration(CustomOCR):
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