from module.base.filter import MultiLangFilter  
import re
from tasks.store_purchase.assets.assets_store_purchase_survival_store import HEAVEN_EARTH_SCROLL_AREA, SURVIVAL_STORE_ITEM_SEARCH_AREA
from tasks.store_purchase.ocr import StoreDetailOcr
from tasks.store_purchase.selector import StoreSelector
from tasks.store_purchase.survival_store.keywords import SurvivalStoreItem
from tasks.store_purchase.ui.store_item_draglist import SurvivalStoreItemList  

SURVIVAL_STORE_ATTR='survival_store'
SURVIVAL_STORE_FILTER_PRESET = ('reset')  
SURVIVAL_STORE_FILTER_ATTR = (SURVIVAL_STORE_ATTR,) 
SURVIVAL_STORE_FILTER = MultiLangFilter(  
    re.compile(r"(.*)"),  
    SURVIVAL_STORE_FILTER_ATTR,  
    SURVIVAL_STORE_FILTER_PRESET  
)
SurvivalStorePreset="""
土台碎片 > 轮回石
""" 
class SurvivalStoreSelector(StoreSelector):
    def search(self, item):
        keyword = SurvivalStoreItem.find(name=item)
        if not SurvivalStoreItemList.search_rows(main=self,keyword=keyword):
            return False
        ocr=StoreDetailOcr(SURVIVAL_STORE_ITEM_SEARCH_AREA)
        buttons=ocr.matched_ocr(image=self.device.image,keyword_classes=[keyword])
        for button in buttons:  
            if button.matched_keyword == keyword:  
                self.button = button  
                break
        return True

  
       
    
    def calculate_relative_areas(self, name_area):  
        x1, y1, x2, y2 = name_area   
        self.relative_areas = {    
        'buy_button_area': (x1-20, y1+172, x2+20, y2+172),    
        'soldout_check_area': (x1, y1, x2, y2),    
        'price_area': (x1-20, y1+172, x2+20, y2+180),    
        'click_area': (x1-20, y1+172, x2+20, y2+172) ,
        'amount_area': (x1, y1+123, x2+80, y2+123),
        'currency_area': HEAVEN_EARTH_SCROLL_AREA.area,
    }  
        
        
    def load_filter(self):
        filter_ = SURVIVAL_STORE_FILTER
        string = ""
        match self.config.SurvivalStore_SurvivalStoreExchangeFilter:
            case 'preset':
                string=SurvivalStorePreset
            case 'custom':
                string = self.config.SurvivalStore_CustomSurvivalStoreFilter
        filter_.load(string)
        self.filter_=filter_


