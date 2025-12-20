import cv2
import numpy as np
from module.base.button import ClickButton
from module.base.utils.utils import area_offset, crop, rgb2gray
from module.logger.logger import logger
from tasks.store_purchase.ocr import StoreDigitCounter, StorePriceDigit


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
        self.count = 1
        self._cost = 'DefaultCost'
        self.price = 0
        self.tag = None
        self.total = 0
        self.currency=0



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
    def recognition(self,relative_areas):
        price_ocr=StorePriceDigit(
            ClickButton(
                area=relative_areas['price_area'],
                name='ItemPriceDigit'
        ))
        logger.info(f'Item Price Area: {relative_areas["price_area"]}')
        amount_ocr=StoreDigitCounter(
             ClickButton(
                area=relative_areas['amount_area'],
                name='ItemAmountDigit'
                )
        )
        currency_ocr=StorePriceDigit(
             ClickButton(
                area=relative_areas['currency_area'],
                name='CurrencyDigit'
                )
        )
        logger.info(f'Item Amount Area: {relative_areas["amount_area"]}')
        price=price_ocr.ocr_single_line(self.image_raw)
        _,remain,total=amount_ocr.ocr_single_line(self.image_raw)
        currency=currency_ocr.ocr_single_line(self.image_raw)
        if price==0:
            price=99999
        self.price=price
        self.total=total
        self.count=remain
        self.currency=currency
    def check_count(self):
        afford_amount=int(self.currency/self.price)
        self.count=min(self.count,afford_amount)



    def __str__(self):
        if self.name != 'DefaultItem' and self.cost == 'DefaultCost':
            name = f'{self.name}_x{self.count}'
        elif self.name == 'DefaultItem' and self.cost != 'DefaultCost':
            name = f'{self.cost}_x{self.price}'
        else:
            name = f'{self.name}_x{self.count}_{self.cost}_x{self.price}'

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
