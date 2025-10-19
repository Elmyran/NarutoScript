from module.logger import logger
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
                    if self.ui_page_confirm(page):
                        logger.info(f'Page arrive confirm {page}')
                    if self.ui_page_appear(page_manual) and page.parent != page_main:
                        TASK_TAB_LIST.search_rows(self,Page2Keyword.get(page.parent))
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


        