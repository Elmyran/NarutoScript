import re

from module.logger import logger
from module.ocr.ocr import Digit


class DataDigit(Digit):
    def format_result(self, result) -> int:
        """
        将带有万、亿后缀的中文数字转换为纯数字

        Returns:
            int: 转换后的数字
        """
        result = super().after_process(result)

        # 处理万的情况
        if '万' in result:
            # 提取万前面的数字部分
            match = re.search(r'([\d.]+)万', result)
            if match:
                number = float(match.group(1))
                return int(number * 10000)

                # 处理亿的情况
        if '亿' in result:
            match = re.search(r'([\d.]+)亿', result)
            if match:
                number = float(match.group(1))
                return int(number * 100000000)

                # 如果没有单位，直接提取数字
        res = re.search(r'(\d+)', result)
        if res:
            return int(res.group(1))
        else:
            logger.warning(f'No digit found in {result}')
            return 0