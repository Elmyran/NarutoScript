from tasks.base.ui import UI

from tasks.organization.pray import Pray


class Organization(UI):
    def run(self):
        if self.config.Organization_OrganizationPray:
            Pray(self.config,self.device).handle_Organization_Pray()


        self.config.task_delay(server_update=True)
        self.config.task_stop()

