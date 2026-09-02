from tasks.base.page import page_feng_rao
from tasks.base.ui import UI
from tasks.fengrao.assets.assets_fengrao import FENG_RAO_CHAO_YING_CHECK, FENG_RAO_FIGHT_SUCCESS, FENG_RAO_HAVE_DONE, FENG_RAO_SKIP_CONFIRM, FENG_RAO_SKIP_FIGHT
from tasks.fengrao.fight import FengRaoFight

class FengRao(UI):
    def run(self):
        self.device.click_record_clear()
        self.ui_ensure(page_feng_rao)
        if self.appear(FENG_RAO_CHAO_YING_CHECK):
            self.config.stored.ChaoYingDays.mark_active()
            self.skip_fight()
        else:
            FengRaoFight(self.config,self.device).handle_feng_rao()
        self.config.task_delay(server_update=True)
        self.config.task_stop()
    def skip_fight(self):
        for _ in self.loop():
            if self.appear(FENG_RAO_HAVE_DONE):
                break
            if self.appear_then_click(FENG_RAO_FIGHT_SUCCESS,interval=1):
                continue
            if self.appear_then_click(FENG_RAO_SKIP_CONFIRM,interval=1):
                continue
            if self.appear_then_click(FENG_RAO_SKIP_FIGHT,interval=1):
                continue
            