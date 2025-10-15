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
    def show_detection(self,image,  show_window=True):  
        """可视化检测结果"""  
        target_color = (110, 247, 253)  
        # 方案 1: G 通道过滤 + 颜色相似度  
        mask = cv2.inRange(image, target_color, target_color)  
        white_pixels = cv2.countNonZero(mask)  
        logger.info(f'White pixels count: {white_pixels}')
        
        # 可视化调试  
        debug_image = image.copy()  
        debug_image[mask > 0] = (0, 255, 0)  
        cv2.imshow('G-filtered result', cv2.cvtColor(debug_image, cv2.COLOR_RGB2BGR))  
        cv2.waitKey(0)  
        cv2.destroyAllWindows()
        if white_pixels > 100:  # 调整阈值  
            return True
        return False
        
