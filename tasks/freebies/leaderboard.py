from module.logger import logger
from tasks.base.page import page_leader_board
from tasks.base.taskui import TaskUI
from tasks.freebies.assets.assets_freebies_leaderboard import *


class LeaderBoard(TaskUI):
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
        self.ui_ensure(page_leader_board)
        for _ in self.loop():
            LEADER_BOARD_LIKE_BUTTON.load_search(LIKE_BUTTON_AREA.area)
            if self.appear(LEADER_BOARD_LIKE_BUTTON):
                logger.info('waiting for like button')
                break
        self.wait_until_stable(LIKE_BUTTON_AREA)
        for _ in self.loop():
            if not self.image_color_count(LIKE_BUTTON_AREA,color=(65,103,149)):
                break
            LEADER_BOARD_LIKE_BUTTON.load_search(LIKE_BUTTON_AREA.area)
            if self.match_template_color(LEADER_BOARD_LIKE_BUTTON):
                self.device.click(LEADER_BOARD_LIKE_BUTTON)
                continue
        return True








