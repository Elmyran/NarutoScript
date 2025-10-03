
from module.logger import logger
from tasks.base.ui import UI
class StorePurchase(UI):
    def run(self):
        from tasks.store_purchase.privilege_store.privilege_store import PrivilegeStorePurchase
        logger.hr('Privilege Store',level=1)
        PrivilegeStorePurchase(config=self.config,device=self.device).run()
        from tasks.store_purchase.organization_store.organization_store import OrganizationStorePurchase
        logger.hr('Organization Store',level=1)
        OrganizationStorePurchase(config=self.config,device=self.device).run()
        from tasks.store_purchase.survival_store.survival_store import SurvivalStorePurchase
        logger.hr('Survival Store',level=1)
        SurvivalStorePurchase(config=self.config,device=self.device).run()
        from tasks.store_purchase.score_store.score_store import ScoreStorePurchase
        logger.hr('Score Store',level=1)
        ScoreStorePurchase(config=self.config,device=self.device).run()
        self.config.task_delay(server_update=True)
        self.config.task_stop()

