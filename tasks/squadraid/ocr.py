from module.ocr.ocr import DigitCounter
import re

class SquadRaidOCR(DigitCounter):
    def after_process(self, result):
        result = result.replace('212', '2/2')
        result = result.replace('112', '1/2')
        result = result.replace('012', '0/2')

        return result