from datetime import datetime,timedelta
from module.base.button import ClickButton
from module.base.timer import Timer
from module.base.utils.utils import  get_color
from module.config.utils import get_server_next_monday_update
from module.logger import logger
from module.ocr.ocr import DigitCounter
from tasks.combat.combat import Combat
from tasks.duel.assets.assets_duel_extended_play import *
from tasks.base.page import page_no_restricted_battle,page_daily,page_extended_play
from tasks.freebies.assets.assets_freebies_daily_daily import ACTIVITY_REWARD_GOTO_PLAY_SEARCH

class ExtendedPlay(Combat):
    def run(self):
        if self.config.stored.ExtendedCurrentScore.is_expired():
           self.config.stored.ExtendedCurrentScore.clear()
        if  self.config.stored.ExtendedCurrentScore.is_full():
            return get_server_next_monday_update(self.config.Scheduler_ServerUpdate)
        self.config.get_next_task()
        if len(self.config.pending_task)>1:
            return datetime.now()+timedelta(minutes=10)
        self.handle_extended_play()
        return get_server_next_monday_update(self.config.Scheduler_ServerUpdate)
    

    def enter_extended_play(self):
        self.ui_ensure(page_daily)
        click_interval=Timer(2)
        drag=True
        drag_interval=Timer(2)
        for _ in self.loop():
            if self.ui_page_appear(page_extended_play):
                break
            ACTIVITY_REWARD_GOTO_EXTENDED_PLAY.load_search(ACTIVITY_REWARD_GOTO_PLAY_SEARCH.area)
            if ACTIVITY_REWARD_GOTO_EXTENDED_PLAY.match_template(self.device.image):
                button_area=ACTIVITY_REWARD_GOTO_EXTENDED_PLAY.button
                button=ClickButton(area=(button_area[0],button_area[1]+110,button_area[2],button_area[3]+110))
                if click_interval.reached():
                    self.device.click(button)
                    click_interval.reset()
                drag=False
                continue
            if drag and drag_interval.reached():
                from module.base.utils import random_rectangle_vector_opted  
                p1, p2 = random_rectangle_vector_opted(  
                    0.5,  
                    box=ACTIVITY_REWARD_GOTO_PLAY_SEARCH.button,  
                    padding=20  
                )  
                self.device.drag(p1, p2, name=f'ACTIVITY_REWARD_DRAG_GOTO_EXTENDED_PLAY')
                continue 




       
    def handle_extended_play(self):
        self.enter_extended_play()
        ready_fight=False
        for _ in self.loop():
           if not ready_fight and self.is_task_finished():
               break
           else:
               ready_fight=True
            
           if ready_fight and self.no_restricted_battle_flow():
               ready_fight=False
    def is_task_finished(self):
        self.ui_ensure(page_no_restricted_battle)
        for _ in self.loop():
            if self.appear(EXTENDED_TASK_PANEL_CHECK):
                logger.info("Extended task panel entered")
                break
            if self.appear_then_click(EXTENDED_GOTO_TASK_PANEL,interval=1):
                continue
        if not self.score_reached():
            return False
        self.reward_claim()
        for _ in self.loop():
            if self.match_template_color(NO_RESTRICTED_BATTLE_CHECK):
                logger.info("Extended task panel exited")
                break
            if self.appear_then_click(EXTENDED_TASK_PANEL_EXIT_BUTTON,interval=1):
                continue
        return True
        
    def score_reached(self):
        logger.info("Checking score")
        counter=DigitCounter(EXTENDED_TASK_SCORE_AREA)
        current_score=0
        target_score=2100
        for _ in self.loop():
            score,reamin,total=counter.ocr_single_line(self.device.image)
            if total==2100:
                current_score=score
                break
        record=self.config.stored.ExtendedCurrentScore.value
        if current_score>record:
            self.config.stored.ExtendedCurrentScore.set(value=current_score)
        if current_score>=target_score:
            return True
        return False
    def reward_claim(self):
        return True

            

        
        
        

    def no_restricted_battle_flow(self):
        logger.info("no_restricted_battle_flow")
        self.ui_ensure(page_no_restricted_battle)
        self.start_fight()
        self.character_select()
        self.secrect_scroll_select()
        self.multi_round_combat()
        return True
    def start_fight(self):
        logger.info("start fight")
        for _ in self.loop():
            if self.appear(NO_RESTRICTED_CHARACTER_SELECT_CHECK):
                break
            if self.match_template_color(NO_RESTRICTED_START_FIGHT,interval=1):
                self.device.click(NO_RESTRICTED_START_FIGHT)
                continue
    def character_select(self):
        logger.info("Character select...")
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
        logger.info('Secrect scroll select...')
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




