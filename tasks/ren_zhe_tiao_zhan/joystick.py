import math
import cv2
import numpy as np
from functools import cached_property
from module.base.utils.utils import color_similarity_2d
from module.device.method.maatouch import MaatouchBuilder, retry as maatouch_retry
from module.device.method.minitouch import CommandBuilder, insert_swipe, random_normal_distribution, retry as minitouch_retry
from module.exception import ScriptError
from module.logger import logger
from tasks.base.assets.assets_base_move import JOYSTICK
from tasks.base.assets.assets_base_skill import CHARACTER_ATTACK, CHARACTER_PSYCHIC, CHARACTER_SECRET_SCROLL, CHARACTER_SKILL_1, CHARACTER_SKILL_2, CHARACTER_SKILL_3
from tasks.base.taskui import TaskUI
from tasks.combat.skill import SkillContact

class JoystickContact:

    CENTER = (JOYSTICK.area[0] + JOYSTICK.area[2]) / 2, (JOYSTICK.area[1] + JOYSTICK.area[3]) / 2
    RADIUS_RUN = (80, 100)

    def __init__(self, main):
        self.main = main
        self.prev_point = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.is_downed:
            self.up()
            logger.info('JoystickContact ends')

    @property
    def is_downed(self):
        return self.prev_point is not None

    @cached_property
    def builder(self):
        method = self.main.config.Emulator_ControlMethod
        if method == 'MaaTouch':
            _ = self.main.device.maatouch_builder
            builder = MaatouchBuilder(self.main.device, contact=1)
        elif method == 'minitouch':
            _ = self.main.device.minitouch_builder
            builder = CommandBuilder(self.main.device, contact=1)
        else:
            raise ScriptError(f'Control method {method} does not support multi-finger')
        builder.DEFAULT_DELAY = 0.
        return builder

    def with_retry(self, func):
        method = self.main.config.Emulator_ControlMethod
        if method == 'MaaTouch':
            retry = maatouch_retry
        elif method == 'minitouch':
            retry = minitouch_retry
        else:
            raise ScriptError(f'Control method {method} does not support multi-finger')
        return retry(func)(self)

    @classmethod
    def direction2screen(cls, direction, run=True):
        direction += random_normal_distribution(-5, 5, n=5)
        radius = cls.RADIUS_RUN
        radius = random_normal_distribution(*radius, n=5)
        direction = math.radians(direction)
        point = (
            cls.CENTER[0] + radius * math.sin(direction),
            cls.CENTER[1] - radius * math.cos(direction),
        )
        return (int(round(point[0])), int(round(point[1])))

    def up(self):
        if not self.is_downed:
            return
        logger.info('JoystickContact up')
        builder = self.builder
        def _up(_self):
            builder.up().commit()
            builder.send()
        self.with_retry(_up)
        self.prev_point = None

    def set(self, direction):
        point = self.direction2screen(direction)
        builder = self.builder
        if self.is_downed:
            points = insert_swipe(p0=self.prev_point, p3=point, speed=20)
            def _set(_self):
                for p in points[1:]:
                    builder.move(*p).commit().wait(10)
                builder.send()
            self.with_retry(_set)
        else:
            def _set(_self):
                builder.down(*point).commit()
                builder.send()
            self.with_retry(_set)
        self.prev_point = point


class GameControl(TaskUI):
    def __init__(self, config, device=None, task=None):
        super().__init__(config, device, task)
        self.SKILL_BUTTONS = {
            "ATTACK": CHARACTER_ATTACK,
            "SKILL1": CHARACTER_SKILL_1,
            "SKILL2": CHARACTER_SKILL_2,
            "SKILL3": CHARACTER_SKILL_3,
            "SECRECT_SCROLL":CHARACTER_SECRET_SCROLL,
            "PSYCHIC":CHARACTER_PSYCHIC
            
        }
        self.SKILL_COOLDOWN_REGIONS = {
            "SKILL1": CHARACTER_SKILL_1.area,
            "SKILL2": CHARACTER_SKILL_2.area,
            "SKILL3": CHARACTER_SKILL_3.area,
            "SECRECT_SCROLL":CHARACTER_SECRET_SCROLL.area,
            "PSYCHIC":CHARACTER_PSYCHIC.area
        }

        self.BRIGHTNESS_THRESHOLD = 100.0
        self.SATURATION_THRESHOLD = 100.0
        self._skill_contact=None
     

    @cached_property
    def joystick_center(self) -> tuple[int, int]:
        return JoystickContact.CENTER
    
    

    def is_skill_ready(self, skill_name):
        """
        通过固定的亮度和饱和度阈值判断技能是否可用
        """
        if skill_name not in self.SKILL_COOLDOWN_REGIONS or skill_name =='ATTACK':
            return True
        try:
            region = self.SKILL_COOLDOWN_REGIONS[skill_name]
            roi = self.image_crop(region, copy=False)
            hsv = cv2.cvtColor(roi, cv2.COLOR_RGB2HSV)
            brightness = np.mean(hsv[:, :, 2])
            saturation = np.mean(hsv[:, :, 1])
            return brightness > self.BRIGHTNESS_THRESHOLD and saturation > self.SATURATION_THRESHOLD
        except Exception as e:
            logger.warning(f"Skill check for '{skill_name}' failed: {e}")
            return True

    def is_skill_3_ready(self):
        roi = self.image_crop(CHARACTER_SKILL_3.area, copy=True)    
        height, width = roi.shape[:2]  
        center_x = width // 2  
        center_y = height // 2      
        outer_radius = min(width, height) // 2  # 图标的半径  
        inner_radius = outer_radius - 5  # 保留10像素的边框宽度  
        cv2.circle(roi, (center_x, center_y), inner_radius, (0, 0, 0), -1) 
        pos = color_similarity_2d(roi, color=(255, 255, 255))  
        _, binary = cv2.threshold(pos, 250, 255, cv2.THRESH_BINARY) 
        bright_count = cv2.countNonZero(binary)  
        logger.info(f"Skill check for : circular border GB=255 ratio={bright_count}")  
        return bright_count >50  # 阈值可能需要调整  

      
    

    def execute_skill(self,skill_name):
        
        if self.is_skill_ready(skill_name):
            button_pos = self.SKILL_BUTTONS[skill_name]
            if skill_name == 'SKILL2':
                self.device.long_click(button_pos, duration=5)
            else :
                self.device.click(button_pos)
            
            return True
        return False
    def move_to_direction(self, direction, duration=0.5):
        """
        向指定方向移动
        """
        with JoystickContact(self) as contact:
            contact.set(direction)
            self.device.sleep(duration)
            contact.up()
    def stop_movement(self):
        """
        停止移动
        """
        with JoystickContact(self) as contact:
            contact.up()
    def multi_long_press(self, buttons, duration=0):  
        with SkillContact(self) as contact:  
            contact.long_press(buttons, duration=duration)
    def press_down(self, buttons):
        if self._skill_contact is None:  
            self._skill_contact = SkillContact(self)  
            self._skill_contact.__enter__()
        self._skill_contact.press_down(buttons)
    def press_up(self, buttons):
        if self._skill_contact is None:  
            return
        self._skill_contact.press_up(buttons)
    def up_all(self):
        if self._skill_contact is None:  
            return
        self._skill_contact.up_all()

    def stop_long_press(self):
        with SkillContact(self) as contact:  
            contact.up_all()
    def is_skill_downed(self):
        return self._skill_contact.is_downed


