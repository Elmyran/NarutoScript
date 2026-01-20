

from module.ui.switch import Switch
from tasks.store_purchase.assets.assets_store_purchase_privilege_store import PRIVILEGE_STORE_TAB_AREA
from tasks.store_purchase.assets.assets_store_purchase_privilege_store_ui import *
class PrivilegeStoreSwitch(Switch):
    SEARCH_BUTTON = PRIVILEGE_STORE_TAB_AREA

    def add_state(self, state, check_button, click_button=None):
        # Load search
        if check_button is not None:
            check_button.load_search(self.SEARCH_BUTTON.area)
        if click_button is not None:
            click_button.load_search(self.SEARCH_BUTTON.area)
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
SWITCH_PRIVILEGE_STORE_TAB = PrivilegeStoreSwitch('RecruitTab', is_selector=True)
SWITCH_PRIVILEGE_STORE_TAB.add_state(
    state='特权忍者',
    check_button=PRIVILEGE_CHARACTER_CHECK,
    click_button=PRIVILEGE_CHARACTER_CLICK

)
SWITCH_PRIVILEGE_STORE_TAB.add_state(
    state='特权道具',
    check_button=PRIVILEGE_ITEM_CHECK,
    click_button=PRIVILEGE_ITEM_CLICK

)
SWITCH_PRIVILEGE_STORE_TAB.add_state(
    state='特权积分',
    check_button=PRIVILEGE_SCORE_CHECK,
    click_button=PRIVILEGE_SCORE_CLICK

)
SWITCH_PRIVILEGE_STORE_TAB.add_state(
    state='特权月直购',
    check_button=PRIVILEGE_PURCHASE_CHECK,
    click_button=PRIVILEGE_PURCHASE_CLICK

)