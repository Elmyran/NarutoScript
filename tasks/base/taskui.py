from module.exception import GamePageUnknownError
from module.logger import logger
from tasks.base.assets.assets_base_page import MAIN_GOTO_CHARACTER
from tasks.base.page import *
from tasks.base.task_tab.draglist import TASK_TAB_LIST
from tasks.base.ui import UI
from tasks.base.task_tab.task_keyword import *

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
        draglist_once=False
        current_page = self.ui_get_current_page()
        next_page = current_page.parent
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
            if current_page == page_main and next_page == page_manual:
                if self.appear_then_click(MAIN_GOTO_BACK_GAME):
                    continue
                if self.match_template_color(BACK_GAME_GOTO_MANUAL,interval=5):
                    self.device.click(BACK_GAME_GOTO_MANUAL)
                    continue                   
            if self.ui_page_appear(next_page): 
                current_page = next_page 
                next_page = current_page.parent
                self.handle_lang_check(current_page)  
                continue 
            if current_page == page_manual and next_page != page_main:
                if not draglist_once:
                    if not TASK_TAB_LIST.search_rows(self,Page2Keyword.get(next_page)):
                        raise GamePageUnknownError(f'Cannot find {Page2Keyword.get(next_page)} in manual')
                draglist_once=True
                # Other pages
            clicked = False
            if current_page.parent is not None:  
                if self.ui_page_appear(current_page): 
                    logger.info(f'Page switch: {current_page} -> {next_page}')  
                    self.handle_lang_check(current_page)  
                    if self.ui_page_confirm(current_page):  
                        logger.info(f'Page arrive confirm {current_page}')  
                    button = current_page.links[next_page]  
                    self.device.click(button)  
                    self.ui_button_interval_reset(button)  
                    # 点击后更新当前页面为下一页面  
                    clicked = True
                    continue  
            if clicked:
                continue

            # Additional
            if self.ui_additional():
                continue

            if self.handle_login_confirm():
                continue

        # Reset connection
        Page.clear_connection()
    def is_in_main(self, interval=0):
        self.device.stuck_record_add(MAIN_GOTO_CHARACTER)

        if interval and not self.interval_is_reached(MAIN_GOTO_CHARACTER, interval=interval):
            return False
        appear = False
        if MAIN_GOTO_CHARACTER.match_template_luma(self.device.image):
            if self.image_color_count(MAIN_GOTO_CHARACTER, color=(235, 235, 235), threshold=234, count=400):
                appear = True
        if appear and interval:
            self.interval_reset(MAIN_GOTO_CHARACTER, interval=interval)

        return appear

        