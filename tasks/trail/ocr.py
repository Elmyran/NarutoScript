from module.ocr.ocr import Duration
import re
from datetime import timedelta, datetime
from module.config.utils import get_server_next_update
class CultivationDuration(Duration):
   
    def after_process(self, result):    
        result = super().after_process(result)       
        # 7:5959 -> 7:59:59    
        # 27:0959 -> 27:09:59    
        result = re.sub(r'(\d{1,2}):(\d{2})(\d{2})', r'\1:\2:\3', result)    
          
        # 转换为标准格式    
        if self.lang == 'cn':    
            result = re.sub(r'(\d+):(\d+):(\d+)', r'\1小时\2分钟\3秒', result)    
        else:    
            result = re.sub(r'(\d+):(\d+):(\d+)', r'\1h\2m\3s', result)    
          
        return result  
    def format_result(self, result: str) -> datetime:
        matched = self.timedelta_regex(self.lang).search(result)
        hours = self._sanitize_number(matched.group('hours'))
        minutes = self._sanitize_number(matched.group('minutes'))
        seconds = self._sanitize_number(matched.group('seconds'))
        if hours == 0 and minutes == 0 and seconds == 0:
            return get_server_next_update('05:00')  
        # Return future datetime when recruit will be available
        return datetime.now() + timedelta(hours=hours, minutes=minutes, seconds=seconds)