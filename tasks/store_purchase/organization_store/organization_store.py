from tasks.base.taskui import TaskUI
from tasks.base.page import *
from tasks.store_purchase.ui.store_tab_draglist import StoreTabList, SubsidiaryStoreTabList
from tasks.store_purchase.keyword.store_keyword import PlayStore,OrganizationStore
from tasks.store_purchase.organization_store.preset import  MeritExchangeSelector


class OrganizationStorePurchase(TaskUI,MeritExchangeSelector):
    def run(self):
        if self.config.OrganizationStore_MeritExchange:
            self.handle_organization_store_purchase()
    def handle_organization_store_purchase(self):
        self.ui_ensure(page_store)
        self.merit_exchange()
    def merit_exchange(self):
        StoreTabList.search_rows(self,PlayStore)
        SubsidiaryStoreTabList.search_rows(self, OrganizationStore)
        self.purchase_items()
if __name__ == '__main__':
    from tasks.store_purchase.organization_store.keywords import  Jade
    az=OrganizationStorePurchase('ns',task='Alas')
    az.device.screenshot()
    az.search(Jade)
    item=az.recognition()
    az.purchase_single_item(item)
    #az.purchase_items()





        
   



        
        
