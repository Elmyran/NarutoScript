from module.logger import logger
from module.ocr.ocr import Ocr


class MiJingOcr(Ocr):
    def __init__(self, button, lang='cn', name=None):
        super().__init__(button, lang=lang, name=name)
        # 定义纠正映射表（常见错字 -> 正确结果）
        self.correction_map = {
            "垂霆秘境": "雷霆秘境",
            "雸霆秘境": "雷霆秘境",
            "雷霆秘淀": "雷霆秘境",
            "雷霆密境": "雷霆秘境",
            "霆霆秘境": "雷霆秘境",
            "显体秘境": "罡体秘境",
            "水宰秘境":"水牢秘境"
        }

    def after_process(self, result: str) -> str:
        """
        在OCR之后进行纠正
        """
        if result in self.correction_map:
            corrected = self.correction_map[result]
            logger.attr(f"{self.name} correction", f"{result} -> {corrected}")
            return corrected

        # 如果OCR结果相似度接近某个目标词，也纠正
        target = "雷霆秘境"
        if len(result) == len(target):
            # 简单编辑距离/相似度判断（替代 fuzzywuzzy，避免额外依赖）
            diff = sum(1 for a, b in zip(result, target) if a != b)
            if diff <= 1:  # 允许1个字不同也算"雷霆秘境"
                logger.attr(f"{self.name} correction", f"{result} -> {target}")
                return target

        return super().after_process(result)
