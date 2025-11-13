from module.base.decorator import cached_property
from module.device.method.maatouch import MaatouchBuilder
from module.exception import ScriptError
from module.logger import logger
from module.device.method.maatouch import MaatouchBuilder, retry as maatouch_retry
from module.device.method.minitouch import CommandBuilder, insert_swipe, random_normal_distribution, retry as minitouch_retry
from tasks.base.assets.assets_base_skill import CHARACTER_ATTACK, CHARACTER_PSYCHIC, CHARACTER_SECRET_SCROLL, CHARACTER_SKILL_1, CHARACTER_SKILL_2, CHARACTER_SKILL_3, CHARACTER_TI_SHEN
class SkillContact:   
    SKILL_CONTACTS = {  
        CHARACTER_SKILL_1: 3,  
        CHARACTER_SKILL_2: 4,  
        CHARACTER_SKILL_3: 5,  
        CHARACTER_SECRET_SCROLL: 6,  
        CHARACTER_PSYCHIC: 7,  
        CHARACTER_ATTACK: 8,  
        CHARACTER_TI_SHEN: 9  
    }  
    def __init__(self, main):
        
            
    
        self.main = main           
        # 跟踪哪些技能当前处于按下状态  
        self._downed_skills = set()  
                
    def __enter__(self):  
        return self  
  
    def __exit__(self,exc_type, exc_val, exc_tb):  
        # 清理所有按下的触控点  
        if self.is_downed:  
            self.up_all()  
            logger.info('SkillContact ends')  
    @cached_property  
    def builder(self):  

        method = self.main.config.Emulator_ControlMethod  
          
 
        if method == 'MaaTouch':  
            _ = self.main.device.maatouch_builder  
            builder = MaatouchBuilder(self.main.device, contact=3)  
        elif method == 'minitouch':  
            _ = self.main.device.minitouch_builder  
            builder = MaatouchBuilder(self.main.device, contact=3)    
        else:  
            raise ScriptError(f'Control method {method} does not support multi-finger')  
          
        # 设置零延迟  
        
        builder.DEFAULT_DELAY = 0  
              
        return builder
    @property  
    def is_downed(self):  
        """检查是否有任何技能处于按下状态"""  
        return len(self._downed_skills) > 0  
    def long_press(self, buttons,duration):
        builder=self.builder
        def _long_press(_self):
            for button in buttons:  
                contact_id = self.SKILL_CONTACTS.get(button)  
                if not contact_id:  
                    continue  
                x, y = button.button[:2]   
                builder.contact = contact_id  
                builder.down(x, y).commit()  
                self._downed_skills.add(button)   
            if duration>0:  
                self.main.device.sleep(duration )
                for button in buttons:  
                    contact_id = self.SKILL_CONTACTS.get(button)  
                    if not contact_id:  
                        continue  
                    x, y = button.button[:2]   
                    builder.contact = contact_id  
                    builder.up().commit()
                    self._downed_skills.discard(button)     
        self.with_retry(_long_press)
    def press_down(self, buttons):  
        def _press_down(_self):  
            builder = self.builder  
            nonlocal buttons  
            if not isinstance(buttons, list):  
                buttons = [buttons]  
            for button in buttons:  
                contact_id = self.SKILL_CONTACTS.get(button)  
                if not contact_id:  
                    continue  
                x, y = button.button[:2]   
                builder.contact = contact_id  
                builder.down(x, y).commit()  
                self._downed_skills.add(button)  
            
            
            builder.send()  
        
        self.with_retry(_press_down)
    def press_up(self, buttons):
        def _press_up(_self):
            builder = self.builder  
            nonlocal buttons  
            if not isinstance(buttons, list):  
                buttons = [buttons]  
            for button in buttons:  
                contact_id = self.SKILL_CONTACTS.get(button)  
                if not contact_id:  
                    continue  
                x, y = button.button[:2]   
                builder.contact = contact_id  
                builder.up().commit()
                self._downed_skills.discard(button) 
        self.with_retry(_press_up)
        

        
    def up_all(self):  
        """抬起所有按下的技能"""  
        def _up_all(_self):  
            builder = self.builder  
            for skill_name in list(self._downed_skills):  
                contact_id = self.SKILL_CONTACTS[skill_name]  
                builder.contact = contact_id  
                builder.up().commit()  
            builder.send()  
            self._downed_skills.clear()    
        self.with_retry(_up_all)
       
      
    def with_retry(self, func):  
        method = self.main.config.Emulator_ControlMethod 
        if method == 'MaaTouch':  
            retry = maatouch_retry  
        elif method == 'minitouch':  
            retry = minitouch_retry  
        else:  
            raise ScriptError(f'Control method {method} does not support multi-finger')  
        return retry(func)(self)