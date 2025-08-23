import math
import cv2
import numpy as np
from functools import cached_property

from module.device.method.maatouch import MaatouchBuilder, retry as maatouch_retry
from module.device.method.minitouch import CommandBuilder, insert_swipe, random_normal_distribution, retry as minitouch_retry
from module.exception import ScriptError
from module.logger import logger
from tasks.base.assets.assets_base_move import JOYSTICK
from tasks.base.assets.assets_base_skill import CHARACTER_ATTACK, CHARACTER_SKILL_1, CHARACTER_SKILL_2
from tasks.base.ui import UI

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


class GameControl(UI):
    def __init__(self, config, device=None, task=None):
        super().__init__(config, device, task)
        self.SKILL_BUTTONS = {
            "ATTACK": CHARACTER_ATTACK,
            "SKILL1": CHARACTER_SKILL_1,
            "SKILL2": CHARACTER_SKILL_2,
        }
        self.SKILL_COOLDOWN_REGIONS = {
            "SKILL1": CHARACTER_SKILL_1.area,
            "SKILL2": CHARACTER_SKILL_2.area,
        }

        self.BRIGHTNESS_THRESHOLD = 100.0
        self.SATURATION_THRESHOLD = 100.0

    @cached_property
    def joystick_center(self) -> tuple[int, int]:
        return JoystickContact.CENTER

    def is_skill_ready(self, skill_name):
        """
        通过固定的亮度和饱和度阈值判断技能是否可用
        """
        if skill_name not in self.SKILL_COOLDOWN_REGIONS:
            return True
        try:
            region = self.SKILL_COOLDOWN_REGIONS[skill_name]
            roi = self.image_crop(region, copy=False)
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            brightness = np.mean(hsv[:, :, 2])
            saturation = np.mean(hsv[:, :, 1])
            return brightness > self.BRIGHTNESS_THRESHOLD and saturation > self.SATURATION_THRESHOLD
        except Exception as e:
            logger.warning(f"Skill check for '{skill_name}' failed: {e}")
            return True

    def execute_attack(self):
        button_pos = self.SKILL_BUTTONS["ATTACK"]
        self.device.click(button_pos)
        logger.info("执行普通攻击")
        return True

    def execute_skill1(self):
        if self.is_skill_ready("SKILL1"):
            button_pos = self.SKILL_BUTTONS["SKILL1"]
            self.device.click(button_pos)
            logger.info("执行一技能")
            return True
        return False

    def execute_skill2(self):
        if self.is_skill_ready("SKILL2"):
            button_pos = self.SKILL_BUTTONS["SKILL2"]
            self.device.click(button_pos)
            logger.info("执行二技能")
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