from module.base.timer import Timer
from module.exception import GameStuckError
from tasks.base.assets.assets_base_page import *
from tasks.base.page import page_ji_fen_sai,page_manual
from tasks.base.task_tab.draglist import TASK_TAB_LIST

from tasks.base.task_tab.task_keyword import ScoreCompetitionKeyword
from tasks.base.ui import UI
from tasks.ji_fen_sai.assets.assets_ji_fen_sai import JI_FEN_SAI_REWARD



class JiFenSaiClaim(UI):
    def handle_ji_fen_sai_claim(self):
        self.device.click_record_clear()
        self.device.stuck_record_clear()
        self.ui_ensure(page_manual)
        TASK_TAB_LIST.search_rows(self,ScoreCompetitionKeyword)
        self.ui_ensure(page_ji_fen_sai)
        self._claim_daily_reward()

        return True
    def _claim_daily_reward(self):
        time=Timer(30,count=30).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError('JI Fen Sai Claim Stuck')
            if self.match_template_color(JI_FEN_SAI_CHECK):
                break
            if self.appear_then_click(JI_FEN_SAI_REWARD,interval=1):
                continue


