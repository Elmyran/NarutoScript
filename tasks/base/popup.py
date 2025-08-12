from typing import Callable

from module.base.base import ModuleBase
from module.base.utils import color_similarity_2d
from module.logger import logger

from tasks.base.assets.assets_base_popup import *
import cv2
import numpy as np

class PopupHandler(ModuleBase):
    def handle_exit(self,interval=2):
        if self.appear_then_click(EXIT_CONFIRM,interval=interval):
            return True
        if self.appear_then_click(EXIT_ORGANIZATION_RED_ENVELOPE,interval=interval):
            return True
        return False

    def reward_appear(self) -> bool:
        buttons = GET_REWARD.data_buttons['share']
        for button in buttons:
            print(button)

            image = self.image_crop(button.search, copy=False)
            image = color_similarity_2d(image, color=(203, 181, 132))

            # 确保输入图像格式正确
            if len(image.shape) == 3:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image = image.astype(np.uint8)

            # 确保模板图像也是正确格式
            template = button.image
            if len(template.shape) == 3:
                template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            template = template.astype(np.uint8)

            # 直接进行模板匹配，绕过button.match_template()
            res = cv2.matchTemplate(template, image, cv2.TM_CCOEFF_NORMED)
            _, sim, _, point = cv2.minMaxLoc(res)

            if sim > 0.85:
                button._button_offset = np.array(point) + button.search[:2] - button.area[:2]
                return True
        return False
    def handle_reward(self, interval=5, click_button: ButtonWrapper = None) -> bool:
            """
            Args:
                interval:
                click_button: Set a button to click

            Returns:
                If handled.
            """
        # Same as ModuleBase.match_template()
            self.device.stuck_record_add(GET_REWARD)

            if interval and not self.interval_is_reached(GET_REWARD, interval=interval):
                return False

            appear = self.reward_appear()

            if click_button is None:
                if appear:
                    self.device.click(GET_REWARD)
            else:
                if appear:
                    logger.info(f'{GET_REWARD} -> {click_button}')
                    self.device.click(click_button)

            if appear and interval:
                self.interval_reset(GET_REWARD, interval=interval)

            return appear
    # def handle_ui_close(self, appear_button: ButtonWrapper | Callable, interval=2) -> bool:
    #     """
    #     Args:
    #         appear_button: Click if button appears
    #         interval:
    #
    #     Returns:
    #         If handled.
    #     """
    #     if callable(appear_button):
    #         if self.interval_is_reached(appear_button, interval=interval) and appear_button():
    #             logger.info(f'{appear_button.__name__} -> {CLOSE}')
    #             self.device.click(CLOSE)
    #             self.interval_reset(appear_button, interval=interval)
    #             return True
    #     else:
    #         if self.appear(appear_button, interval=interval):
    #             logger.info(f'{appear_button} -> {CLOSE}')
    #             self.device.click(CLOSE)
    #             return True
    #
    #     return False
    #
    # def handle_ui_back(self, appear_button: ButtonWrapper | Callable, interval=2) -> bool:
    #     """
    #     Args:
    #         appear_button: Click if button appears
    #         interval:
    #
    #     Returns:
    #         If handled.
    #     """
    #     if callable(appear_button):
    #         if self.interval_is_reached(appear_button, interval=interval) and appear_button():
    #             logger.info(f'{appear_button.__name__} -> {BACK}')
    #             self.device.click(BACK)
    #             self.interval_reset(appear_button, interval=interval)
    #             return True
    #     else:
    #         if self.appear(appear_button, interval=interval):
    #             logger.info(f'{appear_button} -> {BACK}')
    #             self.device.click(BACK)
    #             return True
    #
    #     return False
