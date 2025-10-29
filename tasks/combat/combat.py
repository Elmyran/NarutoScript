import time

from numpy import character
from module.base.button import match_template
from module.base.utils.utils import ensure_int, random_rectangle_point
from tasks.base.assets.assets_base_skill import CHARACTER_ATTACK, CHARACTER_SECRET_SCROLL, CHARACTER_SKILL_1, CHARACTER_SKILL_2, CHARACTER_SKILL_3, CHARACTER_TI_SHEN
from tasks.base.taskui import TaskUI
from tasks.duel.assets.assets_duel import DUEL_EXCEPTION, DUEL_IS_IN_FIGHT
from tasks.ren_zhe_tiao_zhan.joystick import GameControl


class Combat(GameControl):
    def no_restricted_battle_click(self,end_check, timeout=390):
        start_time = time.time()
        
        for _ in self.loop():
            self.device.click_record_clear()

            if time.time() - start_time > timeout:
                print(f"超时 {timeout} 秒，停止点击。")
                
                break
            if self.appear(end_check) or self.appear(DUEL_EXCEPTION):
                break
              
         
            self.device.multi_click(CHARACTER_SKILL_3,n=1,interval=0)
            self.device.multi_click(CHARACTER_SKILL_2,n=1,interval=0)
            self.device.multi_click(CHARACTER_SKILL_1,n=1,interval=0)
            self.device.multi_click(CHARACTER_ATTACK,n=1,interval=0)
            self.device.multi_click(CHARACTER_SECRET_SCROLL,n=1,interval=0)
            self.device.multi_click(CHARACTER_TI_SHEN,n=1,interval=0)
   
            


            
