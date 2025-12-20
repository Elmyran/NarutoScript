
from module.base.timer import Timer
from module.logger import logger
from tasks.base.assets.assets_base_code_second import *
from tasks.base.assets.assets_base_task_tab import MANUAL_TAB_SEARCH_AREA, MANUAL_TAB_SEARCH_AREA_FOR_BACK_GAME
from tasks.base.page import *
from tasks.base.task_tab.draglist import TASK_TAB_LIST
from tasks.base.ui import UI
from tasks.base.task_tab.task_keyword import *
from module.exception import GameStuckError, RequestHumanTakeover
Page2Keyword={
page_survival_trail: SurvivalChallengeKeyword,
page_cultivation:CultivationPathKeyword,
page_feng_rao:FengRaoKeyword,
page_mi_jing:SecretRealmExplorationKeyword,
page_leader_board:LeaderBoardKeyword,
page_organization_panel:OrganizationKeyword,
page_ninjutsu:NinjaBattleKeyword,
page_squad:SquadRaidKeyword,
page_mission:MissionKeyword,
page_ji_fen_sai:ScoreCompetitionKeyword
}

class TaskUI(UI):
    def ui_goto(self, destination, skip_first_screenshot=True):
        """
        Args:
            destination (Page):
            skip_first_screenshot:
        """
        # Create connection
        Page.init_connection(destination)
        self.interval_clear(list(Page.iter_check_buttons()))
        logger.hr(f"UI goto {destination}")
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            # Destination page
            if self.ui_page_appear(destination):
                logger.info(f'Page arrive: {destination}')
                if self.ui_page_confirm(destination):
                    logger.info(f'Page arrive confirm {destination}')
                break
            
            # Other pages
            clicked = False
            for page in Page.iter_pages():
                if page.parent is None or page.check_button is None:
                    continue
                
                if self.ui_page_appear(page, interval=5):
                    logger.info(f'Page switch: {page} -> {page.parent}')
                    self.handle_lang_check(page)
                    if page==page_main:
                        if not self.ui_page_confirm(page):
                            logger.warning(f'Page confirm failed for {page}, skip clicking')  
                            continue
                        else:
                            logger.info(f'Page arrive confirm {page}')  
                    if page==page_manual:
                        if self.ui_page_confirm(page_manual):
                            logger.info(f'Page arrive confirm {page}')  
                            self.wait_until_stable(MANUAL_TAB_SEARCH_AREA)
                            if TASK_TAB_LIST.search_rows(self,Page2Keyword.get(page.parent)):
                                self.interval_reset(page_main.check_button)
                                self.interval_reset(page_manual.check_button)
                        else:
                            logger.info(f'Page confirm failed for {page}, skip clicking')
                            continue  
                    button = page.links[page.parent]
                    self.device.click(button)
                    self.ui_button_interval_reset(button)
                    clicked = True
                    break
            if clicked:
                continue

            # Additional
            if self.ui_additional():
                continue

            if self.handle_login_confirm():
                continue

        # Reset connection
        Page.clear_connection()

    def _ui_button_confirm(
            self,
            button,
            confirm=Timer(0.1, count=0),
            timeout=Timer(2, count=6),
            skip_first_screenshot=True
    ):
        confirm.reset()
        timeout.reset()
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            if timeout.reached():
                logger.warning(f'_ui_button_confirm({button}) timeout')
                return False

            if self.appear(button):
                if confirm.reached():
                    break
            else:
                confirm.reset()
        return True
    def ui_page_confirm(self, page):
        """
        Args:
            page (Page):

        Returns:
            bool: If handled
        """
        if page == page_main:
            if self._ui_button_confirm(page.check_button):
                return True
        if page== page_manual:
            if self._ui_button_confirm(page.check_button):
                return True

        return False
    def handle_second_password(self):
        code=self.config.Password_SecondPassword
        if not code :
            raise RequestHumanTakeover('SecondPassword need to fill')
        self.device.scrcpy_init()
        time=Timer(10,count=10).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError('Password Input Timeout, Game Restart Needed')
            if not self.enter_input():
                continue
            self.wait_until_stable(CODE_SECOND_PASSWORD_INPUT_CONFIRM,timer=
                                   Timer(0.5,count=3),
                                   timeout=Timer(1,count=5))
            self.clear_input()
            self.device._scrcpy_control.set_clipboard(code, paste=True)
            if self.check_input():
               return True
            

        
    def enter_input(self):
        CODE_SECOND_PASSWORD_INPUT_CONFIRM.load_search(FULL_SCREEN.area)
        if self.image_color_count(CODE_SECOND_PASSWORD_INPUT_CONFIRM, color=(255, 255, 255), count=10000, threshold=221):
            return True
          
        if self.appear_then_click(CODE_SECOND_PASSWORD,interval=2):
            return False
        
        return False
    def clear_input(self):
       for _ in range(10):  
            self.device._scrcpy_control.keycode(  
                keycode=67,  
                action=0  
            )  
            self.device._scrcpy_control.keycode(  
                keycode=67,  
                action=1  
            )
    def check_input(self):
        for _ in self.loop():
            if self.appear(CODE_SECOND_PASSOWRD_LOCKED):
                raise RequestHumanTakeover('SecondPassword Locked, Human Takeover Needed')
            if self.appear(CODE_SECOND_PASSWORD_ERROR):
                return False
            if self.appear(CODE_SECOND_PASSWORD_LENGTH_ERROR):
                return False
            if self.appear(CODE_SECOND_PASSWORD_INPUT_SUCCESS):
                return True
            if self.appear_then_click(CODE_SECOND_PASSWORD_CONFIRM,interval=1):
                continue
