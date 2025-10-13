
from typing import Optional
from module.base.base import ModuleBase
import numpy as np
from module.base.button import ButtonWrapper
from module.base.decorator import cached_property
from module.base.timer import Timer
from module.exception import GameStuckError
from module.logger import logger
from module.ocr.keyword import Keyword
from module.ocr.ocr import OcrResultButton
from tasks.base.assets.assets_base_page import FULL_SCREEN
from tasks.organization.assets.assets_organization_fortress import FORTRESS_ENTER_CONFIRM
from tasks.organization.fortress.keywords import FortressNameKeyword
from tasks.organization.fortress.ocr import FortressOcr

class MapNavigation:

    def __init__(self,
                name,
                ocr_class,
                keyword_class,
                search_button: ButtonWrapper,    
        
                ):
        
        self.name=name
        self.ocr_class=ocr_class
        self.keyword_class=keyword_class
        self.search_button=search_button
        self.cur_buttons: list[OcrResultButton] = []
       
    def __str__(self):
        return f'MapNavigation({self.name})'

    __repr__ = __str__

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(self.name)
    @cached_property
    def ocr(self):
        return self.ocr_class(self.search_button)
    def keyword2button(self, target: Keyword, show_warning=True) -> Optional[OcrResultButton]:
        for button in self.cur_buttons:
            if button == target:
                return button

        if show_warning:
            logger.warning(f'Keyword {target} is not in current rows of {self}')
            logger.warning(f'Current rows: {self.cur_buttons}')
        return None
    def load_points(self, main: ModuleBase):
        """
        Parse current rows to get list position.
        """
        results= self.ocr.matched_ocr(main.device.image, self.keyword_class)
        scale_x = 1280 / 2560  # 0.5  
        scale_y = 720 / 1920   # 0.375  
        
        # 缩放每个结果的坐标  
        for result in results:  
            x1, y1, x2, y2 = result.button  
            result.button = (  
                int(x1 * scale_x),  
                int(y1 * scale_y),  
                int(x2 * scale_x),  
                int(y2 * scale_y)  
            )  
            # 同样需要缩放area和search属性  
            x1, y1, x2, y2 = result.area  
            result.area = (  
                int(x1 * scale_x),  
                int(y1 * scale_y),  
                int(x2 * scale_x),  
                int(y2 * scale_y)  
            )
       
        self.cur_buttons = results
    def calculate_direction(self, target:Keyword):
        target_pos=target.area_pos
        if not self.cur_buttons:  
            logger.warning('No fortresses detected on screen')  
            return (0, 0) 
        current_positions = [] 
        for button in self.cur_buttons:
            if button.matched_keyword:  
                current_positions.append(button.matched_keyword.area_pos)
        if not current_positions:  
            logger.warning('Cannot match detected fortresses to DIC_OS_MAP')  
            return (0, 0) 
        avg_x = sum(pos[0] for pos in current_positions) / len(current_positions)  
        avg_y = sum(pos[1] for pos in current_positions) / len(current_positions)  
        current_center = (avg_x, avg_y)      
        # 计算滑动向量  
        dx = target_pos[0] - current_center[0]  
        dy = target_pos[1] - current_center[1]
        logger.info(f'Current center: {current_center}, Target: {target_pos}, Vector: ({dx}, {dy})')  
        return (dx, dy)
    def drag_page(self, direction_vector, main: ModuleBase):  
        """  
        根据方向向量执行滑动  
        
        Args:  
            direction_vector: (dx, dy) 从 calculate_direction 返回的向量  
            main: ModuleBase 实例  
        """  
        dx, dy = direction_vector  
        
        # 计算距离  
        distance = np.sqrt(dx**2 + dy**2)  
        if distance < 50:  # 目标已在视口内  
            return  
        
        # 限制单次滑动距离  
        max_drag = 400  
        if distance > max_drag:  
            scale = max_drag / distance  
            dx *= scale  
            dy *= scale  
        
        # 注意:屏幕滑动方向与地图移动方向相反  
        # 要让地图向右移动(显示左边的内容),需要向左滑动屏幕  
        drag_vector = (-dx, -dy)  
        
        # 使用 random_rectangle_vector_opted 生成滑动起止点  
        from module.base.utils import random_rectangle_vector_opted  
        p1, p2 = random_rectangle_vector_opted(  
            drag_vector,  
            box=self.search_button.button,  
            padding=20  
        )  
        
        main.device.drag(p1, p2, name=f'{self.name}_DRAG_TO_TARGET')
    def is_point_selected(self, button: OcrResultButton, main: ModuleBase) -> bool:
        # Having gold letters
        if main.appear(FORTRESS_ENTER_CONFIRM):
            return True

        return False

    def select_point(self, target: Keyword, main: ModuleBase, insight=True, skip_first_screenshot=True):
        if insight:
            result = self.insight_point(
                target, main=main, skip_first_screenshot=skip_first_screenshot)
            if not result:
                return False
        logger.info(f'Select point: {target}')
        skip_first_screenshot = True
        interval = Timer(5)
        skip_first_load_points = True
        load_points_interval = Timer(1)
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                main.device.screenshot()

            if skip_first_load_points:
                skip_first_load_points = False
                load_points_interval.reset()
            else:
                if load_points_interval.reached():
                    self.load_points(main=main)
                    load_points_interval.reset()

            button = self.keyword2button(target)
            if not button:
                return False

            # End
            if self.is_point_selected(button, main=main):
                logger.info(f'point selected at {target}')
                return True

            # Click
            if interval.reached():
                print(f'origin button: {button.button}')
                button.button = (button.area[0]-50, button.area[1], button.area[2]-50, button.area[3])
                print(f'adjusted button: {button.button}')
                main.device.click(button)
                interval.reset()
        
    def insight_point(self, target: Keyword, main: ModuleBase, skip_first_screenshot=True) -> bool:
        """
        Args:
            point:
            main:
            skip_first_screenshot:

        Returns:
            If success
        """
        timeout = Timer(30, count=30).start()
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                main.device.screenshot()
            if timeout.reached():
                raise GameStuckError(f"{target.name} Navigation Stucked")
            self.load_points(main=main)
            button=self.keyword2button(target, show_warning=False)
            if button:
                break
            vector=self.calculate_direction(target)
            self.drag_page(direction_vector=vector, main=main)
            main.wait_until_stable(
                self.search_button, timer=Timer(0, count=0),
                timeout=Timer(1.5, count=5)
            )
            skip_first_screenshot = True

        return True
    def search_points(self, main, keyword):  
        if self.insight_point(keyword, main=main):  
            logger.info(f'Successfully navigated to {keyword.name} ')  
            if self.select_point(keyword, main=main):  
                logger.info(f'Successfully selected {keyword.name} ')  
                return True  
        return False  
    
   
    
FortressNavigation = MapNavigation(
    name='FortressNavigation',
    keyword_class=FortressNameKeyword,
    ocr_class=FortressOcr,
    search_button=FULL_SCREEN,
    )