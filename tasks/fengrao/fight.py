from module.base.timer import Timer
from module.exception import GameStuckError
from tasks.base.page import  page_feng_rao
from tasks.combat.combat import Combat
from tasks.fengrao.assets.assets_fengrao import FENG_RAO_CHECK, FENG_RAO_FIGHT_SUCCESS, FENG_RAO_START_FIGHT_BUTTON, FENG_RAO_FIGHT_STATUS, FENG_RAO_HAVE_DONE


class FengRaoFight(Combat):
    def handle_feng_rao(self):
        self.device.click_record_clear()
        self.ui_ensure(page_feng_rao)
        if self.is_feng_rao_have_done():
            return True
        self.start_fight()
        self.single_round_combat(
            end_check=FENG_RAO_CHECK,
            end_confirm=FENG_RAO_FIGHT_SUCCESS
        )
        return True
    def is_feng_rao_have_done(self):
        time=Timer(3, count=5).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError("Feng Rao status check stucked")
            if self.appear(FENG_RAO_HAVE_DONE):
                return True
            if self.appear(FENG_RAO_START_FIGHT_BUTTON):
                return False
    def start_fight(self):
        for _ in self.loop():
            if self.appear_then_click(FENG_RAO_START_FIGHT_BUTTON,interval=1):
                continue
            if self.appear(FENG_RAO_FIGHT_STATUS):
                break




















