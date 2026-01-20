from module.logger import logger
import cv2  
class CharacterCircleDetector:  
   
    
    def detect_character_circle(self, image):  
        """  
        检测角色脚底的光圈  
          
        Args:  
            image: RGB 格式的游戏截图  

              
        Returns:  
            bool: 是否检测到角色脚底光圈  
              
        """  
       
        target_color = (110, 247, 253)  
        mask = cv2.inRange(image, target_color, target_color)
        white_pixels = cv2.countNonZero(mask)  
        if white_pixels > 100:  # 调整阈值  
            return True  
        return False
    def image_process(self,image):
 
        #(15, 500) (70, 555)  
        image[500:555, 15:70, :] = 0  
        
        #(0, 560)  (380, 720)  
        image[560:720, 0:380, :] = 0  
        
        #(1100, 634)  (1260, 680)  
        image[634:680, 1100:1260, :] = 0  
        
        #(1150, 80)  (1250, 590)  
        image[80:590, 1150:1250, :] = 0  
        
        return image


        
    
        
