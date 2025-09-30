
from module.base.button import Button
from module.base.filter import MultiLangFilter
import re




from module.logger import logger
from tasks.store_purchase.assets.assets_store_purchase_score_store import SCORE_MEDAL_AREA, SCORE_STORE_ITEM_SEARCH_AREA
from tasks.store_purchase.ocr import StoreDetailOcr
from tasks.store_purchase.score_store.keywords import AdvancedSummoningScrollFragment, ScoreStoreChest
from tasks.store_purchase.selector import Item, StoreSelector
from tasks.store_purchase.store_item_draglist import ScoreStoreItemList

SCORE_STORE_ATTR='score_store'
SCORE_STORE_FILTER_PRESET = ('reset')  
SCORE_STORE_FILTER_ATTR = (SCORE_STORE_ATTR,) 
SCORE_STORE_FILTER = MultiLangFilter(  
    re.compile(r"(.*)"),  
    SCORE_STORE_FILTER_ATTR,  
    SCORE_STORE_FILTER_PRESET  
)
ScoreStorePreset="""
AdvancedSummoningScrollFragment > ScoreStoreChest
""" 
class ScoreStoreSelector(StoreSelector):
    def search(self, keyword):
        if not ScoreStoreItemList.search_rows(main=self.main,keyword=keyword):
            return False
        return True
    def recognition(self,keyword):
        ocr=StoreDetailOcr(SCORE_STORE_ITEM_SEARCH_AREA)
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
    
    def create_shop_item_from_ocr(self,button):  
        # 1. OCR识别商品名称  
        
        if not button:  
            return None  

        self.calculate_relative_areas(button.area)

        relative_areas = self.relative_areas
        
        
        item_button = Button(  
            search=button.search,
            file="temp_click", 
            area=relative_areas['soldout_check_area'],  
            color=(),  
            button=relative_areas['click_area']  
        )  
        
        item = Item(self.main.device.image, item_button)  
        item.name = button.text 
        if not item.is_valid:
            logger.info(f'{item.name} sold out')
            return 
        
        price,current,remain,total = self.ocr_item_price_and_amount(price_area=relative_areas['price_area'],amount_area=relative_areas['amount_area'])  
        self.ocr_currency(self.relative_areas['currency_area'])
        currency=self.currency
        item.price = price
        if button.matched_keyword is not AdvancedSummoningScrollFragment:
            afford_amount = int((currency - 1000) / price)
            afford_amount=max(0,afford_amount)
        else :
            afford_amount = int(currency / price)

        if  button.matched_keyword is ScoreStoreChest:
            preset_max_amount=self.main.config.ScoreStore_ScoreStoreChestPurchaseTimes
            if current>=preset_max_amount:  
                return 
            afford_amount=min(preset_max_amount-current,afford_amount)
        item.amount=min(remain,afford_amount)
        item.sold=current
        item.total=total
        return item
    
    def calculate_relative_areas(self, name_area):  
        x1, y1, x2, y2 = name_area   
        self.relative_areas = {    
        'buy_button_area': (x1-20, y1+172, x2+20, y2+172),    
        'soldout_check_area': (x1, y1, x2, y2),    
        'price_area': (x1-20, y1+172, x2+20, y2+172),    
        'click_area': (x1-20, y1+172, x2+20, y2+172) ,
        'amount_area': (x1, y1+123, x2+80, y2+123),
        'currency_area': SCORE_MEDAL_AREA.area,
    }  
        
        
    def load_filter(self):
        filter_ = SCORE_STORE_FILTER
        string = ""
        match self.main.config.ScoreStore_ScoreStoreExchangeFilter:
            case 'preset':
                string=ScoreStorePreset
            case 'custom':
                string = self.main.config.ScoreStore_CustomScoreStoreFilter
        filter_.load(string)
        self.filter_=filter_
