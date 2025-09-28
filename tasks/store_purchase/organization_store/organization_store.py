

from tasks.base.ui import UI
from tasks.base.page import *
from tasks.store_purchase.organization_store.keywords import  MeritExchangeItem
from tasks.store_purchase.store_tab_draglist import StoreTabList, SubsidiaryStoreTabList
from tasks.store_purchase.store_keyword import PlayStore,OrganizationStore
from tasks.store_purchase.organization_store.preset import  MeritExchangeSelector


class OrganizationStorePurchase(UI):
    def run(self):
        if self.config.OrganizationStore_MeritExchange:
            self.handle_organization_store_purchase()
    def handle_organization_store_purchase(self):
        self.ui_ensure(page_store)
        self.merit_exchange()
    def merit_exchange(self):
        StoreTabList.search_rows(self,PlayStore)
        SubsidiaryStoreTabList.search_rows(self, OrganizationStore)
        selector=MeritExchangeSelector(main=self)
        selector.purchase_items(keyword_class=MeritExchangeItem)

        
   



        
        
