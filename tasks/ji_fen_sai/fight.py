from module.base.timer import Timer
from module.exception import RequestHumanTakeover
from module.logger import logger
from module.ocr.ocr import Digit,DigitCounter
from tasks.base.assets.assets_base_page import JI_FEN_SAI_CHECK
from tasks.base.taskui import TaskUI
from tasks.base.page import page_ji_fen_sai
from tasks.ji_fen_sai.assets.assets_ji_fen_sai import ENEMY_REFRESH, ENEMY_REFRESH_COUNT, ENEMY_REFRESH_SUCCESS, JI_FEN_SAI_FIGHT_COUNT, JI_FEN_SAI_FIGHT_END_CONFIRM, JI_FEN_SAI_FIGHT_PANEL_CHECK, JI_FEN_SAI_FIGHT_START_BUTTON, JI_FEN_SAI_GOTO_FIGHT_PANEL, JI_FEN_SAI_IS_IN_FIGHT, JI_FEN_SAI_SKIP_FIGHT_BUTTON, TEAM_POWER_SELF
from tasks.ji_fen_sai.assets.assets_ji_fen_sai_enemy import ENEMY_1, ENEMY_2, ENEMY_3, ENEMY_4, \
        ENEMY_1_POWER, ENEMY_2_POWER, ENEMY_3_POWER, ENEMY_4_POWER, \
        ENEMY_1_ORGANIZATION, ENEMY_2_ORGANIZATION, ENEMY_3_ORGANIZATION, ENEMY_4_ORGANIZATION, \
        ENEMY_1_SCORE, ENEMY_2_SCORE, ENEMY_3_SCORE, ENEMY_4_SCORE
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
            if self.refresh_popup_appear():
                continue
            enemy_list=self.enemy_recognition()
            enemy=self.enemy_filter(enemy_list)
            if not enemy:
                if not self.refresh_enemy():
                    break
                continue
            self.start_fight(enemy)
            self.skip_fight()
            self.back_to_ji_fen_sai()
            if self.config.JiFenSai_JiFenSaiOnlyFightOnce:
                logger.info(f'仅挑战一次')
                logger.info(f'正在退出')
                break
        return True
    def back_to_ji_fen_sai(self):
        logger.info(f'Back to Page')
        for _ in self.loop():
            if self.appear(JI_FEN_SAI_CHECK):
                break
            if self.appear_then_click(JI_FEN_SAI_FIGHT_END_CONFIRM,interval=2):
                continue
        return True
    def refresh_popup_appear(self):
        if self.appear(ENEMY_REFRESH_SUCCESS,similarity=0.5):
            return True
        return False
            
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
        logger.info(f'刷新')
        ocr=DigitCounter(ENEMY_REFRESH_COUNT)
        count,_,_=ocr.ocr_single_line(self.device.image)
        if count==0:
            return False 
        self.device.click_record_remove(ENEMY_REFRESH)
        self.ui_click(click_button=ENEMY_REFRESH,check_button=ENEMY_REFRESH_SUCCESS)
        return True

    def start_fight(self,enemy):
        logger.info(f'挑战:{enemy}')
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
        enemy_list=[]
        for area, power, organization, score in zip(
                (ENEMY_1, ENEMY_2, ENEMY_3, ENEMY_4),
                (ENEMY_1_POWER, ENEMY_2_POWER, ENEMY_3_POWER, ENEMY_4_POWER),
                (ENEMY_1_ORGANIZATION, ENEMY_2_ORGANIZATION, ENEMY_3_ORGANIZATION, ENEMY_4_ORGANIZATION),
                (ENEMY_1_SCORE, ENEMY_2_SCORE, ENEMY_3_SCORE, ENEMY_4_SCORE)   ):
            enemy=Enemy(area)
            enemy.recognition(self.device.image, power, organization, score)
            if enemy.button:
                enemy_list.append(enemy)
        return enemy_list
  
    def enter_panel(self):
        for _ in self.loop():
            if self.appear(ENEMY_REFRESH_SUCCESS):
                continue 
            if self.appear(JI_FEN_SAI_FIGHT_PANEL_CHECK):
                break
            if self.match_template_color(JI_FEN_SAI_GOTO_FIGHT_PANEL,interval=1):
                self.device.click(JI_FEN_SAI_GOTO_FIGHT_PANEL)
                continue
        self.device.click_record_remove(JI_FEN_SAI_GOTO_FIGHT_PANEL)
            

    def is_fight_count_enough(self):
        ocr=DigitCounter(JI_FEN_SAI_FIGHT_COUNT)
        times,_,_=ocr.ocr_single_line(self.device.image)
        if times>0:
            return True
        return False
if __name__ == '__main__':
    ns=JiFenSaiFight('ns',task='Alas')
    ns.device.screenshot()
    ns.enemy_recognition()
    