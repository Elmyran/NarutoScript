from module.ui.switch import Switch
from tasks.battle_order.assets.assets_battle_order_ui import BATTLE_ORDER_LIST, BATTLE_ORDER_REWARD_CHECK, \
    BATTLE_ORDER_REWARD_CLICK, BATTLE_ORDER_WEEKLY_REWARD_CHECK, BATTLE_ORDER_WEEKLY_REWARD_CLICK, \
    BATTLE_ORDER_WEEKLY_TASK_CHECK, BATTLE_ORDER_WEEKLY_TASK_CLICK

class BattleOrderSwitch(Switch):
    SEARCH_BUTTON = BATTLE_ORDER_LIST

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

