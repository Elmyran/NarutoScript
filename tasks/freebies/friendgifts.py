from logging import setLogRecordFactory

from module.exception import GameStuckError
from tasks.base.page import page_main, page_friend_panel
from tasks.base.ui import UI
from tasks.freebies.assets.assets_freebies_friendgifts import MAIN_GOTO_FRIEND_PANEL, GIFTS_GIVE, GIFTS_CLAIM, \
    GIFTS_CLAIM_CHECK, GIFTS_CLAIM_CONFIRM, FRIEND_PANEL_RED_DOT, GIVE_DONE, FRIEND_PANEL_GOTO_MAIN
from module.base.timer import Timer
from module.logger.logger import logger

class FriendGifts(UI):
    def handle_friend_gifts(self):
        self.device.click_record_clear()
        self.ui_ensure(page_main)
        self.ui_goto(page_friend_panel)
        self._friend_gifts_give()
        self._friend_gifts_claim()
        self._friend_gifts_exit()

    def _friend_gifts_give(self):
       time=Timer(8,count=10).start()
       for _ in self.loop():
        if time.reached():
            raise GameStuckError("friend gifts give failed")
        if self.appear(GIFTS_GIVE,interval=1):
            self.device.click(GIFTS_GIVE)
            continue
        if self.appear(GIVE_DONE):
            break


    def _friend_gifts_claim(self):
        time=Timer(8,count=10).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError("friend gifts claim failed")
            if self.appear(GIFTS_CLAIM_CONFIRM):
                break
            if self.appear(GIFTS_CLAIM_CHECK):
                return  True
            if self.appear(GIFTS_CLAIM,interval=1):
                self.device.click(GIFTS_CLAIM)
                continue

        for _ in self.loop():
            if time.reached():
                raise GameStuckError("friend gifts confirm failed")
            if self.appear(GIFTS_CLAIM_CHECK):
                break
            if self.appear_then_click(GIFTS_CLAIM_CONFIRM):
                continue
            if self.appear(GIFTS_CLAIM,interval=1):
                self.device.click(GIFTS_CLAIM)
                continue
        return True

    def _friend_gifts_exit(self):
        time=Timer(5,count=8).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError("friend gifts exit failed")
            if self.ui_page_appear(page_main):
                break
            if self.appear(FRIEND_PANEL_GOTO_MAIN,interval=1):
                self.device.click(FRIEND_PANEL_GOTO_MAIN)
                continue
