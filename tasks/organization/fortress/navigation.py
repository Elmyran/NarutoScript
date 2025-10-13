

from typing import Optional
from module.base.base import ModuleBase
import numpy as np

from module.base.button import ButtonWrapper
from module.base.decorator import cached_property
from module.base.timer import Timer
from module.base.utils.utils import color_similarity_2d, crop
from module.logger import logger
from module.ocr.keyword import Keyword
from module.ocr.ocr import OcrResultButton
from module.ocr.onnxocr.onnx_paddleocr import ONNXPaddleOcr
from tasks.base.assets.assets_base_page import FULL_SCREEN
from tasks.organization.fortress.keywords import FortressNameKeyword
from tasks.organization.fortress.ocr import FortressOcr
import cv2
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
    

    def insight_point(self, target: Keyword, main: ModuleBase, skip_first_screenshot=True) -> bool:
        """
        Args:
            row:
            main:
            skip_first_screenshot:

        Returns:
            If success
        """
       


        
        bottom_check = Timer(3, count=5).start()
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                main.device.screenshot()

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
    
   
    
FortressNavigation = MapNavigation(
    name='FortressNavigation',
    keyword_class=FortressNameKeyword,
    ocr_class=FortressOcr,
    search_button=FULL_SCREEN,
    )