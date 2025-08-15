import re
from datetime import timedelta, datetime
from module.ocr.ocr import Duration
from module.ui.switch import Switch
from tasks.recruit.assets.assets_recruit_ui import *

class RecruitSwitch(Switch):
    SEARCH_BUTTON = RECRUIT_TAB_SEARCH

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
SWITCH_RECRUIT_TAB = RecruitSwitch('RecruitTab', is_selector=True)
SWITCH_RECRUIT_TAB.add_state(
    state='高级招募',
    check_button=PREMIUM_RECRUIT_CHECK,
    click_button=PREMIUM_RECRUIT_CLICK

)
SWITCH_RECRUIT_TAB.add_state(
    '限定招募',
    check_button=RECRUIT_LIMITED_RETURN_CHECK,
    click_button=RECRUIT_LIMITED_RETURN_CLICK

)
SWITCH_RECRUIT_TAB.add_state(
    '普通招募',
    check_button=NORMAL_RECRUIT_CHECK,
    click_button=NORMAL_RECRUIT_CLICK

)
SWITCH_RECRUIT_TAB.add_state(
    '祈愿夺宝',
    check_button=RECRUIT_PRAY_FOR_TREASURES_CHECK,
    click_button=RECRUIT_PRAY_FOR_TREASURES_CLICK

)
class RecruitDuration(Duration):
    @classmethod
    def timedelta_regex(cls, lang):
        if lang == 'cn':
            # 专门匹配 "HH:MM:SS后免费" 格式
            return re.compile(r'(?P<hours>\d{1,2}):(?P<minutes>\d{1,2}):(?P<seconds>\d{1,2})后.*?免费')
        return super().timedelta_regex(lang)

    def format_result(self, result: str) -> datetime:
        matched = self.timedelta_regex(self.lang).search(result)
        if not matched:
            return datetime.now()  # Return current time if no match

        hours = self._sanitize_number(matched.group('hours'))
        minutes = self._sanitize_number(matched.group('minutes'))
        seconds = self._sanitize_number(matched.group('seconds'))

        # Return future datetime when recruit will be available
        return datetime.now() + timedelta(hours=hours, minutes=minutes, seconds=seconds)