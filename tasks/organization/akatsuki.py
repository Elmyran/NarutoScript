

from module.base.timer import Timer
from module.config.utils import get_server_next_monday_update
from module.exception import GameStuckError
from module.logger import logger
from tasks.base.page import page_organization_panel,page_manual

from tasks.base.task_tab.draglist import TASK_TAB_LIST
from tasks.base.task_tab.task_keyword import OrganizationKeyword
from tasks.base.ui import UI
from tasks.organization.assets.assets_organization_akatsuki import *
from tasks.organization.assets.assets_organization_pray import *

class Akatsuki(UI):
    def run(self):
        if self.handle_pursue_akatsuki():
            monday = get_server_next_monday_update(self.config.Scheduler_ServerUpdate)
            self.config.task_delay(target=monday)
        else:
            self.config.task_delay(server_update=True)
        self.config.task_stop()

   
        
       
    def handle_pursue_akatsuki(self):
        self.device.click_record_clear()
        self.ui_ensure(page_manual)
        TASK_TAB_LIST.search_rows(self,OrganizationKeyword)
        self.ui_ensure(page_organization_panel)
        self._organization_play_panel_enter()
        self._enter_akatsuki_page()
        return self._reward_claim()
       

    def _organization_play_panel_enter(self):
        time = Timer(10, count=10).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError("Organization Play Panel Stucked")
            if self.appear(ORGANIZATION_GOTO_PRAY,interval=1):
                break
            if self.appear(ORGANIZATION_PLAY_PANEL):
                self.device.click(ORGANIZATION_PLAY_PANEL)
                continue
        logger.info(f"Organization Play Panel entered")
    def _enter_akatsuki_page(self):
        time=Timer(8, count=10).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError("Organization Akatsuki Enter Stucked")
            if self.appear(AKATSUKI_CHECK):
                break
            if self.appear_then_click(ORGANIZATION_GOTO_AKATSUKI,interval=1):
                continue


    def _reward_claim(self):
        self.device.click_record_clear()
        time=Timer(3, count=5).start()
        for _ in self.loop():
            if time.reached():
                return False
            if self.appear(REWARD_HAVE_CLAIMED):
                return True
            if self.appear_then_click(REWARD_CLAIM_ALL,interval=0):
                time.reset()
                continue
            REWARD_CLAIM_BUTTON.load_search(REWARD_CLAIM_PANEL.area)
            if self.appear_then_click(REWARD_CLAIM_BUTTON,interval=1):
                time.reset()
                continue
            if self.appear_then_click(AKATSUKI_GOTO_REWARD,interval=1):
                time.reset()
                continue
            
            
            
    
