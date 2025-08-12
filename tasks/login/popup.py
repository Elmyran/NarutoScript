from module.base.base import ModuleBase
from module.base.timer import Timer
from tasks.base.page import page_main
from tasks.base.ui import UI

from tasks.login.assets.assets_login_popup import GAME_MAIN_ANNOUNCEMENT, GAME_IN_ADVERTISE, Daily_Bonus, RANK_UP


class GameInPopup(ModuleBase):
    def handle_game_popup(self):
        """
        Returns:
            bool: If clicked
        """
        # CN user agreement popup
        timer=Timer(2,count=5).start()
        for _ in  self.loop():
            if timer.reached():
                return True
            if self.appear_then_click(GAME_MAIN_ANNOUNCEMENT):
                timer.reset()
                continue
            if self.appear_then_click(GAME_IN_ADVERTISE):
                timer.reset()
                continue
            if self.appear_then_click(Daily_Bonus):
                timer.reset()
                continue
            if self.appear_then_click(RANK_UP):
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
            if self.appear(GAME_IN_ADVERTISE):
                return True
            if self.appear(Daily_Bonus):
                return True
            if self.appear(RANK_UP):
                return True
            if timer.reached():
                return False



        return False
