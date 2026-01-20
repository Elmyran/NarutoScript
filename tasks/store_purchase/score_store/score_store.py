from tasks.base.taskui import TaskUI
from tasks.base.page import page_store
from tasks.store_purchase.score_store.preset import ScoreStoreSelector
from tasks.store_purchase.keyword.store_keyword import PlayStore, ScoreStore
from tasks.store_purchase.ui.store_tab_draglist import StoreTabList, SubsidiaryStoreTabList


class ScoreStorePurchase(TaskUI, ScoreStoreSelector):
    def run(self):
        if self.config.ScoreStore_ScoreStoreExchange:
            self.handle_score_store_purchase()
        
    def handle_score_store_purchase(self):
        self.ui_ensure(page_store)
        StoreTabList.search_rows(main=self,keyword=PlayStore)
        SubsidiaryStoreTabList.search_rows(self, ScoreStore)
        self.purchase_items()

if __name__ == '__main__':
    from tasks.store_purchase.score_store.keywords import AdvancedSummoningScrollFragment
    az=ScoreStorePurchase('ns',task='Alas')
    az.device.screenshot()
    az.search(AdvancedSummoningScrollFragment)
    item=az.recognition()
    az.purchase_single_item(item)

        