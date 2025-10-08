from tasks.base.ui import UI
from tasks.base.page import *
from tasks.store_purchase.assets.assets_store_purchase_privilege_store import DAILY_FREE_COINS, DAILY_FREE_COINS_DONE
from tasks.store_purchase.privilege_store.switch import SWITCH_PRIVILEGE_STORE_TAB
from tasks.store_purchase.store_tab_draglist import StoreTabList, SubsidiaryStoreTabList
from tasks.store_purchase.store_keyword import PrivilegeStore, Store

class PrivilegeStorePurchase(UI):
    def run(self):
        self.handle_privilege_store_purchase()
    def handle_privilege_store_purchase(self):
        if self.config.stored.PrivilegeStoreFinishCount.is_expired():
            self.config.stored.PrivilegeStoreFinishCount.clear()
        if self.config.stored.PrivilegeStoreFinishCount.is_full():
            return
        self.ui_ensure(page_store)
        if self.config.PrivilegeStore_DailyFreeCoins:
            self.handle_daily_free_coins()
    def handle_daily_free_coins(self):
        StoreTabList.search_rows(self,Store)
        SubsidiaryStoreTabList.search_rows(self, PrivilegeStore)
        SWITCH_PRIVILEGE_STORE_TAB.set(main=self, state='特权积分')
        for _ in self.loop():
            if self.appear(DAILY_FREE_COINS_DONE):
                break
            if self.appear_then_click(DAILY_FREE_COINS, interval=1):
                continue
        self.config.stored.PrivilegeStoreFinishCount.add()

