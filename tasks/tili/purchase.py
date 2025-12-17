

from module.base.timer import Timer
from module.logger.logger import logger
from module.ocr.ocr import Digit
from tasks.base.assets.assets_base_code_second import CODE_SECOND_PASSWORD
from tasks.base.assets.assets_base_page import MAIN_GOTO_CHARACTER
from tasks.base.taskui import TaskUI
from tasks.tili.assets.assets_tili_purchase import MAIN_GOTO_TILI_PURCHASE, TILI_PURCHASE_BUTTON, TILI_PURCHASE_CHECK, TILI_PURCHASE_POPUP_CLOSE, TILI_PURCHASE_REMAIN_TIMES


class TiLiPurchase(TaskUI):
    def run(self):
        if self.config.stored.TiLiPurchaseFinishCount.is_expired():
            self.config.stored.TiLiPurchaseFinishCount.clear()
        if self.config.stored.TiLiPurchaseFinishCount.is_full():
            return True
        self.handle_purchase()
        self.config.stored.TiLiPurchaseFinishCount.add()
    def handle_purchase(self):
        self.enter_purchase_page()
        self.purchase()
        self.back_to_main()
    def enter_purchase_page(self):
        for _ in self.loop():
            if self.appear(TILI_PURCHASE_CHECK):
                break 
            if self.appear_then_click(MAIN_GOTO_TILI_PURCHASE,interval=2):
                continue
    def purchase(self):
        ocr=Digit(TILI_PURCHASE_REMAIN_TIMES)
        remain_total=ocr.ocr_single_line(self.device.image)
        if remain_total==0:
            return True
        target_times=self.config.TiLiPurchase_TiLiPurchaseTimes
        real_times=min(target_times,remain_total)
        final_times=remain_total-real_times
        click_interval = Timer(1, count=3).start()  
        for _ in self.loop():
            if self.appear(CODE_SECOND_PASSWORD):
                self.handle_second_password()
                click_interval.reset()
                continue  
            if click_interval.reached():  
                remain_times = ocr.ocr_single_line(self.device.image)  
                if remain_times==final_times:
                    break  
                self.appear_then_click(TILI_PURCHASE_BUTTON, interval=0)
                click_interval.reset()
    def back_to_main(self):
        for _ in self.loop():
            if self.match_template_color(MAIN_GOTO_CHARACTER):
                break
            if self.appear_then_click(TILI_PURCHASE_POPUP_CLOSE,interval=1):
                continue

            
            