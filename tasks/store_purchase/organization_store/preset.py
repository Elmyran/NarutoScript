
from module.base.filter import MultiLangFilter  
import re
from module.ocr.ocr import Ocr
from tasks.store_purchase.assets.assets_store_purchase_organization_store import ORGANIZATION_STORE_ITEM_SEARCH_AREA
from tasks.store_purchase.assets.assets_store_purchase_organization_store import MERIT_AREA
from tasks.store_purchase.ocr import StoreDetailOcr
from tasks.store_purchase.selector import StoreSelector
from tasks.store_purchase.store_item_draglist import OrganizationStoreItemList  

MERIT_EXCHANGE_ATTR='merit_exchange'
MERIT_EXCHANGE_FILTER_PRESET = ('reset')  
MERIT_EXCHANGE_FILTER_ATTR = (MERIT_EXCHANGE_ATTR,) 
MERIT_EXCHANGE_FILTER = MultiLangFilter(  
    re.compile(r"(.*)"),  
    MERIT_EXCHANGE_FILTER_ATTR,  
    MERIT_EXCHANGE_FILTER_PRESET  
)
MeritExchangePreset="""
GiftBox > Coins > ReincarnationStone > Jade
""" 
class MeritExchangeSelector(StoreSelector):
    def search(self, keyword):
        if not OrganizationStoreItemList.search_rows(main=self.main,keyword=keyword):
            return False
        return True
    def recognition(self,keyword):
        ocr=StoreDetailOcr(ORGANIZATION_STORE_ITEM_SEARCH_AREA)
        buttons=ocr.matched_ocr(image=self.main.device.image,keyword_classes=[keyword])
        target_button=None
        lang=self.main.config.LANG
        if lang=='auto':
            lang='cn'
        lang_value = getattr(keyword, lang, None)  
        for button in buttons:  
            if button.text == lang_value:
                target_button=button
                break
        item=self.create_shop_item_from_ocr(target_button)
        return item
       
    
    def calculate_relative_areas(self, name_area):  
        x1, y1, x2, y2 = name_area   
        self.relative_areas = {    
        'buy_button_area': (x1-20, y1+172, x2+20, y2+172),    
        'soldout_check_area': (x1, y1, x2, y2),    
        'price_area': (x1-20, y1+172, x2+20, y2+172),    
        'click_area': (x1-20, y1+172, x2+20, y2+172) ,
        'amount_area': (x1, y1+123, x2+80, y2+123),
        'currency_area': MERIT_AREA.area,
    }  
        
        
    def load_filter(self):
        filter_ = MERIT_EXCHANGE_FILTER
        string = ""
        match self.main.config.OrganizationStore_MeritExchangeFilter:
            case 'preset':
                string=MeritExchangePreset
            case 'custom':
                string = self.main.config.OrganizationStore_CustomMeritExchangeFilter
        filter_.load(string)
        self.filter_=filter_


