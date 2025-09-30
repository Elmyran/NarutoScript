
import numpy as np
import cv2
from module.base.button import Button, ClickButton
from module.base.timer import Timer
from module.base.utils.utils import area_offset, crop, rgb2gray
from module.exception import ScriptError
from module.logger import logger
from module.ocr.ocr import Digit, DigitCounter, Ocr
from tasks.base.assets.assets_base_page import FULL_SCREEN, STORE_CHECK
from tasks.store_purchase.assets.assets_store_purchase import BUY_BUTTON, BUY_REACH_TOP, PURCHASE_POPUP, STORE_ITEM_PURCHASE_AMOUNT_AREA
from tasks.store_purchase.ocr import StoreDetailOcr, StoreDigitCounter, StorePriceDigit

class StoreSelector:
    def __init__(self, main):
        self.main = main
        self.filter_ = None
        self.ocr_results = []
        self.currency=0
        self.relative_areas = None
    def search(self, keyword):
        ...
    def recognition(self,keyword):
        ...



    def load_filter(self):
        ...


    def get_priority_keywords_from_filter(self):  
        if not self.filter_:  
            return []  
        return self.filter_.filter_raw
    def purchase_items(self,keyword_class):  
        """
        Usage: purchase items based on the priority
        """
        self.load_filter()  
        priority_name = self.filter_.filter_raw
        priority_keyword = []  
        for name in priority_name:  
            try:  
                instance = keyword_class.find_name(name)  
                priority_keyword.append(instance)  
            except ScriptError:  
                print(f"找不到名为 {name} 的 keyword 实例")
        
        logger.info(f"Purchase priority: {priority_keyword}")
        for keyword in priority_keyword:  
            if not self.search(keyword): 
                logger.warning(f"No item found for {keyword.cn}") 
                continue
            item=self.recognition(keyword)
            if self.purchase_single_item(item):
                break
            
        
        
    def purchase_single_item(self, item):
        if not item : 
            return False
        if item.amount==0:  
            logger.info(f"Currency not enough to purchase {item.name}")
            return True
        if item.amount==1:
            self.ocr_currency(self.relative_areas['currency_area'])
            click_interval=Timer(1).start()
            pre_currency=self.currency
            for _ in self.main.loop():  
                self.ocr_currency(self.relative_areas['currency_area'])
                if self.currency<item.price :
                    logger.info(f"Currency not enough to purchase {item.name}")
                    return True
                elif pre_currency!=self.currency :
                    logger.info(f"{item.name} have been purchased")
                    break
                if click_interval.reached():  
                    self.main.device.click(item)  
                    click_interval.reset()
            return False
        logger.info(f"Purchasing item: {item}")
        click_interval=Timer(1).start()
        for _ in self.main.loop():
            if self.main.appear(PURCHASE_POPUP):
                logger.info("Detected purchase popup.")
                break
            if click_interval.reached():
                self.main.device.click(item)
                click_interval.reset()
        amount_ocr=StorePriceDigit(STORE_ITEM_PURCHASE_AMOUNT_AREA)
        for _ in self.main.loop():
            amount=amount_ocr.ocr_single_line(self.main.device.image)
            if amount==item.amount or self.main.appear(BUY_REACH_TOP):
                break
            if self.main.appear_then_click(PURCHASE_POPUP,interval=2):  
                continue
        for _ in self.main.loop():
            if self.main.match_template_color(STORE_CHECK):  
                break
            if self.main.appear_then_click(BUY_BUTTON,interval=1):  
                continue
        
        return False
            
    def ocr_item_price_and_amount(self, price_area,amount_area):  
        price_ocr=StorePriceDigit(
            ClickButton(
                area=price_area,
                name='ItemPriceDigit'
        ))
        price=price_ocr.ocr_single_line(self.main.device.image)
        amount_ocr=StoreDigitCounter(
             ClickButton(
                area=amount_area,
                name='ItemAmountDigit'
                )
        )
        current,remain,total=amount_ocr.ocr_single_line(self.main.device.image)
        if total!=0:
            return price,current,remain,total
        return price,0,0,0
    def ocr_currency(self,area):  
        currency_ocr=StorePriceDigit(
            ClickButton(
                area=area,
                name='CurrencyDigit'
            )
        )
        currency=currency_ocr.ocr_single_line(self.main.device.image)
        self.currency=currency
        
    def create_shop_item_from_ocr(self,button):  
        # 1. OCR识别商品名称  
        
        if not button:  
            return None  

        self.calculate_relative_areas(button.area)
        # 2. 计算相对区域  
        relative_areas = self.relative_areas
        
        # 3. 创建Item对象  
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
        # 5. OCR价格信息  
        price,current,remain,total = self.ocr_item_price_and_amount(price_area=relative_areas['price_area'],amount_area=relative_areas['amount_area'])  
        self.ocr_currency(self.relative_areas['currency_area'])
        currency=self.currency
        item.price = price
        afford_amount=int(currency/price)
        item.amount=min(remain,afford_amount)
        item.sold=current
        item.total=total
        return item
class Item:
    IMAGE_SHAPE = (96, 96)

    def __init__(self, image, button):
        """
        Args:
            image:
            button:
        """
        self.image_raw = image
        self._button = button
        image = crop(image, button.area)
        if image.shape == self.IMAGE_SHAPE:
            self.image = image
        else:
            self.image = cv2.resize(image, self.IMAGE_SHAPE, interpolation=cv2.INTER_CUBIC)
        self.is_valid = self.predict_valid()
        self._name = 'DefaultItem'
        self.amount = 1
        self._cost = 'DefaultCost'
        self.price = 0
        self.tag = None
        self.total = 0
        self.sold=0


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        """
        Args:
            value (str): Item name, such as 'PlateGeneralT3'. Suffix in name will be ignore.
                For example, 'Javelin' and 'Javelin_2' are different templates, but have same output name 'Javelin'.
        """
        if '_' in value:
            pre, suffix = value.rsplit('_', 1)
            if suffix.isdigit():
                value = pre
        self._name = value

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, value):
        if '_' in value:
            pre, suffix = value.rsplit('_', 1)
            if suffix.isdigit():
                value = pre
        self._cost = value

    def is_known_item(self):
        if self.name == 'DefaultItem':
            return False
        elif self.name.isdigit():
            return False
        else:
            return True

    def __str__(self):
        if self.name != 'DefaultItem' and self.cost == 'DefaultCost':
            name = f'{self.name}_x{self.amount}'
        elif self.name == 'DefaultItem' and self.cost != 'DefaultCost':
            name = f'{self.cost}_x{self.price}'
        else:
            name = f'{self.name}_x{self.amount}_{self.cost}_x{self.price}'

        if self.tag is not None:
            name = f'{name}_{self.tag}'

        return name

    def predict_valid(self):
        return np.mean(rgb2gray(self.image) > 127) > 0.1

    @property
    def button(self):
        return self._button.button

    def crop(self, area):
        return crop(self.image_raw, area_offset(area, offset=self._button.area[:2]))

    def __eq__(self, other):
        # For de-redundancy in Filter.apply()
        return str(self) == str(other)

    def __hash__(self):
        # For de-redundancy in merging two get items images
        return hash(self.name)
