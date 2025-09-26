from sympy import true
from tasks.store_purchase.assets.assets_store_purchase import *
from module.ocr.ocr import Ocr
from module.ui.draggable_list import DraggableList
from module.logger import logger
from tasks.store_purchase.organization_store import keywords
from tasks.store_purchase.organization_store.preset import MeritExchangeItem

class ItemDragList(DraggableList):
    current_keyword=None
    def load_rows(self, main):
        """重写 load_rows 方法以适应商店界面"""
        super().load_rows(main=main)
        logger.info(f'Loaded {len(self.cur_buttons)}  tabs')
        for i, button in enumerate(self.cur_buttons):
            logger.info(f'Tab {i}: {button.matched_keyword}')

    def search_rows(self, main,keyword):
        self.current_keyword=keyword
        if StoreItemList.insight_row(keyword, main=main):
            logger.info('Successfully navigated to'+keyword.cn)
            if StoreItemList.select_row(keyword, main=main):
                logger.info('Successfully selected '+keyword.cn)
    def is_row_selected(self, button, main):
        return True
    

        
StoreItemList= ItemDragList(
    name='StoreItemList',
    keyword_class=MeritExchangeItem,
    ocr_class=Ocr,
    search_button=STORE_ITEM_SEARCH_AREA,
    check_row_order=False,
    drag_direction="right"
)
