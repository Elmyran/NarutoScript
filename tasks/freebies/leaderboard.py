
from tasks.base.page import page_main
from tasks.base.task_tab.draglist import TASK_TAB_LIST
from tasks.base.task_tab.task_keyword import LeaderBoardKeyword
from tasks.base.ui import UI
from tasks.freebies.assets.assets_freebies_leaderboard import *


class LeaderBoard(UI):
    def run(self):
        if self.config.stored.LeaderBoardFinishCount.is_expired():
            self.config.stored.LeaderBoardFinishCount.clear()
        if self.config.stored.LeaderBoardFinishCount.is_full():
            return True
        if not self.handle_leader_board():
            return False
        self.config.stored.LeaderBoardFinishCount.add()  
        return True
    def handle_leader_board(self):
        self.device.click_record_clear()
        self.ui_ensure(page_main)
        if not TASK_TAB_LIST.search_rows(main=self,keyword=LeaderBoardKeyword):
            return False
        for _ in self.loop():
            if LEADER_BOARD_HAVE_LIKED.match_template_luma(self.device.image,direct_match=True):
                break
            if self.appear_then_click(LEADER_BOARD_LIKE_BUTTON,interval=1):
                continue
        


