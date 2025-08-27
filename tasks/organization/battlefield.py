from module.base.timer import Timer
from module.exception import GameStuckError
from module.logger import logger

from tasks.base.page import page_main
from tasks.base.ui import UI
from tasks.organization.assets.assets_organization import ORGANIZATION_PANEL_GOTO_PAGE

from tasks.organization.assets.assets_organization_pray import ORGANIZATION_RED_DOT, MAIN_GOTO_ORGANIZATION, \
   ORGANIZATION


class Battlefield(UI):
    def handle_battle_field(self):
        self.ui_ensure(page_main)
        self._organization_enter()
    def _organization_enter(self):
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
                    raise GameStuckError("Organization Pray Stucked")
            ORGANIZATION_RED_DOT.load_search((200, 100, 1100, 400))
            if self.appear_then_click(ORGANIZATION_RED_DOT,interval=0):
                continue
            MAIN_GOTO_ORGANIZATION.load_search((200, 100, 1100, 400))
            if MAIN_GOTO_ORGANIZATION.match_template(self.device.image,direct_match=True):
                move = False
                continue
            if self.appear_then_click(ORGANIZATION_PANEL_GOTO_PAGE,interval=0):
                continue
            if self.appear(ORGANIZATION):
                return True
        logger.info(f"Organization entered")

az=Battlefield('alas',task='Alas')
az.handle_battle_field()

