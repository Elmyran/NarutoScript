
from module.base.timer import Timer
from module.config.utils import get_server_next_monday_update
from module.exception import GameStuckError
from module.logger import logger
from tasks.base.page import page_main
from tasks.base.ui import UI
from tasks.organization.assets.assets_organization_akatsuki import *
from tasks.organization.assets.assets_organization_pray import *

class Akatsuki(UI):
    def run(self):
        self.handle_pursue_akatsuki()
        monday = get_server_next_monday_update(self.config.Scheduler_ServerUpdate)
        self.config.task_delay(target=monday)
        self.config.task_stop()
    def handle_pursue_akatsuki(self):
        self.device.click_record_clear()
        self.ui_ensure(page_main)
        self._organization_panel_enter()
        self._enter_akatsuki_panel()
        result=self._reward_claim()
        self._akatsuki_exit()
        return result
    def _organization_panel_enter(self):
        self.device.swipe([0, 322], [1280, 314])
        move = True
        time = Timer(10, count=10).start()
        m=2
        for _ in self.loop():
            if time.reached():
                if move and m%2==0:
                    self.device.swipe( [1200, 314],[0, 322])
                    time.reset()
                    m=m+1
                elif move and m%2==1:
                    self.device.swipe([0, 322], [1200, 314])
                    m=m+1
                    time.reset()
                elif m>5:
                    raise GameStuckError("Organization Play Panel Stucked")
            if self.appear(ORGANIZATION_GOTO_PRAY,interval=1):
                break
            if self.appear(ORGANIZATION_PLAY_PANEL):
                self.device.click(ORGANIZATION_PLAY_PANEL)
                continue
            ORGANIZATION_RED_DOT.load_search((200, 100, 1100, 400))
            if self.appear_then_click(ORGANIZATION_RED_DOT):
                continue
            MAIN_GOTO_ORGANIZATION.load_search((200, 100, 1100, 400))
            if MAIN_GOTO_ORGANIZATION.match_template(self.device.image,direct_match=True):
                move = False
                continue

        logger.info(f"Organization Play Panel entered")
    def _enter_akatsuki_panel(self):
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
            if time.reached() and self.appear(AKATSUKI_DONE):
                return True
            if self.appear(AKATSUKI_REWARD_CHECK):
                break
            if self.appear(AKATSUKI_REWARD_RED_DOT):
                self.device.click(AKATSUKI_REWARD_RED_DOT)
            elif time.reached():
                return  False
        claim_time=Timer(20, count=30).start()
        times=0
        for _ in self.loop():
            if claim_time.reached():
                raise GameStuckError("Akatsuki Reward Claim Stucked")
            REWARD_HAVE_CLAIMED.load_search(REWARD_CLAIM_PANEL.area)
            success = REWARD_HAVE_CLAIMED.match_multi_template(self.device.image)
            if success and len(success) == 5:
                self.device.swipe([1028,593],[1027,201])
                times+=1
                if times>3 :
                    break
                continue
            if self.appear_then_click(REWARD_CLAIM_ALL,interval=0):
                continue
            if self.appear_then_click(REWARD_CLAIM_BUTTON,interval=1):
                continue
    def _akatsuki_exit(self):
        self.device.click_record_clear()
        time=Timer(10, count=10).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError("Akatsuki Exit Stucked")
            if self.ui_page_appear(page_main):
                break
            if self.appear(REWARD_PANEL_EXIT):
                self.device.click(REWARD_PANEL_EXIT)
                continue
            if self.appear(AKATSUKI_EXIT):
                self.device.click(AKATSUKI_EXIT)
                continue
            if self.appear(ORGANIZATION_EXIT):
                self.device.click(ORGANIZATION_EXIT)
                continue

