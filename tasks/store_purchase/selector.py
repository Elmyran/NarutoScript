from locale import currency

from module.base.button import Button, ClickButton
from module.base.timer import Timer
from module.logger import logger
from tasks.base.assets.assets_base_code_second import CODE_SECOND_PASSWORD
from tasks.base.assets.assets_base_page import  STORE_CHECK
from tasks.store_purchase.assets.assets_store_purchase import BUY_AMOUNT_ADD, BUY_BUTTON, BUY_CONFIRM, BUY_REACH_TOP, BUY_SUCCESS, STORE_CURRENCY_NOT_ENOUGH
from tasks.store_purchase.item import Item
from tasks.store_purchase.ocr import  StorePriceDigit

class StoreSelector:
    def __init__(self):
        self.filter_ = None
        self.ocr_results = []
        self.relative_areas = None
        self.button=None
    def search(self, item : str):
        ...




    def load_filter(self):
        ...
    def purchase_items(self):  
        """
        Usage: purchase items based on the priority
        """
        self.load_filter()  
        items= self.filter_.filter_raw
        skip_first_screenshot = True  
        for item in items:  
            if skip_first_screenshot:  
                skip_first_screenshot = False  
            else:  
                self.device.screenshot()  
            if not self.search(item): 
                logger.warning(f"No item found for {item}") 
                continue
            item=self.recognition()
            if self.purchase_single_item(item):
                break
            
        
    def currency_recognition(self):  
        currency_ocr=StorePriceDigit(
            ClickButton(
                area=self.relative_areas['currency_area'],
                name='CurrencyDigit'
            )
        )
        currency=currency_ocr.ocr_single_line(self.device.image)
        return currency    
    def purchase_single_item(self, item):
        if not item : 
            return False
        if item.count==0:  
            logger.info(f"Currency not enough to purchase {item.name}")
            return True
        logger.info(f"Purchasing item: {item}")
        click_interval=Timer(1).start()
        purchase_times=0
        pre_currency=item.currency
        for _ in self.loop():
            if self.appear(BUY_AMOUNT_ADD):
                break
            if self.appear(STORE_CURRENCY_NOT_ENOUGH):
                logger.info(f"Currency not enough to purchase {item.name}")
                return False

            if self.appear(BUY_SUCCESS):
                continue
            if click_interval.reached():
                currency=self.currency_recognition()
                if pre_currency < currency:
                    purchase_times += 1
                    logger.info(f"Purchase confirmed ({purchase_times}/{item.count}).")
                if purchase_times >= item.count:
                    return False
                self.device.click(item)
                click_interval.reset()
                        
                
        
        for _ in self.loop():
            if self.appear(BUY_REACH_TOP):
                break
            if self.appear_then_click(BUY_AMOUNT_ADD,interval=2):  
                continue
        for _ in self.loop():
            if self.appear(BUY_REACH_TOP,similarity=0.6):
                continue
            if self.appear(BUY_SUCCESS) or self.match_template_color(STORE_CHECK):  
                break
            if self.appear(CODE_SECOND_PASSWORD):
                if self.handle_second_password():
                    self.purchase_single_item(item)
                    break
            if self.appear_then_click(BUY_CONFIRM,interval=2):
                continue
            if self.appear_then_click(BUY_BUTTON,interval=1):  
                continue
        return False
    def recognition(self):  
        button=self.button
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
        item = Item(self.device.image, item_button)  
        if not item.is_valid:
            logger.info(f'{item.name} sold out')
            return 
        item.name = button.text 
        item.recognition(relative_areas)
        item.check_count()
        return item
