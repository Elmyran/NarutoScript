from module.base.timer import Timer
from tasks.store_purchase.assets.assets_store_purchase import *
from module.ocr.ocr import Ocr
from module.ui.draggable_list import DraggableList
from module.logger import logger
from tasks.store_purchase.ocr import StoreDetailOcr
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
        check_area=(self.search_button.area[0],button.area[1],self.search_button.area[2],self.search_button.area[3])
        if self.current_keyword.name=='Recommendation':
            RECOMMENDATION_SELECTED.load_search(check_area)
            if RECOMMENDATION_SELECTED.match_template(main.device.image):
                return True
        elif self.current_keyword.name=='Store':
            STORE_SELECTED.load_search(check_area)
            if STORE_SELECTED.match_template(main.device.image):
                return True
        elif self.current_keyword.name=='PlayStore':
            PLAY_STORE_SELECTED.load_search(check_area)
            if PLAY_STORE_SELECTED.match_template(main.device.image):
                return True
        elif self.current_keyword.name=='LimitedTimeSale':
            LIMITED_TIME_SALE_SELECTED.load_search(check_area)
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
            main.wait_until_stable(  
                    self.search_button,  
                    timer=Timer(0.3, count=2),  # 连续0.3秒稳定  
                    timeout=Timer(2, count=4)   # 最多等待2秒  
                )  
            if SubsidiaryStoreTabList.select_row(keyword, main=main):
                logger.info('Successfully selected '+keyword.cn)
    
            

       
    
        
StoreTabList= StoreDragList(
    name='StoreTabList',
    keyword_class=StoreKeyword,
    ocr_class=StoreDetailOcr,
    search_button=STORE_TAB_LIST_AREA,
    check_row_order=False,
    active_color=(247, 255, 173),
    drag_direction="down"
)
SubsidiaryStoreTabList= SubsidiaryStoreDragList(
    name='SubsidiaryStoreTabList',
    keyword_class=SubsidiaryStoreKeyword,
    ocr_class=StoreDetailOcr,
    search_button=STORE_TAB_LIST_AREA,
    check_row_order=False,
    active_color=(218,30,31),
    drag_direction="down"
)