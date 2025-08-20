import re
from datetime import timedelta, datetime
from module.ocr.ocr import Duration
from module.ui.switch import Switch
from tasks.battle_order.assets.assets_battle_order_ui import BATTLE_ORDER_LIST, BATTLE_ORDER_REWARD_CHECK, \
    BATTLE_ORDER_REWARD_CLICK, BATTLE_ORDER_WEEKLY_REWARD_CHECK, BATTLE_ORDER_WEEKLY_REWARD_CLICK, \
    BATTLE_ORDER_WEEKLY_TASK_CHECK, BATTLE_ORDER_WEEKLY_TASK_CLICK
from tasks.recruit.assets.assets_recruit_ui import *

class BattleOrderSwitch(Switch):
    SEARCH_BUTTON = BATTLE_ORDER_LIST
    def add_state(self, state, check_button, click_button=None):
        # Load search
        if check_button is not None:
            check_button.load_search(RECRUIT_TAB_SEARCH.area)
        if click_button is not None:
            click_button.load_search(RECRUIT_TAB_SEARCH.area)
        return super().add_state(state, check_button, click_button)

    def click(self, state, main):
        """
        Args:
            state (str):
            main (ModuleBase):
        """
        button = self.get_data(state)['click_button']
        _ = main.appear(button)  # Search button to load offset
        main.device.click(button)
BATTLE_ORDER_TAB = BattleOrderSwitch('BattleOrderTab', is_selector=True)
BATTLE_ORDER_TAB.add_state(
    state='奖励',
    check_button=BATTLE_ORDER_REWARD_CHECK,
    click_button=BATTLE_ORDER_REWARD_CLICK

)
BATTLE_ORDER_TAB.add_state(
    state='周任务',
    check_button=BATTLE_ORDER_WEEKLY_TASK_CHECK,
    click_button=BATTLE_ORDER_WEEKLY_TASK_CLICK


)
BATTLE_ORDER_TAB.add_state(
    state='周活跃',
    check_button=BATTLE_ORDER_WEEKLY_REWARD_CHECK,
    click_button=BATTLE_ORDER_WEEKLY_REWARD_CLICK
)

