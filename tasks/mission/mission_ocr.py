from module.ocr.ocr import RecOCR


class MissionOcr(RecOCR):
    def after_process(self, result):
        result=result.replace("消天","消灭")
        return super().after_process(result)