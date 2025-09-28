
from module.base.filter import MultiLangFilter  
import re
from module.ocr.ocr import Ocr
from tasks.store_purchase.assets.assets_store_purchase_survival_store import HEAVEN_EARTH_SCROLL_AREA, SURVIVAL_STORE_ITEM_SEARCH_AREA
from tasks.store_purchase.selector import StoreSelector
from tasks.store_purchase.store_item_draglist import SurvivalStoreItemList  

SURVIVAL_STORE_ATTR='survival_store'
SURVIVAL_STORE_FILTER_PRESET = ('reset')  
SURVIVAL_STORE_FILTER_ATTR = (SURVIVAL_STORE_ATTR,) 
SURVIVAL_STORE_FILTER = MultiLangFilter(  
    re.compile(r"(.*)"),  
    SURVIVAL_STORE_FILTER_ATTR,  
    SURVIVAL_STORE_FILTER_PRESET  
)
SurvivalStorePreset="""
TsuchikuraFragment > ReincarnationStone
""" 
class SurvivalStoreSelector(StoreSelector):
    def search(self, keyword):
        if not SurvivalStoreItemList.search_rows(main=self.main,keyword=keyword):
            return False
        return True
    def recognition(self,keyword):
        ocr=Ocr(SURVIVAL_STORE_ITEM_SEARCH_AREA)
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
        'currency_area': HEAVEN_EARTH_SCROLL_AREA.area,
    }  
        
        
    def load_filter(self):
        filter_ = SURVIVAL_STORE_FILTER
        string = ""
        match self.main.config.OrganizationStore_MeritExchangeFilter:
            case 'preset':
                string=SurvivalStorePreset
            case 'custom':
                string = self.main.config.OrganizationStore_CustomMeritExchangeFilter
        filter_.load(string)
        self.filter_=filter_


