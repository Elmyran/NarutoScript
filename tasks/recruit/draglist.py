import re
from datetime import timedelta, datetime
from module.config.utils import get_server_next_update
from module.ocr.ocr import Duration
from module.ui.draggable_list import DraggableList
from tasks.recruit.assets.assets_recruit_ui import *
from module.logger import logger
from module.ocr.ocr import Ocr
from tasks.recruit.keywords import RecruitKeyword
class RecruitDragList(DraggableList):
    current_keyword=None
    def load_rows(self, main):
        """重写 load_rows 方法以适应商店界面"""
        super().load_rows(main=main)
        logger.info(f'Loaded {len(self.cur_buttons)}  tabs')
        for i, button in enumerate(self.cur_buttons):
            logger.info(f'Tab {i}: {button.matched_keyword}')

    def search_rows(self, main,keyword):
        self.current_keyword=keyword
        if RecruitTabList.insight_row(keyword, main=main):
            logger.info('Successfully navigated to'+keyword.cn)
            if RecruitTabList.select_row(keyword, main=main):
                logger.info('Successfully selected '+keyword.cn)
    def is_row_selected(self, button, main):
        button.area=(button.area[0]-50,button.area[1]-50,button.area[2]+50,button.area[3]+50)
        if main.image_color_count(button, color=self.active_color, threshold=240, count=1000):
            return True
        return False

        
   
RecruitTabList= RecruitDragList(
    name='RecruitTabList',
    keyword_class=RecruitKeyword,
    ocr_class=Ocr,
    search_button=RECRUIT_TAB_SEARCH,
    check_row_order=False,
    active_color=(241,231,209),
    drag_direction="down"
)
class RecruitDuration(Duration):
   
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