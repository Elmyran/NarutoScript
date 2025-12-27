


from module.ocr.ocr import DigitCounter, Ocr


class JiFenSaiOcr(Ocr):
    def after_process(self, result):

        return super().after_process(result)
class JiFenSaiDigitCounter(DigitCounter):
    def after_process(self, result):
        result=result.replace('1V/','11/')
        return super().after_process(result)
    