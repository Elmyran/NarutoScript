from module.base.utils.utils import color_similarity_2d, get_color
from module.logger import logger
from tasks.base.assets.assets_base_skill import CHARACTER_SKILL_3
from tasks.combat.combat import Combat
from tasks.duel.assets.assets_duel import DUEL_FIGHT_END, DUEL_FIGHT_FAIL, DUEL_FIGHT_SUCCESS, DUEL_ROUND_SWITCH
from tasks.duel.assets.assets_duel_extended_play import *
from tasks.base.page import page_no_restricted_battle


class ExtendedPlay(Combat):
    def run(self):
       self.handle_extended_play()
       
    def handle_extended_play(self):
        self.ui_ensure(page_no_restricted_battle)
        self.start_fight()
        self.character_select()
        self.secrect_scroll_select()
        for _ in self.loop():
            if self.appear(DUEL_FIGHT_SUCCESS) or self.appear(DUEL_FIGHT_FAIL):
                break
            if self.appear(DUEL_ROUND_SWITCH):
                self.no_restricted_battle_click(end_check=DUEL_FIGHT_END)

    def start_fight(self):
        for _ in self.loop():
            if self.appear(NO_RESTRICTED_CHARACTER_SELECT_CHECK):
                break
            if self.match_template_color(NO_RESTRICTED_START_FIGHT,interval=1):
                self.device.click(NO_RESTRICTED_START_FIGHT)
                continue
    def character_select(self):
        for _ in self.loop():
            if self.appear(AWAITING_SELF_SECRECT_SCROLL_SELECT):
                break
            if self.appear(AWAITING_OPPONENT_SELECT):
                continue
            if self.appear(AWAITING_SELF_SELECT):
                skip_first_screenshot = True
                for character in EXTENDED_SELECT_CHARACTER.buttons:
                    if skip_first_screenshot:
                        skip_first_screenshot = False
                    else :
                        self.device.screenshot()
                    
                    if self.is_character_selected(character):
                        continue
                    if self.single_character_select(character):
                        break
                   
                    
    def single_character_select(self,button):
        for _ in self.loop():
            if self.appear(AWAITING_SELF_SECRECT_SCROLL_SELECT):
                break
            if self.appear(AWAITING_OPPONENT_SELECT):
                return False
            if self.is_character_selected(button):
                return False
            if EXTENDED_CHARACTER_SELECTED.match_template(self.device.image,direct_match=True,similarity=0.6):
                if self.appear_then_click(NO_RESTRICTED_CHARACTER_SELECT_CONFIRM,interval=1):
                    self.device.click_record_remove(NO_RESTRICTED_CHARACTER_SELECT_CONFIRM)
                continue    
            
            if self.match_template_color(AWAITING_SELF_SELECT,interval=1):
                self.device.click(button)
                self.device.click_record_remove(button)
                continue
        return True
    def secrect_scroll_select(self):
        for _ in self.loop():
            if self.appear(AWATING_FIGHT_START):
                break
            if self.appear(AWAITING_OPPONENT_SELECT):
                continue
            if self.appear(AWAITING_SELF_SECRECT_SCROLL_SELECT):
                skip_first_screenshot=True
                for scroll in EXTENDED_SELECT_SECRECT_SCROLL_GRID.buttons:
                    if skip_first_screenshot:
                        skip_first_screenshot = False
                    else :
                        self.device.screenshot()
                    SECRECT_SCROLL_IS_SELECTED_OR_BANED.load_search(scroll.search)
                    if self.appear(SECRECT_SCROLL_IS_SELECTED_OR_BANED):
                        continue
                    if self.single_secrect_scroll_select(scroll):
                        break
    def single_secrect_scroll_select(self,button):
        for _ in self.loop():
            if self.appear(AWATING_FIGHT_START):
                break
            if self.appear(AWAITING_OPPONENT_SELECT):
                return False
            SECRECT_SCROLL_IS_SELECTED_OR_BANED.load_search(button.search)
            if self.appear(SECRECT_SCROLL_IS_SELECTED_OR_BANED):
                return False
            if EXTENDED_CHARACTER_SELECTED.match_template(self.device.image,direct_match=True,similarity=0.6):
                if self.appear_then_click(NO_RESTRICTED_CHARACTER_SELECT_CONFIRM,interval=1):
                    self.device.click_record_remove(NO_RESTRICTED_CHARACTER_SELECT_CONFIRM)
                continue
            
            if self.match_template_color(AWAITING_SELF_SECRECT_SCROLL_SELECT,interval=1):
                self.device.click(button)
                self.device.click_record_remove(button)
                continue
        return True

            
    def is_character_selected(self,button):
        # 获取区域的平均颜色  
        area=(button.area[0]+5, button.area[1]+5, button.area[2]-40, button.area[3]-40)
        color = get_color(self.device.image, area)  
        r, g, b = color  
        threshold = 1
        
        if abs(r - g) < threshold and abs(g - b) < threshold and abs(r - b) < threshold:  
            logger.info(f"区域已选中:{button.posi}")
            return True  
        return False
    def test(self):
        self.no_restricted_battle_click(end_check=AWAITING_SELF_SECRECT_SCROLL_SELECT)
       

az=ExtendedPlay('ns',task='Alas')
az.device.screenshot()
az.no_restricted_battle_click(end_check=DUEL_FIGHT_END)
