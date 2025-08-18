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
        self.ui_ensure(page_friend_panel)
        self._friend_gifts_give()
        self._friend_gifts_claim()
        self.ui_goto_main()

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
                return True
            if self.appear_then_click(GIFTS_CLAIM,interval=1):
                continue

        for _ in self.loop():
            if time.reached():
                raise GameStuckError("friend gifts confirm failed")
            if self.appear_then_click(GIFTS_CLAIM_CONFIRM):
                continue
            if self.appear(GIFTS_CLAIM_CHECK):
                break
            if self.appear_then_click(GIFTS_CLAIM,interval=1):
                continue
        return True


az=FriendGifts('alas',task='Alas')
az.device.screenshot()
az.ui_goto_main()