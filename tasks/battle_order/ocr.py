from module.ocr.ocr import Digit


class BattleOrderOcr(Digit):
    def format_result(self, result):
        return Digit.format_result(self, result)
