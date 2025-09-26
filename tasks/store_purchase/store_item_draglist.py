import numpy as np
from module.base.base import ModuleBase
from module.base.utils.utils import area_size, random_rectangle_vector_opted
from tasks.store_purchase.assets.assets_store_purchase import *
from module.ocr.ocr import Ocr
from module.ui.draggable_list import DraggableList
from module.logger import logger
from tasks.store_purchase.organization_store import keywords
from tasks.store_purchase.organization_store.keywords import MeritExchangeItem
from tasks.store_purchase.assets.assets_store_purchase_organization_store import SAFE_DRAG_AREA
class ItemDragList(DraggableList):
   
    def load_rows(self, main):
        """重写 load_rows 方法以适应商店界面"""
        super().load_rows(main=main)
        logger.info(f'Loaded {len(self.cur_buttons)}  tabs')
        for i, button in enumerate(self.cur_buttons):
            logger.info(f'Tab {i}: {button.matched_keyword}')
   
    def drag_page(self, direction: str, main: ModuleBase, vector=None):
        """
        Args:
            direction: up, down, left, right
            main:
            vector (tuple[float, float]): Specific `drag_vector`, None by default to use `self.drag_vector`
        """
        if vector is None:
            vector = self.drag_vector
        vector = np.random.uniform(*vector)
        width, height = area_size(SAFE_DRAG_AREA.button)
        if direction == 'up':
            vector = (0, vector * height)
        elif direction == 'down':
            vector = (0, -vector * height)
        elif direction == 'left':
            vector = (vector * width, 0)
        elif direction == 'right':
            vector = (-vector * width, 0)
        else:
            logger.warning(f'Unknown drag direction: {direction}')
            return

        p1, p2 = random_rectangle_vector_opted(vector, box=SAFE_DRAG_AREA.button)
        main.device.drag(p1, p2, name=f'{self.name}_DRAG')
    def search_rows(self, main,keyword):
        self.current_keyword=keyword
        if StoreItemList.insight_row(keyword, main=main):
            logger.info('Successfully navigated to'+keyword.cn)
            return True
            
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
