from module.base.decorator import cached_property
from module.device.method.maatouch import MaatouchBuilder
from module.exception import ScriptError
from module.logger import logger
from module.device.method.maatouch import MaatouchBuilder, retry as maatouch_retry
from module.device.method.minitouch import CommandBuilder, insert_swipe, random_normal_distribution, retry as minitouch_retry
from tasks.base.assets.assets_base_skill import CHARACTER_ATTACK, CHARACTER_PSYCHIC, CHARACTER_SECRET_SCROLL, CHARACTER_SKILL_1, CHARACTER_SKILL_2, CHARACTER_SKILL_3, CHARACTER_TI_SHEN
class SkillContact:    
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
    def builders(self):  

        method = self.main.config.Emulator_ControlMethod  
          
 
        if method == 'MaaTouch':  
            _ = self.main.device.maatouch_builder  
            builders_dict = {      
                CHARACTER_SKILL_1: MaatouchBuilder(self.main.device, contact=3),    
                CHARACTER_SKILL_2: MaatouchBuilder(self.main.device, contact=4),    
                CHARACTER_SKILL_3: MaatouchBuilder(self.main.device, contact=5),    
                CHARACTER_SECRET_SCROLL: MaatouchBuilder(self.main.device, contact=6),    
                CHARACTER_PSYCHIC: MaatouchBuilder(self.main.device, contact=7),    
                CHARACTER_ATTACK: MaatouchBuilder(self.main.device, contact=8),    
                CHARACTER_TI_SHEN: MaatouchBuilder(self.main.device, contact=9)    
            }  
        elif method == 'minitouch':  
            _ = self.main.device.minitouch_builder  
            builders_dict = {      
                CHARACTER_SKILL_1: CommandBuilder(self.main.device, contact=3),    
                CHARACTER_SKILL_2: CommandBuilder(self.main.device, contact=4),    
                CHARACTER_SKILL_3: CommandBuilder(self.main.device, contact=5),    
                CHARACTER_SECRET_SCROLL: CommandBuilder(self.main.device, contact=6),    
                CHARACTER_PSYCHIC: CommandBuilder(self.main.device, contact=7),    
                CHARACTER_ATTACK: CommandBuilder(self.main.device, contact=8),    
                CHARACTER_TI_SHEN: CommandBuilder(self.main.device, contact=9)    
            }  
        else:  
            raise ScriptError(f'Control method {method} does not support multi-finger')  
          
        # 设置零延迟  
        for builder in builders_dict.values():      
            builder.DEFAULT_DELAY = 0  
              
        return builders_dict
    @property  
    def is_downed(self):  
        """检查是否有任何技能处于按下状态"""  
        return len(self._downed_skills) > 0  
    def long_press(self, buttons,duration):
        builders=self.builders
        def _long_press(_self):
            for button in buttons:  
                builder = builders.get(button)
                if not builder:  
                    continue
                x, y = button.button[:2] 
                builder.down(x, y).commit()  
                builder.send()  
                self._downed_skills.add(button)  
            if duration>0:  
                self.main.device.sleep(duration )
                for button in buttons:  
                    builder = builders.get(button)
                    if not builder:  
                        continue
                    builder.up().commit()   
                    builder.send()  
                    self._downed_skills.discard(button)    
        self.with_retry(_long_press)
    def press_down(self, buttons):
        builders=self.builders
        for button in buttons:  
                builder = builders.get(button)
                if not builder:  
                    continue
                x, y = button.button[:2] 
                builder.down(x, y).commit()  
                builder.send()  
    def press_up(self, buttons):
        builders=self.builders
        for button in buttons:  
                builder = builders.get(button)
                if not builder:  
                    continue
                builder.up() 
                builder.commit()
                builder.send()

        
    def up_all(self):  
        builders=self.builders
        """抬起所有按下的技能"""  
        for skill_name in list(self._downed_skills):  
            builder = builders[skill_name]  
            builder.up().commit()  
            builder.send()  
        self._downed_skills.clear()  
      
    def with_retry(self, func):  
        method = self.main.config.Emulator_ControlMethod 
        if method == 'MaaTouch':  
            retry = maatouch_retry  
        elif method == 'minitouch':  
            retry = minitouch_retry  
        else:  
            raise ScriptError(f'Control method {method} does not support multi-finger')  
        return retry(func)(self)