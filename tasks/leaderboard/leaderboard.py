from module.base.timer import Timer
from module.exception import GameStuckError
from tasks.base.page import page_main
from tasks.base.task_tab.draglist import TASK_TAB_LIST
from tasks.base.task_tab.keyword import LeaderBoardKeyword
from tasks.base.ui import UI
from tasks.leaderboard.assets.assets_leaderboard import *


class LeaderBoard(UI):
    def  run(self):
        self.handle_leader_board()
        self.config.task_delay(server_update=True)
        self.config.task_stop()

    def handle_leader_board(self):
        self.device.click_record_clear()
        self.ui_ensure(page_main)
        if not TASK_TAB_LIST.search_rows(main=self,keyword=LeaderBoardKeyword):
            raise GameStuckError(' Leaderboard Not Found')
        time=Timer(20,count=30).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError('Leader board like timed out')
            LEADER_BOARD_HAVE_LIKED.load_search(LEADER_BOARD_AREA.area)
            if LEADER_BOARD_HAVE_LIKED.match_template(self.device.image):
                break
            if self.appear_then_click(LEADER_BOARD_LIKE_BUTTON):
                continue

