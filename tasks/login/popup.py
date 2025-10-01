from module.base.base import ModuleBase
from module.base.timer import Timer

from tasks.base.assets.assets_base_page import MAIN_GOTO_CHARACTER
from tasks.base.page import page_main
from tasks.base.ui import UI
from module.logger import logger

from tasks.login.assets.assets_login_popup import GAME_MAIN_ANNOUNCEMENT, GAME_IN_ADVERTISE, Daily_Bonus, RANK_UP


class GameInPopup(ModuleBase):

    def handle_game_popup(self):
        """
        Returns:
            bool: If clicked
        """
        logger.info('handle game popup')
        # CN user agreement popup
        timer=Timer(2,count=5).start()
        for _ in  self.loop():
            if timer.reached() and self.match_template_color(MAIN_GOTO_CHARACTER):
                return True

            if self.appear_then_click(GAME_MAIN_ANNOUNCEMENT,interval=1):
                timer.reset()
                continue
            if self.match_template_luma(GAME_IN_ADVERTISE,interval=1):
                self.device.click(GAME_IN_ADVERTISE)
                timer.reset()
                continue
            if self.appear_then_click(Daily_Bonus,interval=1):
                timer.reset()
                continue
            if self.appear_then_click(RANK_UP,interval=1):
                timer.reset()
                continue



    def is_game_popup(self):
        """
        Returns:
            bool: If clicked
        """
        # CN user agreement popup
        
        timer=Timer(2,count=2)
        for _ in  self.loop():
            if self.appear(GAME_MAIN_ANNOUNCEMENT):
                return True
            if self.match_template_luma(GAME_IN_ADVERTISE):
                return True
            if self.appear(Daily_Bonus):
                return True
            if self.appear(RANK_UP):
                return True
            if timer.reached():
                return False

        return False

