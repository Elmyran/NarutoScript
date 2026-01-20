from module.base.filter import MultiLangFilter  
import re
from tasks.store_purchase.assets.assets_store_purchase_organization_store import ORGANIZATION_STORE_ITEM_SEARCH_AREA
from tasks.store_purchase.assets.assets_store_purchase_organization_store import MERIT_AREA
from tasks.store_purchase.ocr import StoreDetailOcr
from tasks.store_purchase.organization_store.keywords import MeritExchangeItem
from tasks.store_purchase.selector import StoreSelector
from tasks.store_purchase.ui.store_item_draglist import OrganizationStoreItemList  

MERIT_EXCHANGE_ATTR='merit_exchange'
MERIT_EXCHANGE_FILTER_PRESET = ('reset')  
MERIT_EXCHANGE_FILTER_ATTR = (MERIT_EXCHANGE_ATTR,) 
MERIT_EXCHANGE_FILTER = MultiLangFilter(  
    re.compile(r"(.*)"),  
    MERIT_EXCHANGE_FILTER_ATTR,  
    MERIT_EXCHANGE_FILTER_PRESET  
)
MeritExchangePreset="""
组织饰品礼盒 > 铜币 > 轮回石 > 忍玉
""" 
class MeritExchangeSelector(StoreSelector):
    def search(self, item):
        keyword = MeritExchangeItem.find(name=item)
        if not OrganizationStoreItemList.search_rows(main=self,keyword=keyword):
            return False
        ocr=StoreDetailOcr(ORGANIZATION_STORE_ITEM_SEARCH_AREA)
        buttons=ocr.matched_ocr(image=self.device.image,keyword_classes=[keyword])
        for button in buttons:  
            if button.matched_keyword == keyword:  
                self.button = button  
                break
        return True

    
    def calculate_relative_areas(self, name_area):  
        x1, y1, x2, y2 = name_area   
        self.relative_areas = {    
        'buy_button': (x1-20, y1+172, x2+20, y2+172),    
        'soldout_check_area': (x1, y1, x2, y2),    
        'price_area': (x1-20, y1+172, x2+20, y2+180),    
        'click_area': (x1-20, y1+172, x2+20, y2+172) ,
        'amount_area': (x1, y1+123, x2+80, y2+123),
        'currency_area': MERIT_AREA.area,
    }  
        
        
    def load_filter(self):
        filter_ = MERIT_EXCHANGE_FILTER
        string = ""
        match self.config.OrganizationStore_MeritExchangeFilter:
            case 'preset':
                string=MeritExchangePreset
            case 'custom':
                string = self.config.OrganizationStore_CustomMeritExchangeFilter
        filter_.load(string)
        self.filter_=filter_


