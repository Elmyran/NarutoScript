from module.ocr.ocr import  Ocr
import re
class FortressOcr(Ocr):

    def pre_process(self, image):
        return super().pre_process(image)
       
    def after_process(self, result):

        return super().after_process(result)
