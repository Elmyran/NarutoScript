from tasks.base.ui import UI
class StorePurchase(UI):
    def run(self):
        from tasks.store_purchase.privilege_store.privilege_store import PrivilegeStorePurchase
        PrivilegeStorePurchase(config=self.config,device=self.device).run()
        from tasks.store_purchase.organization_store.organization_store import OrganizationStore
        OrganizationStore(config=self.config,device=self.device).run()
        self.config.task_delay(server_update=True)
        self.config.task_stop()

