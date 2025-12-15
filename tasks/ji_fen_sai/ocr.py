


from module.ocr.ocr import Ocr


class JiFenSaiOcr(Ocr):
    def after_process(self, result):
        return super().after_process(result)
    