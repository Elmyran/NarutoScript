from module.base.timer import Timer
from module.exception import GameStuckError
from tasks.base.page import page_welfare_station
from tasks.base.ui import UI
from tasks.information_club.assets.assets_information_club import *


class InformationClub(UI):
    def run(self):
        self.handle_information_club()
        self.config.task_delay(server_update=True)
        self.config.task_stop()

    def handle_information_club(self):
        self.device.click_record_clear()
        self.ui_ensure(page_welfare_station)
        time=Timer(20,30).start()
        for _ in  self.loop():
            if time.reached():
                raise GameStuckError('Information club claim stuck')
            if self.appear_then_click(DAILY_SIGN_IN_SUCCESS,similarity=0.9):
                continue
            if self.appear_then_click(DAILY_SIGN_IN_BUTTON,similarity=0.9):
                continue
            if self.appear(DAILY_SIGN_IN_HAVE_DONE,interval=1):
                break
        self.ui_goto_main()

