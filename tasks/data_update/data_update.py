from module.base.timer import Timer
from module.base.utils import crop
from module.logger import logger
from module.ocr.ocr import  Digit, DigitCounter
from tasks.base.page import page_main, page_recruit, page_store, page_tong_ling
from tasks.base.ui import UI
from tasks.data_update.assets.assets_data_update import DATA_COINS, DATA_GOLD, DATA_RECRUITMENT_TICKETS, \
    DATA_FAME, DATA_TI_LI
from tasks.data_update.ocr import DataDigit
from tasks.store_purchase.assets.assets_store_purchase_reward_store import CHAO_YING_DAYS_BASE, CHAO_YING_DAYS_CHECK, CHAO_YING_DAYS_CLICK_BUTTON, CHAO_YING_DAYS_LIMITED, CHAO_YING_DAYS_PREMIUM
from tasks.store_purchase.keyword.store_keyword import ChaoYingService, RewardsStore
from tasks.store_purchase.ui.store_tab_draglist import StoreTabList, SubsidiaryStoreTabList


class DataUpdate(UI):
    def run(self):
        self.handle_data_update()
        self.config.task_delay(server_update=True)
        self.config.task_stop()
    def handle_data_update(self):
        self._coins_and_gold()
        self._chao_ying_days()  

    def _coins_and_gold(self):
        self.ui_ensure(page_main)
        coins_ocr=DataDigit(DATA_COINS)
        gold_ocr=Digit(DATA_GOLD)
        ti_li_ocr=DigitCounter(DATA_TI_LI)
        coins_flag=False
        gold_flag=False
        ti_li_flag=False
        ti_li=0
        gold=0
        coins=0
        time=Timer(5,count=10).start()
        for _ in self.loop():
            if time.reached():
                logger.warning('get ti_li or coins or gold failed')
                break
            if coins_flag and gold_flag and ti_li_flag:
                break
            if not coins_flag:
                coins=coins_ocr.ocr_single_line(self.device.image)
                if coins>0:
                    coins_flag=True
            if not gold_flag:
                gold=gold_ocr.ocr_single_line(self.device.image)
                if gold>0:
                    gold_flag=True
            if not ti_li_flag:
                ti_li,remain,total=ti_li_ocr.ocr_single_line(self.device.image)
                if  ti_li>0 and total==200:
                    ti_li_flag=True
        with self.config.multi_set():
            self.config.stored.TiLi.value=ti_li
            self.config.stored.Coins.value=coins
            self.config.stored.Golds.value=gold
 
    def _fame(self):
        self.ui_ensure(page_tong_ling)
        fame=DataDigit(DATA_FAME)
        time=Timer(5,count=10).start()
        fames=0
        for _ in self.loop():
            if time.reached():
                logger.warning('get fame failed')
                break
            fames=fame.ocr_single_line(self.device.image)
            if fames > 0:
                break
        self.config.stored.Fame.value=fames
    def _mission(self):
        with self.config.multi_set():
            mission=self.config.stored.MissionAccept.value
            self.config.stored.Mission.value=mission
    def _chao_ying_days(self):
        stored = self.config.stored.ChaoYingDays
        remain = stored.predict_current()
        if remain > 0:
            # 未到期：只按刷新点衰减计数，不进游戏识别
            stored.value = remain
            logger.info(f'ChaoYing days tick: {remain}')
            return
        # 已到期（或首次无记录）：进游戏重新识别
        self.ui_ensure(page_store)
        StoreTabList.search_rows(main=self,keyword=RewardsStore)
        SubsidiaryStoreTabList.search_rows(self, ChaoYingService)
        click_interval=Timer(2).start()
        for _ in self.loop():
            if self.appear(CHAO_YING_DAYS_CHECK):
                break
            if click_interval.reached():
                self.device.click(CHAO_YING_DAYS_CLICK_BUTTON)
                click_interval.reset()
                continue
        ocr=Digit(CHAO_YING_DAYS_CHECK)
        areas = [CHAO_YING_DAYS_PREMIUM, CHAO_YING_DAYS_BASE, CHAO_YING_DAYS_LIMITED]  # 几个 ButtonWrapper
        images = [crop(self.device.image, a.area) for a in areas]
        res = ocr.ocr_multi_lines(images)   # 返回与 areas 等长的 [(天数, 置信度), ...]
        total_days = sum(item[0] for item in res)
        stored.value=total_days
        logger.info(f'ChaoYing total days: {total_days}')
if __name__ == '__main__':
    data=DataUpdate(config='ns', device='127.0.0.1:16384',task='Alas')
    data._chao_ying_days()







