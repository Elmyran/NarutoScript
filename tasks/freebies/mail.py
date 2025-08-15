from module.base import button
from module.base.timer import Timer
from module.exception import GameStuckError
from module.logger import logger

from tasks.base.page import  page_main, page_mail
from tasks.base.ui import UI
from tasks.freebies.assets.assets_freebies_mail import *


class MailReward(UI):
    def _mail_enter(self):
        """
        Pages:
            in: page_menu
            out: MAIL_CHECK
        """
        logger.info('Mail enter')
        time=Timer(10,count=15).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError("Mail enter failed")
            if self.appear(MAIL_CHECK):
                logger.info('Mail enter success')
                break
            if self.appear_then_click(MAIL_RED_DOT,interval=1,similarity=0.9):
                continue

    def _mail_exit(self):
        """
        Pages:
            in: MAIL_CHECK
            out: page_menu
        """
        logger.info('Mail exit')

        time=Timer(5,count=10).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError("Mail exit failed")
            if self.ui_page_appear(page_main):
                logger.info('go to page main')
                break
            if  self.appear_then_click(MAIL_EXIT):
                logger.info('Mail exit done')






    def _mail_claim(self):
        """
        Pages:
            in: CLAIM_ALL
            out: CLAIM_ALL_DONE
        """
        logger.info('Mail claim all')
        time=Timer(4,count=8).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError("Mail claim all failed")
            if self.appear(CLAIM_ALL_DONE):
                break
            if self.appear(CLAIM_ALL):
                self.device.click(CLAIM_ALL)






    def handle_mail_reward(self):
        """
        Claim mails and exit

        Returns:
            bool: If claimed

        Pages:
            in: page_menu
            out: page_menu
        """
        self.device.click_record_clear()
        self.ui_ensure(page_mail)
        self._mail_claim()
        self.ui_goto_main()




    def _mail_delete(self):
        timeout = Timer(1.5, count=3).start()
        for _ in self.loop():
            if self.appear_then_click(CLAIM_DELETE,interval=1):
                continue
            if self.appear_then_click(CLAIM_DELETE_POPUP,interval=1):
                break
            if timeout.reached():
                break


