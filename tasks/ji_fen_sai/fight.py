from module.base.timer import Timer
from module.exception import RequestHumanTakeover
from module.logger import logger
from module.ocr.ocr import Digit, DigitCounter
from tasks.base.assets.assets_base_page import JI_FEN_SAI_CHECK
from tasks.base.taskui import TaskUI
from tasks.base.page import page_ji_fen_sai
from tasks.ji_fen_sai.assets.assets_ji_fen_sai import ENEMY_1, ENEMY_2, ENEMY_3, ENEMY_4, ENEMY_REFRESH, ENEMY_REFRESH_COUNT, ENEMY_REFRESH_SUCCESS, JI_FEN_SAI_FIGHT_COUNT, JI_FEN_SAI_FIGHT_END_CONFIRM, JI_FEN_SAI_FIGHT_START_BUTTON, JI_FEN_SAI_GOTO_FIGHT_PANEL, JI_FEN_SAI_IS_IN_FIGHT, JI_FEN_SAI_SKIP_FIGHT_BUTTON, TEAM_POWER_SELF
from tasks.ji_fen_sai.enemy import Enemy
class JiFenSaiFight(TaskUI):
    def run(self):
        self.device.click_record_clear()
        self.device.stuck_record_clear()
        self.handle_fight()
    def handle_fight(self):
        self.ui_ensure(page_ji_fen_sai)
        for _ in self.loop():
            if self.ui_page_appear(page_ji_fen_sai):
                if not self.is_fight_count_enough():
                    break  
            self.enter_panel()
            enemy_list=self.enemy_recognition()
            enemy=self.enemy_filter(enemy_list)
            if not enemy:
                if not self.refresh_enemy():
                    break
                continue
            self.start_fight(enemy)
            self.skip_fight()
            self.back_to_ji_fen_sai()
        return True
    def back_to_ji_fen_sai(self):
        logger.info(f'Back to Page')
        for _ in self.loop():
            if self.appear(JI_FEN_SAI_CHECK):
                break
            if self.appear_then_click(JI_FEN_SAI_FIGHT_END_CONFIRM,interval=2):
                continue
        return True
    def skip_fight(self):
        if not self.config.JiFenSai_JiFenSaiSkipFight:
            return 
        for _ in self.loop():
            if self.appear(JI_FEN_SAI_FIGHT_END_CONFIRM):
                break
            if self.match_template_color(JI_FEN_SAI_SKIP_FIGHT_BUTTON,interval=2):
                self.device.click(JI_FEN_SAI_SKIP_FIGHT_BUTTON)
                continue
    def refresh_enemy(self):
        logger.info(f'Refresh enemy')
        ocr=DigitCounter(ENEMY_REFRESH_COUNT)
        count,_,_=ocr.ocr_single_line(self.device.image)
        if count==0:
            return False 
        for _ in self.loop():
            if self.appear(ENEMY_REFRESH_SUCCESS):
                break
            if self.appear_then_click(ENEMY_REFRESH,interval=2):
                continue
        return True

    def start_fight(self,enemy):
        logger.info(f'Start fight:{enemy}')
        click_interval=Timer(1,count=3).start()
        for _ in self.loop():
            if self.appear(JI_FEN_SAI_IS_IN_FIGHT):
                break
            if self.appear(JI_FEN_SAI_FIGHT_START_BUTTON):
                if click_interval.reached():
                    self.device.click(enemy)
                    click_interval.reset()
                    continue


    def enemy_filter(self,list):
        if not list:
            raise RequestHumanTakeover(f'No enemy found')
        ocr=Digit(TEAM_POWER_SELF)
        power_self=ocr.ocr_single_line(self.device.image)
        if self.config.JiFenSai_JiFenSaiFilter=='PowerLowest':
            return min(list, key=lambda enemy: enemy.power)  
        if self.config.JiFenSai_JiFenSaiFilter=='ScoreHighest':
            return list[0]
        if self.config.JiFenSai_JiFenSaiFilter=='PowerLowerThanSelfAndScoreHigher':
            for enemy in list:
                if enemy.power<power_self and enemy.score>0:
                    return enemy
        if self.config.JiFenSai_JiFenSaiFilter=='PowerLowerThanSelfAndScoreLower':
            enemy=min(list, key=lambda enemy: enemy.power)  
            if enemy.power<power_self:  
                return enemy
            else :
                return None 
        return list[-1]
    def enemy_recognition(self):
        enemy_area=[ENEMY_1,ENEMY_2,ENEMY_3,ENEMY_4]
        enemy_list=[]
        for area in enemy_area:
            enemy=Enemy(area)
            enemy.recognition(self.device.image)
            if enemy.button:
                enemy_list.append(enemy)
        return enemy_list
  
    def enter_panel(self):
        for _ in self.loop():
            if self.appear(ENEMY_REFRESH_SUCCESS):
                continue 
            if self.appear(ENEMY_REFRESH):
                break
            if self.appear_then_click(JI_FEN_SAI_GOTO_FIGHT_PANEL,interval=1):
                continue
            

    def is_fight_count_enough(self):
        
        ocr=DigitCounter(JI_FEN_SAI_FIGHT_COUNT)
        times,_,_=ocr.ocr_single_line(self.device.image)
        if times>0:
            return True
        return False
