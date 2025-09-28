from tasks.base.ui import UI
from tasks.base.page import page_store
from tasks.store_purchase.store_keyword import PlayStore, SurvivalStore
from tasks.store_purchase.store_tab_draglist import StoreTabList, SubsidiaryStoreTabList
from tasks.store_purchase.survival_store.keywords import SurvivalStoreItem
from tasks.store_purchase.survival_store.preset import SurvivalStoreSelector


class SurvivalStorePurchase(UI):
    def run(self):
        if self.config.SurvivalStore_SurvivalStoreExchange:
            self.handle_survival_store_purchase()
        
    def handle_survival_store_purchase(self):
        self.ui_ensure(page_store)
        StoreTabList.search_rows(main=self,keyword=PlayStore)
        SubsidiaryStoreTabList.search_rows(self, SurvivalStore)
        selector=SurvivalStoreSelector(main=self)
        selector.purchase_items(SurvivalStoreItem)
        