from module.ocr.ocr import Duration, OcrResultButton
from pponnxcr.predict_system import BoxedResult
from typing import List

class TimeFilterOcr(Duration):
    """专门用于筛选时间格式文本的OCR类"""

    def filter_detected(self, result: BoxedResult) -> bool:
        """只保留包含时间格式的文本"""
        # 使用时间正则表达式检查是否匹配
        res = self.timedelta_regex(self.lang).search(result.ocr_text)
        if res and (res.group('hours') or res.group('minutes') or res.group('seconds') or res.group('days')):
            return True
        return False

    def after_process(self, result):
        result = super().after_process(result)
        # 去掉"时间："前缀，支持中英文冒号
        for prefix in ['时间：', '时间:', 'Time:', 'Time：']:
            if result.startswith(prefix):
                result = result[len(prefix):]
                break
        return result.strip()

    def extract_time_results(self, image, direct_ocr=False) -> List[OcrResultButton]:
        """提取所有时间格式的文本并返回OcrResultButton列表"""
        results = self.detect_and_ocr(image, direct_ocr=direct_ocr)

        time_buttons = []
        for result in results:
            ocr_button = OcrResultButton(result, matched_keyword=None)
            time_buttons.append(ocr_button)

        return time_buttons

    def parse_time_values(self, time_buttons: List[OcrResultButton]) -> List[tuple]:
        """解析时间文本为具体的时间值"""
        time_values = []
        for button in time_buttons:
            # 使用Duration的format_result方法解析时间
            time_delta = self.format_result(button.text)
            minutes = time_delta.total_seconds() / 60
            time_values.append((button.text, time_delta, minutes))

        return time_values