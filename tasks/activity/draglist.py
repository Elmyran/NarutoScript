from module.logger import logger
from module.ocr.ocr import Ocr
from module.ui.draggable_list import DraggableList
from tasks.activity.assets.assets_activity import ACTIVITY_LIST_AREA
from tasks.activity.assets.assets_activity_ui import MONTHLY_SIGN_IN_CHECK
from tasks.activity.keyword import ActivityTab


class DraggableActivityTabList(DraggableList):


    def load_rows(self, main):
        """重写 load_rows 方法以适应活动界面"""
        super().load_rows(main=main)
        logger.info(f'Loaded {len(self.cur_buttons)} activity tabs')
        for i, button in enumerate(self.cur_buttons):
            logger.info(f'Tab {i}: {button.matched_keyword}')
    def search_rows(self, main,keyword):
        if ACTIVITY_TAB_LIST.insight_row(keyword, main=main):
            logger.info('Successfully navigated to monthly '+keyword.name+' area')
            if ACTIVITY_TAB_LIST.select_row(keyword, main=main):
                logger.info('Successfully selected monthly '+keyword.name+'tab')

        # 创建活动标签页列表实例
ACTIVITY_TAB_LIST = DraggableActivityTabList(
    name='ActivityTabList',
    keyword_class=ActivityTab,
    ocr_class=Ocr,
    search_button=ACTIVITY_LIST_AREA,
    check_row_order=False,
    active_color=(212,190,143),
    drag_direction="down"
)