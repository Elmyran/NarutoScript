
from module.base.timer import Timer
from tasks.base.page import page_manual,page_leader_board

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
        self.ui_ensure(page_manual)
        TASK_TAB_LIST.search_rows(self, LeaderBoardKeyword)
        self.ui_ensure(page_leader_board)
        time=Timer(2, count=4).start()    
        for _ in self.loop():
            if time.reached():
                break
            LEADER_BOARD_LIKE_BUTTON.load_search(LIKE_BUTTON_AREA.area)
            if self.match_template_color(LEADER_BOARD_LIKE_BUTTON):
                self.device.click(LEADER_BOARD_LIKE_BUTTON)
                time.reset()
                continue
        return True




