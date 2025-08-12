from module.base.timer import Timer
from module.exception import GameStuckError
from module.logger import logger
from tasks.base.page import page_main
from tasks.base.ui import UI
from tasks.organization.assets.assets_organization_fortress import ORGANIZATION_ENTER, ORGANIZATION_MAIN_PAGE, \
    ORGANIZATION_GOTO_FORTRESS, FORTRESS_LOCAL_SELECT, FORTRESS_FIRE, FORTRESS_ENTER_CONFIRM, FORTRESS_PAGE, \
    FORTRESS_MATCHING
from tasks.organization.assets.assets_organization_pray import ORGANIZATION_RED_DOT, MAIN_GOTO_ORGANIZATION, \
    ORGANIZATION_PANEL
from tasks.organization.move import SimpleRightMover


class Fortress(UI):
    def handle_organization_fortress(self):
        self.device.click_record_clear()
        self.ui_ensure(page_main)
        self._organization_panel_enter()
        self._organization_goto_fortress()
        self._fortress_goto_fight()
    def _organization_panel_enter(self):
        self.device.swipe([0, 322], [1280, 314])
        move = True
        time = Timer(10, count=10).start()
        m=2
        for _ in self.loop():
            ORGANIZATION_RED_DOT.load_search((200, 100, 1100, 400))
            if self.appear_then_click(ORGANIZATION_RED_DOT):
                continue
            MAIN_GOTO_ORGANIZATION.load_search((200, 100, 1100, 400))
            if MAIN_GOTO_ORGANIZATION.match_template(self.device.image,direct_match=True):
                move = False
                continue
            if self.appear(ORGANIZATION_MAIN_PAGE):
                break
            if self.appear(ORGANIZATION_PANEL):
                if self.appear(ORGANIZATION_ENTER):
                    self.device.click(ORGANIZATION_ENTER)
                continue
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
                    raise GameStuckError("Organization Pray Stucked")
        logger.info(f"Organization Panel entered")

    def _organization_goto_fortress(self):
        for  _ in self.loop():
            if self.appear(FORTRESS_PAGE):
                break
            if self.appear(FORTRESS_ENTER_CONFIRM):
                self.device.click(FORTRESS_ENTER_CONFIRM)
                continue
            if self.appear(FORTRESS_FIRE):
                self.device.click(FORTRESS_FIRE)
                continue
            if self.appear(FORTRESS_LOCAL_SELECT):
                self.device.click(FORTRESS_LOCAL_SELECT)
                continue
            if self.appear(ORGANIZATION_GOTO_FORTRESS):
                self.device.click(ORGANIZATION_GOTO_FORTRESS)
                continue
    def _check_still_in_fortress(self):
        for _ in self.loop():
            if self.appear(FORTRESS_MATCHING):
                return True

    def _fortress_goto_fight(self):
        mover = SimpleRightMover(self.config,self.device)
        mover.move_right_until_condition(self._check_still_in_fortress())
        #todo 识别战斗状态，采用丰饶之间一二技能和普攻轮换




