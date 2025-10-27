import re
from datetime import timedelta, datetime
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
        if main.image_color_count(button, color=self.active_color, threshold=221, count=100):
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
    @classmethod
    def timedelta_regex(cls, lang):
        if lang == 'cn':
            # 专门匹配 "HH:MM:SS后免费" 格式
            return re.compile(r'(?P<hours>\d{1,2}):(?P<minutes>\d{1,2}):(?P<seconds>\d{1,2})后.*?免费')
        return super().timedelta_regex(lang)

    def format_result(self, result: str) -> datetime:
        matched = self.timedelta_regex(self.lang).search(result)
        if not matched:
            return datetime.now()  # Return current time if no match

        hours = self._sanitize_number(matched.group('hours'))
        minutes = self._sanitize_number(matched.group('minutes'))
        seconds = self._sanitize_number(matched.group('seconds'))

        # Return future datetime when recruit will be available
        return datetime.now() + timedelta(hours=hours, minutes=minutes, seconds=seconds)