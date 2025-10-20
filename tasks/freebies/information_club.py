from module.base.timer import Timer
from module.exception import GameStuckError
from tasks.base.page import page_welfare_station
from tasks.base.ui import UI
from tasks.freebies.assets.assets_freebies_information_club import *


class InformationClub(UI):


    def handle_information_club(self):
        if self.config.stored.InformationClubSignInCount.is_expired():
            self.config.stored.InformationClubSignInCount.clear()
        if self.config.stored.InformationClubSignInCount.is_full():
            return True
        self.device.click_record_clear()
        self._sign_in_information_club()
        self.config.stored.InformationClubSignInCount.add()
    def _sign_in_information_club(self):
        self.ui_ensure(page_welfare_station)
        time=Timer(20,30).start()
        for _ in  self.loop():
            if time.reached():
                raise GameStuckError('Information club claim stuck')
            if self.match_template_color(DAILY_SIGN_IN_HAVE_DONE):
                break
            if self.appear_then_click(DAILY_SIGN_IN_SUCCESS,interval=1):
                continue
            if self.match_template_color(DAILY_SIGN_IN_BUTTON,interval=1):
                self.device.click(DAILY_SIGN_IN_BUTTON)
                continue
