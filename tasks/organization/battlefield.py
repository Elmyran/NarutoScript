from module.base.timer import Timer
from module.exception import GameStuckError
from module.logger import logger

from tasks.base.page import page_main
from tasks.base.task_tab.draglist import TASK_TAB_LIST
from tasks.base.task_tab.keyword import OrganizationKeyword
from tasks.base.ui import UI
from tasks.organization.assets.assets_organization import ORGANIZATION_PANEL_GOTO_PAGE

from tasks.organization.assets.assets_organization_pray import ORGANIZATION_RED_DOT, MAIN_GOTO_ORGANIZATION, \
   ORGANIZATION


class Battlefield(UI):
    def handle_battle_field(self):
        self.ui_ensure(page_main)
        if not TASK_TAB_LIST.search_rows(main=self,keyword=OrganizationKeyword):
            raise GameStuckError(' Organization Not Found')
        self._organization_enter()
    def _organization_enter(self):
        self.device.swipe([0, 322], [1280, 314])
        time = Timer(10, count=10).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError('Organization Panel Goto Page Stuck')
            if self.appear_then_click(ORGANIZATION_PANEL_GOTO_PAGE,interval=0):
                continue
            if self.appear(ORGANIZATION):
                return True
        logger.info(f"Organization Page entered")


