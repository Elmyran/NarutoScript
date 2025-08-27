from module.base.base import ModuleBase
from module.base.timer import Timer
from module.logger import logger
from module.ocr.keyword import Keyword
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
    def insight_row(self, row: Keyword, main: ModuleBase, skip_first_screenshot=True) -> bool:
        """重写以处理动态活动列表"""
        logger.info(f'Insight activity tab: {row}')

        # 首先尝试在当前可见范围内查找
        self.load_rows(main=main)
        if self.keyword2button(row, show_warning=False):
            return True

            # 如果找不到，遍历整个列表
        visited = set()
        for direction in ['down', 'up']:  # 先向下再向上
            while True:
                self.load_rows(main=main)
                if self.keyword2button(row, show_warning=False):
                    return True

                    # 检查是否到达列表末尾
                current_buttons = {btn.matched_keyword.name for btn in self.cur_buttons}
                if current_buttons.issubset(visited):
                    break
                visited.update(current_buttons)

                self.drag_page(direction, main=main)
                # 等待稳定
                main.wait_until_stable(self.search_button, timer=Timer(0, count=0), timeout=Timer(1.5, count=5))

        return False
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