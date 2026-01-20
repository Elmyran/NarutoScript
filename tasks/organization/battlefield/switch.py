from module.ui.switch import Switch
from tasks.base.assets.assets_base_character_switch import *


class CharacterTabSwitch(Switch):
    SEARCH_BUTTON = CHARACTER_TAB_SEARCH

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
CHARACTER_TAB = CharacterTabSwitch('RecruitTab', is_selector=True)
CHARACTER_TAB.add_state(
    state='忍者',
    check_button=CHARACTER_CHECK,
    click_button=CHARACTER_CLICK

)
CHARACTER_TAB.add_state(
    state='通灵',
    check_button=TONG_LING_CHECK,
    click_button=TONG_LING_CLICK

)
CHARACTER_TAB.add_state(
    state='秘卷',
    check_button=MI_JUAN_CHECK,
    click_button=MI_JUAN_CLICK

)
