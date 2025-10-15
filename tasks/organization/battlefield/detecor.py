import cv2  
import numpy as np

from module.base.decorator import cached_property
from module.base.utils.utils import color_similarity_2d, load_image  
  
class CharacterCircleDetector:  
   
    @cached_property
    def mask_interact(self):
        return load_image('./assets/share/organization/battlefield/BATTLE_FIELD_MASK.png')
    def detect_character_circle(self, image):  
        """  
        检测角色脚底的光圈  
          
        Args:  
            image: RGB 格式的游戏截图  

              
        Returns:  
            bool: 是否检测到角色脚底光圈  
              
        """  
        if self.mask_interact is not None:  
            image = cv2.bitwise_and(image, image, mask=self.mask_interact)  
        target_color = (110, 247, 253)  
        similarity = color_similarity_2d(image, color=target_color)  
        mask = cv2.inRange(similarity, 221, 255)  
        # 统计白色像素数量  
        white_pixels = cv2.countNonZero(mask)  
        
        if white_pixels > 200:  # 设置一个阈值  
            print(f"检测到蓝色光圈,匹配像素数: {white_pixels}")
            return True  