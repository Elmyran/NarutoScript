from module.base.timer import Timer
from module.logger import logger
from module.ocr.ocr import Ocr, Digit, DigitCounter

from tasks.base.page import page_main, page_recruit, page_tong_ling
from tasks.base.ui import UI
from tasks.data_update.assets.assets_data_update import DATA_COINS, DATA_GOLD, DATA_RECRUITMENT_TICKETS, \
    DATA_FAME, DATA_TI_LI
from tasks.data_update.ocr import DataDigit


class DataUpdate(UI):
    def run(self):
        self.handle_data_update()
        self.config.task_delay(server_update=True)
        self.config.task_stop()
    def handle_data_update(self):
        self._coins_and_gold()
        self._recruit_tikit()
        self._fame()
    def _coins_and_gold(self):
        self.ui_ensure(page_main)
        coin=DataDigit(DATA_COINS)
        gold=Digit(DATA_GOLD)
        ti_li=DigitCounter(DATA_TI_LI)
        coins_flag=False
        gold_flag=False
        ti_li_flag=False
        time=Timer(5,count=10).start()
        for _ in self.loop():
            if time.reached():
                logger.warning('get coins and gold failed')
                break
            if coins_flag and gold_flag and ti_li_flag:
                break
            if not coins_flag:
                coins=coin.ocr_single_line(self.device.image)
                if coins:
                    self.config.stored.Coins.value=coins
                    coins_flag=True
            if not gold_flag:
                gold=gold.ocr_single_line(self.device.image)
                if gold>0:
                    self.config.stored.Golds.value=gold
                    gold_flag=True
            if not ti_li_flag:
                current,remain,total=ti_li.ocr_single_line(self.device.image)
                if current>0 and total==200:
                    self.config.stored.TiLi.value=current
                    ti_li_flag=True
    def _recruit_tikit(self):
        self.ui_ensure(page_recruit)
        ocr=Digit(DATA_RECRUITMENT_TICKETS)
        time=Timer(5,count=10).start()
        for _ in self.loop():
            if time.reached():
                logger.warning('get recruit tickets failed')
                break
            ticket=ocr.ocr_single_line(self.device.image)
            if ticket > 0:
                self.config.stored.Tickets.value=ticket
                break
    def _fame(self):
        self.ui_ensure(page_tong_ling)
        fame=DataDigit(DATA_FAME)
        time=Timer(5,count=10).start()
        for _ in self.loop():
            if time.reached():
                logger.warning('get fame failed')
                break
            fames=fame.ocr_single_line(self.device.image)
            if fames:
                self.config.stored.Fame.value=fames
                break
    def _mission(self):
        with self.config.multi_set():
            mission=self.config.stored.MissionAccept.value
            self.config.stored.Mission.value=mission







