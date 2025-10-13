


from tasks.base.task_tab.ocr import TaskTabOcr
from module.ui.draggable_list import DraggableList
from tasks.base.page import *
from tasks.base.task_tab.task_keyword import TaskTab
from module.logger import logger
from tasks.base.assets.assets_base_task_tab import *


class DraggableTaskTabList(DraggableList):
    drag_vector=(0.9, 0.95)
    def is_row_selected(self, button, main):
        return super().is_row_selected(button, main)

    def search_rows(self, main, keyword):
        self.adapt_special_ui(main)
        if TASK_TAB_LIST.insight_row(keyword, main=main):
            logger.info('Successfully navigated to ' + keyword.name + ' area')
            if TASK_TAB_LIST.select_row(keyword, main=main):
                logger.info('Successfully selected ' + keyword.name + ' tab')
                return True
            else:
                logger.error(f'Failed to select {keyword.name} tab')
                return False
        else:
            logger.error(f'Failed to find {keyword.name} in task list')
            return False
    def adapt_special_ui(self, main):
        if main.appear(BACK_GAME_CHECK):
            self.search_button=MANUAL_TAB_SEARCH_AREA_FOR_BACK_GAME
        




TASK_TAB_LIST = DraggableTaskTabList(
    name='TaskTabList',
    keyword_class=TaskTab,
    ocr_class=TaskTabOcr,
    search_button=MANUAL_TAB_SEARCH_AREA,
    check_row_order=False,
    active_color=(212,190,143),
    drag_direction="down",
)