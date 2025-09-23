from re import S
from tasks.store_purchase.assets.assets_store_purchase import *
from module.ocr.ocr import Ocr
from module.ui.draggable_list import DraggableList
from module.logger import logger
from tasks.store_purchase.store_keyword import StoreKeyword,SubsidiaryStoreKeyword
class StoreDragList(DraggableList):
    current_keyword=None
    def load_rows(self, main):
        """重写 load_rows 方法以适应商店界面"""
        super().load_rows(main=main)
        logger.info(f'Loaded {len(self.cur_buttons)}  tabs')
        for i, button in enumerate(self.cur_buttons):
            logger.info(f'Tab {i}: {button.matched_keyword}')

    def search_rows(self, main,keyword):
        self.current_keyword=keyword
        if StoreTabList.insight_row(keyword, main=main):
            logger.info('Successfully navigated to'+keyword.cn)
            if StoreTabList.select_row(keyword, main=main):
                logger.info('Successfully selected '+keyword.cn)
    def is_row_selected(self, button, main):
        if self.current_keyword.name=='Recommendation':
            RECOMMENDATION_SELECTED.load_search(STORE_TAB_LIST_AREA.area)
            if RECOMMENDATION_SELECTED.match_template(main.device.image):
                return True
        elif self.current_keyword.name=='Store':
            STORE_SELECTED.load_search(STORE_TAB_LIST_AREA.area)
            if STORE_SELECTED.match_template(main.device.image):
                return True
        elif self.current_keyword.name=='PlayStore':
            PLAY_STORE_SELECTED.load_search(STORE_TAB_LIST_AREA.area)
            if PLAY_STORE_SELECTED.match_template(main.device.image):
                return True
        elif self.current_keyword.name=='LimitedTimeSale':
            LIMITED_TIME_SALE_SELECTED.load_search(STORE_TAB_LIST_AREA.area)
            if LIMITED_TIME_SALE_SELECTED.match_template(main.device.image):
                return True
        return False
class SubsidiaryStoreDragList(DraggableList):
    current_keyword=None
    def load_rows(self, main):
        """重写 load_rows 方法以适应商店界面"""
        super().load_rows(main=main)
        logger.info(f'Loaded {len(self.cur_buttons)}  tabs')
        for i, button in enumerate(self.cur_buttons):
            logger.info(f'Tab {i}: {button.matched_keyword}')

    def search_rows(self, main,keyword):
        self.current_keyword=keyword
        if SubsidiaryStoreTabList.insight_row(keyword, main=main):
            logger.info('Successfully navigated to'+keyword.cn)
            if SubsidiaryStoreTabList.select_row(keyword, main=main):
                logger.info('Successfully selected '+keyword.cn)
    def is_row_selected(self, button, main):
        text_area = button.area
        top_line_area = (text_area[0], text_area[1] - 15, text_area[2], text_area[1])  
        bottom_line_area = (text_area[0], text_area[3], text_area[2], text_area[3] + 15)  
        top_has_gold = main.image_color_count(top_line_area, color=self.active_color, threshold=221, count=40)  
        bottom_has_gold = main.image_color_count(bottom_line_area, color=self.active_color, threshold=221, count=40) 
        if top_has_gold and  bottom_has_gold:
            return True
        return False
    
        
StoreTabList= StoreDragList(
    name='StoreTabList',
    keyword_class=StoreKeyword,
    ocr_class=Ocr,
    search_button=STORE_TAB_LIST_AREA,
    check_row_order=False,
    active_color=(247, 255, 173),
    drag_direction="down"
)
SubsidiaryStoreTabList= SubsidiaryStoreDragList(
    name='SubsidiaryStoreTabList',
    keyword_class=SubsidiaryStoreKeyword,
    ocr_class=Ocr,
    search_button=STORE_TAB_LIST_AREA,
    check_row_order=False,
    active_color=(255,255,165),
    drag_direction="down"
)