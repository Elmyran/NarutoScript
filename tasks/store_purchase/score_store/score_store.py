from tasks.base.ui import UI
from tasks.base.page import page_store
from tasks.store_purchase.score_store.keywords import ScoreStoreItem
from tasks.store_purchase.score_store.preset import ScoreStoreSelector
from tasks.store_purchase.store_keyword import PlayStore, ScoreStore
from tasks.store_purchase.store_tab_draglist import StoreTabList, SubsidiaryStoreTabList


class ScoreStorePurchase(UI):
    def run(self):
        if self.config.ScoreStore_ScoreStoreExchange:
            self.handle_score_store_purchase()
        
    def handle_score_store_purchase(self):
        self.ui_ensure(page_store)
        StoreTabList.search_rows(main=self,keyword=PlayStore)
        SubsidiaryStoreTabList.search_rows(self, ScoreStore)
        selector=ScoreStoreSelector(self)
        selector.purchase_items(ScoreStoreItem)
   
        