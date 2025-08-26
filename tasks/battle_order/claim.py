
from module.base.timer import Timer
from tasks.base.assets.assets_base_page import BATTLE_ORDER_CHECK
from tasks.base.page import page_battle_order
from tasks.base.ui import UI
from tasks.battle_order.assets.assets_battle_order_claim import *

from tasks.battle_order.draglist import CHARACTER_TAB_LIST
from tasks.base.character_keyword import CharacterTab
from tasks.battle_order.switch import BATTLE_ORDER_TAB


class BattleOrderClaim(UI):
    def handle_battle_order_claim(self):
        self.device.click_record_clear()
        self.ui_ensure(page_battle_order)
        BATTLE_ORDER_TAB.set('奖励',main=self)
        time=Timer(2,5).start()
        for _ in self.loop():
            if time.reached():
                break
            if self.appear(BATTLE_ORDER_CHARACTER_SELECT_CHECK,interval=0):
                self._character_fragments_select()
                continue
            if self.appear_then_click(BATTLE_ORDER_CLAIM_ALL,interval=0):
                continue
            if self.appear_then_click(BATTLE_ORDER_REWARD_CLAIM_SUCCESS,interval=0):
                continue
            res=self.detect_claimable_buttons(button=BATTLE_ORDER_REWARD_AREA,similarity=0.6)
            if res and len(res)!=0:
                if self.interval_is_reached('claimable_click', interval=1):
                    self.device.click(res[0])
                    self.interval_reset('claimable_click', interval=1)
                    time.reset()


    def _character_fragments_select(self):
        name=self.config.BattleOrder_CharacterFragments
        keyword=self.find_character_by_cn(name)
        CHARACTER_TAB_LIST.search_rows(main=self,keyword=keyword)
        for _ in self.loop():
            if BATTLE_ORDER_CHECK.match_color(self.device.image):
                break
            if self.appear_then_click(BATTLE_ORDER_REWARD_CLAIM_SUCCESS,interval=0):
                continue
            if self.appear_then_click(BATTLE_ORDER_CHARACTER_SELECT_CONFIRM):
                continue

# 通过中文名称查找对应的关键词对象
    def find_character_by_cn(self,chinese_name):
        for character in CharacterTab.instances.values():
            if character.cn == chinese_name:
                return character
        return None
