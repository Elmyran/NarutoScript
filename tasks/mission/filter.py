import re
from datetime import timedelta

from module.ocr.ocr import Duration, Ocr


class TaskTimeExtractor(Ocr):
    def after_process(self, result):
        result = super().after_process(result)
        # 移除"时间:"或"时间："前缀
        result = result.replace('时间:', '').replace('时间：', '')
        return result

    def format_result(self, result: str) -> timedelta:
        import re
        # 匹配"3时0分"格式
        pattern = r'(?:(\d+)时)?(?:(\d+)分)?'
        match = re.search(pattern, result)
        if match:
            hours = int(match.group(1)) if match.group(1) else 0
            minutes = int(match.group(2)) if match.group(2) else 0
            return timedelta(hours=hours, minutes=minutes)
        return timedelta()