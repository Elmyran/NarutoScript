from module.base.timer import Timer
from module.exception import GameStuckError
from tasks.base.assets.assets_base_page import *
from tasks.base.page import page_ji_fen_sai
from tasks.base.taskui import TaskUI
from tasks.ji_fen_sai.assets.assets_ji_fen_sai_reward import JI_FEN_SAI_REWARD



class JiFenSaiClaim(TaskUI):
    def run(self):
        self.device.click_record_clear()
        self.device.stuck_record_clear()
        self.handle_ji_fen_sai_claim()
    def handle_ji_fen_sai_claim(self):
        self.ui_ensure(page_ji_fen_sai)
        self._claim_daily_reward()
        return True
    def _claim_daily_reward(self):
        time=Timer(2,count=3).start()
        for _ in self.loop():
            if time.reached():
                break
            if self.appear_then_click(JI_FEN_SAI_REWARD,interval=1):
                time.reset()
                continue
            
            


