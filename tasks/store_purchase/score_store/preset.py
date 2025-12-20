from module.base.filter import MultiLangFilter
import re
from tasks.store_purchase.assets.assets_store_purchase_score_store import SCORE_MEDAL_AREA, SCORE_STORE_ITEM_SEARCH_AREA
from tasks.store_purchase.ocr import StoreDetailOcr
from tasks.store_purchase.score_store.keywords import AdvancedSummoningScrollFragment, ScoreStoreChest, ScoreStoreItem
from tasks.store_purchase.selector import  StoreSelector
from tasks.store_purchase.ui.store_item_draglist import ScoreStoreItemList

SCORE_STORE_ATTR='score_store'
SCORE_STORE_FILTER_PRESET = ('reset')  
SCORE_STORE_FILTER_ATTR = (SCORE_STORE_ATTR,) 
SCORE_STORE_FILTER = MultiLangFilter(  
    re.compile(r"(.*)"),  
    SCORE_STORE_FILTER_ATTR,  
    SCORE_STORE_FILTER_PRESET  
)
ScoreStorePreset="""
高级通灵卷轴碎片 > 积分赛宝箱
""" 
class ScoreStoreSelector(StoreSelector):
    def search(self, item):
        keyword = ScoreStoreItem.find(name=item)
        if not ScoreStoreItemList.search_rows(main=self,keyword=keyword):
            return False
        ocr=StoreDetailOcr(SCORE_STORE_ITEM_SEARCH_AREA)
        buttons=ocr.matched_ocr(image=self.device.image,keyword_classes=[keyword])
        for button in buttons:  
            if button.matched_keyword == keyword:  
                self.button = button  
                break
        return True
    def recognition(self):  
        item = super().recognition()
        if not item:
            return None
        purchased_count = item.total-item.count
        if self.button.matched_keyword is not AdvancedSummoningScrollFragment:
            afford_amount = int((item.currency - 1000) / item.price)
            afford_amount = max(0,afford_amount)
        else :
            afford_amount = int(item.currency / item.price)

        if  self.button.matched_keyword is ScoreStoreChest:
            preset_max_amount = self.main.config.ScoreStore_ScoreStoreChestPurchaseTimes
            if purchased_count >= preset_max_amount:  
                return None
            afford_amount = min(preset_max_amount - purchased_count , afford_amount)
        item.count = min(item.count , afford_amount)
        return item 
    
    def calculate_relative_areas(self, name_area):  
        x1, y1, x2, y2 = name_area   
        self.relative_areas = {    
        'buy_button_area': (x1-20, y1+172, x2+20, y2+172),    
        'soldout_check_area': (x1, y1, x2, y2),    
        'price_area': (x1-20, y1+172, x2+20, y2+180),    
        'click_area': (x1-20, y1+172, x2+20, y2+172) ,
        'amount_area': (x1, y1+123, x2+80, y2+123),
        'currency_area': SCORE_MEDAL_AREA.area,
    }  
        
        
    def load_filter(self):
        filter_ = SCORE_STORE_FILTER
        string = ""
        match self.config.ScoreStore_ScoreStoreExchangeFilter:
            case 'preset':
                string=ScoreStorePreset
            case 'custom':
                string = self.config.ScoreStore_CustomScoreStoreFilter
        filter_.load(string)
        self.filter_=filter_
