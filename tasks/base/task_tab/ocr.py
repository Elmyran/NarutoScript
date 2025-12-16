from module.ocr.ocr import Ocr


class TaskTabOcr(Ocr):
    def after_process(self, result):
        result=result.replace('袭','装')
        result=result.replace('秋','秘')
        result=result.replace('桃','挑')    
        result=result.replace('條','像')
        result=result.replace('双','忍')
        result=result.replace('驱','忍')
        result=result.replace('亚','忍')
        result=result.replace('贝','忍')
        result=result.replace('四','忍')
        result=result.replace('烫','忍')
        result=result.replace('館','馆')
        result=result.replace('禾头','秘')
        result=result.replace('彩秘','秘')
        if '小队' in result:
            result='小队突袭'
        if '集会所' in result:
            result='任务集会所'
        

        return super().after_process(result)
