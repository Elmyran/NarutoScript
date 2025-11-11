from datetime import datetime
from module.base.timer import Timer
from module.logger import logger
from tasks.base.page import page_leader_board
from tasks.base.taskui import TaskUI
from tasks.freebies.assets.assets_freebies_leaderboard import *
import cv2

class LeaderBoard(TaskUI):
    def run(self):
        now =datetime.now() 
        if now.hour<8:
            logger.info(f'Not 8am yet, skip task')
            return False
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
        timeout = Timer(2, count=4).start()
        for _ in self.loop():
            if timeout.reached():
                LEADER_BOARD_LIKED.load_search(LIKE_BUTTON_AREA.area)
                if self.match_template_luma(LEADER_BOARD_LIKED):
                    if self.is_liked(LEADER_BOARD_LIKED):
                        logger.info('may be liked manuly')  
                        break
                    timeout.reset()
            LEADER_BOARD_LIKED_FLAG.load_search(LIKE_BUTTON_AREA.area)
            if self.match_template_luma(LEADER_BOARD_LIKED_FLAG):
                if self.image_color_count(LEADER_BOARD_LIKED_FLAG,color=(226,84,56)):
                    logger.info('Learderboard liked')   
                    break
            LEADER_BOARD_LIKE_BUTTON.load_search(LIKE_BUTTON_AREA.area)
            if self.appear_then_click(LEADER_BOARD_LIKE_BUTTON,interval=1):
                continue
        return True
    def is_liked(self,button, threshold=255, count=200):  
        image = self.image_crop(button,copy=True)
        r, g, b = cv2.split(image)  
        # 检查R=G=B  
        mask1 = cv2.absdiff(r, g)  
        mask2 = cv2.absdiff(g, b)  
        cv2.inRange(mask1, 0, 255 - threshold, dst=mask1)  
        cv2.inRange(mask2, 0, 255 - threshold, dst=mask2)  
        mask = cv2.bitwise_and(mask1, mask2)  
        sum_ = cv2.countNonZero(mask)  
        return sum_ > count


