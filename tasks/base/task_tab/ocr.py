from module.ocr.ocr import Ocr


class TaskTabOcr(Ocr):
    def after_process(self, result):
        result=result.replace('袭','装')
        result=result.replace('秋','秘')
        if '小队' in result:
            result='小队突袭'
        if '集会所' in result:
            result='任务集会所'
        

        return super().after_process(result)
