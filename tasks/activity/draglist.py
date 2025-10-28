from module.base.base import ModuleBase
from module.base.timer import Timer
from module.logger import logger
from module.ocr.keyword import Keyword
from module.ocr.ocr import Ocr
from module.ui.draggable_list import DraggableList
from tasks.activity.assets.assets_activity import ACTIVITY_LIST_AREA
from tasks.activity.activity_keyword import ActivityTab

class DraggableActivityTabList(DraggableList):   
    target_activity = None  # 目标活动类型，用于过滤  
    limit_entrance = False  # 确保入口按钮可见  
      
    def wait_bottom_appear(self, main: ModuleBase, skip_first_screenshot=True):  
        """  
        当滑动到列表末尾时，等待列表反弹  
        """  
        logger.info('activity_list_wait_list_end')  
        timeout = Timer(1, count=3).start()  
          
        while True:  
            if skip_first_screenshot:  
                skip_first_screenshot = False  
            else:  
                main.device.screenshot()  
              
            # 超时检查  
            if timeout.reached():  
                logger.warning('Wait activity_list_wait_list_end timeout')  
                return True  
                  
 
            # 暂时返回False，表示没有特殊的底部检测  
            return False  
  
    def load_rows(self, main: ModuleBase):  
        
        # 调用父类方法  
        super().load_rows(main=main)  
          
        logger.info(f'Loaded {len(self.cur_buttons)} activity tabs')  
        for i, button in enumerate(self.cur_buttons):  
            logger.info(f'Tab {i}: {button.matched_keyword}')  
      
    def insight_row(self, row: Keyword, main: ModuleBase, skip_first_screenshot=True) -> bool:  
        logger.info(f'Insight activity tab : {row}')  
      
        for _ in range(3):  # 最多重试3次  
            visited = set()  
            end_count = 0  
            
            while True:  
                visited_count = len(visited) 
               
                self.load_rows(main=main)  
                
                # 检查是否找到目标  
                for button in self.cur_buttons:  
                    if button.matched_keyword == row:  
                        logger.info(f'Found activity tab {row}')  
                        return True  
                
                # 检查是否到达末尾  
                for button in self.cur_buttons:  
                    if button.matched_keyword:  
                        visited.add(button.matched_keyword.name)  
                
                if len(visited) <= visited_count:  
                    end_count += 1  
                    if end_count >= 3:  
                        logger.error('Activity list reached end but target not found')  
                        break  
                else:  
                    end_count = 0  
                
                # 继续滚动  
                self.drag_page(self.drag_direction, main=main)  
                self.wait_bottom_appear(main, skip_first_screenshot=False)  
                main.wait_until_stable(  
                    self.search_button,  
                    timer=Timer(0, count=0),  
                    timeout=Timer(1.5, count=5)  
                )  
        
        return False
    def is_row_selected(self, button, main):
        if main.image_color_count(button, color=self.active_color, threshold=240, count=100):
            return True

        return False
  
    def search_rows(self, main, keyword):  
        """搜索并选择指定的活动标签"""  
        if self.insight_row(keyword, main=main):  
            logger.info(f'Successfully navigated to {keyword.name} area')  
            if self.select_row(keyword, main=main):  
                logger.info(f'Successfully selected {keyword.name} tab')  
                return True  
        return False  
   
  
# 创建活动标签页列表实例  
ACTIVITY_TAB_LIST = DraggableActivityTabList(  
    name='ActivityTabList',  
    keyword_class=ActivityTab,  
    ocr_class=Ocr,  
    search_button=ACTIVITY_LIST_AREA,  
    check_row_order=False,  
    active_color=(221, 199, 161),  
    drag_direction="down"  
)