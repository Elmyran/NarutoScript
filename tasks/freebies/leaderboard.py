from module.base.timer import Timer
from module.exception import GameStuckError
from tasks.base.page import page_main
from tasks.base.task_tab.draglist import TASK_TAB_LIST
from tasks.base.task_tab.keyword import LeaderBoardKeyword
from tasks.base.ui import UI
from tasks.freebies.assets.assets_freebies_leaderboard import *


class LeaderBoard(UI):
    def handle_leader_board(self):
        if self.config.stored.LeaderBoardLikeCount.is_expired():
            self.config.stored.LeaderBoardLikeCount.clear()
        if self.config.stored.LeaderBoardLikeCount.is_full():
            return True
        self.device.click_record_clear()
        self.ui_ensure(page_main)
        if not TASK_TAB_LIST.search_rows(main=self,keyword=LeaderBoardKeyword):
            return False
        time=Timer(20,count=30).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError('Leader board like timed out')
            if self.appear(LEADER_BOARD_HAVE_LIKED):
                break
            if self.appear_then_click(LEADER_BOARD_LIKE_BUTTON,interval=1):
                continue
        self.config.stored.LeaderBoardLikeCount.add()

