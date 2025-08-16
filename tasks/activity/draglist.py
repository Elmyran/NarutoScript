from module.logger import logger
from module.ocr.ocr import Ocr
from module.ui.draggable_list import DraggableList
from tasks.activity.assets.assets_activity import ACTIVITY_LIST_AREA
from tasks.activity.assets.assets_activity_ui import MONTHLY_SIGN_IN_CHECK
from tasks.activity.keyword import ActivityTab


class DraggableActivityTabList(DraggableList):
    def is_row_selected(self, button, main):
        """检测标签页是否被选中且页面已加载"""
        # 检查页面是否已加载（这是最重要的判断条件）
        if main.appear(MONTHLY_SIGN_IN_CHECK):
            return True
        return False

    def load_rows(self, main):
        """重写 load_rows 方法以适应活动界面"""
        super().load_rows(main=main)
        logger.info(f'Loaded {len(self.cur_buttons)} activity tabs')
        for i, button in enumerate(self.cur_buttons):
            logger.info(f'Tab {i}: {button.matched_keyword}')
    def search_rows(self, main,keyword):
        if ACTIVITY_TAB_LIST.insight_row(keyword, main=main):
            logger.info('Successfully navigated to monthly sign-in tab area')
            if ACTIVITY_TAB_LIST.select_row(keyword, main=main):
                logger.info('Successfully selected monthly sign-in tab')

        # 创建活动标签页列表实例
ACTIVITY_TAB_LIST = DraggableActivityTabList(
    name='ActivityTabList',
    keyword_class=ActivityTab,
    ocr_class=Ocr,
    search_button=ACTIVITY_LIST_AREA,
    check_row_order=False,
    active_color=(247, 255, 173),
    drag_direction="down"
)