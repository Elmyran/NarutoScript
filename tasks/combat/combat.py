import time
from module.base.timer import Timer
from tasks.combat.skill import *
from tasks.duel.assets.assets_duel import DUEL_EXCEPTION, DUEL_FIGHT_END, DUEL_FIGHT_FAIL, DUEL_FIGHT_SUCCESS, DUEL_IS_IN_FIGHT, DUEL_ROUND_SWITCH
from tasks.ren_zhe_tiao_zhan.joystick import GameControl


class Combat(GameControl):
    
    
    def single_round_combat(self,
                      end_check=DUEL_FIGHT_END,
                      end_confirm=None,                      
                      skill=True,
                      scroll=True,
                      psychic=True,
                      timeout=120):
    
        try :
            self.device.stuck_timer=Timer(timeout).start()
            self._click_script(
                    end_check=end_check,
                    end_confirm=end_confirm,
                    skill=skill,
                    scroll=scroll,
                    psychic=psychic,
                    timeout=timeout
                   
                      )
        finally:
            self.up_all()
            self.device.stuck_timer=Timer(60,count=60).start()
        return True
    def multi_round_combat(self,
                      success_check=DUEL_FIGHT_SUCCESS,
                      fail_check=DUEL_FIGHT_FAIL,
                      round_check=DUEL_FIGHT_END,
                      skill=True,
                      scroll=True,
                      psychic=True,
                      timeout=400):
       
        logger.info('Starting multi-round combat')
     
        for _ in self.loop():
            self.device.stuck_record_clear()
            end=self._is_combat_end(success_check,fail_check)
            if end:
                logger.info('Combat end: '+end) 
                return True
            if self._is_round_start():
                self.single_round_combat(end_check=round_check, skill=skill, scroll=scroll, psychic=psychic, timeout=timeout)
                continue

    def _click_script(self,
                      end_check,
                      end_confirm,
                      skill,
                      scroll,
                      psychic,
                      timeout,
                      ):
        buttons=[CHARACTER_ATTACK,CHARACTER_TI_SHEN]
        if skill:
            buttons.extend([CHARACTER_SKILL_1, CHARACTER_SKILL_2, CHARACTER_SKILL_3])
       
        start_time = time.time()
        press_interval=Timer(3).start()
        secrect_scroll_interval=Timer(5).start()
        psychic_interval=Timer(5).start()
        self.press_down(buttons)
        for _ in self.loop():
            if time.time() - start_time > timeout or self.appear(end_check):
                logger.info("click_script end_check")
                self.up_all()
                break
            if end_confirm:
                if self.appear_then_click(end_confirm,interval=1):
                    logger.info("click_script end_cofirm")
                    break
            if self._is_exception():
                logger.info("click_script exception")
                break
            if press_interval.reached() :
                self.press_up(buttons)
                self.press_down(buttons)
                press_interval.reset()
            if psychic and psychic_interval.reached():
                if not self.is_skill_ready('PSYCHIC'):
                    if self.is_downed(CHARACTER_PSYCHIC):
                        self.press_up(CHARACTER_PSYCHIC)
                    psychic_interval.reset()
                    
                else :
                    self.press_down(CHARACTER_PSYCHIC)
            if scroll and secrect_scroll_interval.reached():
                if not self.is_skill_ready('SECRECT_SCROLL'):
                    if self.is_downed(CHARACTER_SECRET_SCROLL):
                        self.press_up(CHARACTER_SECRET_SCROLL)
                    secrect_scroll_interval.reset()
                    
                else:
                    self.press_down(CHARACTER_SECRET_SCROLL)
                    
            
    def _is_exception(self):
        if self.appear(DUEL_EXCEPTION):
            return True
        return False
    def _is_round_start(self):
        return self.appear(DUEL_ROUND_SWITCH)
    def _is_in_combat(self):
        return self.appear(DUEL_IS_IN_FIGHT) or self.appear(CHARACTER_ATTACK) or self.appear(DUEL_ROUND_SWITCH)
    def _is_combat_end(self,success_check=DUEL_FIGHT_SUCCESS,fail_check=DUEL_FIGHT_FAIL):
        if self.appear(success_check):
            return 'success'
        if self.appear(fail_check):
            return 'fail'
        if self._is_exception():
            return 'success'
        return False

    
        

            


            
