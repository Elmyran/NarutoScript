import time
from module.base.timer import Timer
from tasks.combat.skill import *
from tasks.duel.assets.assets_duel import DUEL_EXCEPTION, DUEL_FIGHT_END, DUEL_FIGHT_FAIL, DUEL_FIGHT_SUCCESS, DUEL_IS_IN_FIGHT, DUEL_ROUND_SWITCH
from tasks.ren_zhe_tiao_zhan.joystick import GameControl


class Combat(GameControl):
    
    
    def single_round_combat(self,
                      end_check=DUEL_FIGHT_END,
                      skill=True,
                      scroll=True,
                      psychic=True,
                      timeout=120):
        if not self.waiting_combat_start():
            return False
        try :
            self.device.stuck_timer=Timer(timeout).start()
            self._click_script(
                      end_check,
                      skill,
                      scroll,
                      psychic,
                      timeout
                      )
        finally:
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
       

     
        for _ in self.loop():
            end=self._is_combat_end(success_check,fail_check)
            if end:
                logger.info('Combat end: '+end) 
                return True
            if not self.single_round_combat(round_check, skill, scroll, psychic, timeout):
                continue
            logger.info('Round End')
            self.device.stuck_record_clear()
     



        
        
        
        
        
    
     
 

    def waiting_combat_start(self):
        log_interval=Timer(10)
        for _ in self.loop():
            if log_interval.reached():
                logger.info("Waiting for combat start...")
                log_interval.reset()
            if self._is_in_combat():
                break
            if self._is_combat_end():
                return False
        return True

    def _click_script(self,
                      end_check,
                      skill,
                      scroll,
                      psychic,
                      timeout,
                      ):
        buttons=[CHARACTER_ATTACK,CHARACTER_TI_SHEN]
        if skill:
            buttons.extend([CHARACTER_SKILL_1, CHARACTER_SKILL_2, CHARACTER_SKILL_3])
        if scroll:
            buttons.append(CHARACTER_SECRET_SCROLL)
        if psychic:
            buttons.append(CHARACTER_PSYCHIC)
        start_time = time.time()
        
        for _ in self.loop():

            if time.time() - start_time > timeout or self.appear(end_check):
                self.press_up(buttons)
                break
            if self._is_exception():
                self.press_up(buttons)
                break
            self.press_down(buttons)
    def _is_exception(self):
        if self.appear(DUEL_EXCEPTION):
            return True
        return False
    def _is_in_combat(self):
        return self.appear(DUEL_IS_IN_FIGHT) or self.appear(CHARACTER_ATTACK) 
    def _is_combat_end(self,success_check=DUEL_FIGHT_SUCCESS,fail_check=DUEL_FIGHT_FAIL):
        if self.appear(success_check):
            return 'success'
        if self.appear(fail_check):
            return 'fail'
        if self._is_exception():
            return 'success'
        return False

    
        

            


            
