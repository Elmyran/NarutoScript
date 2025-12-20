from tasks.base.taskui import TaskUI
from tasks.base.page import page_store
from tasks.store_purchase.keyword.store_keyword import PlayStore, SurvivalStore
from tasks.store_purchase.ui.store_tab_draglist import StoreTabList, SubsidiaryStoreTabList
from tasks.store_purchase.survival_store.preset import SurvivalStoreSelector


class SurvivalStorePurchase(TaskUI,SurvivalStoreSelector):
    def run(self):
        if self.config.SurvivalStore_SurvivalStoreExchange:
            self.handle_survival_store_purchase()
        
    def handle_survival_store_purchase(self):
        self.ui_ensure(page_store)
        StoreTabList.search_rows(main=self,keyword=PlayStore)
        SubsidiaryStoreTabList.search_rows(self, SurvivalStore)
        self.purchase_items()

if __name__ == '__main__':
    from tasks.store_purchase.survival_store.keywords import TsuchikuraFragment
    az=SurvivalStorePurchase('ns',task='Alas')
    az.config.Password_SecondPassword='123456'
    az.device.screenshot()
    az.search(TsuchikuraFragment)
    item=az.recognition()
    az.purchase_single_item(item)