from module.base.base import ModuleBase
from module.base.timer import Timer
from module.logger import logger
from module.ocr.keyword import Keyword
from module.ocr.ocr import Ocr
from module.ui.draggable_list import DraggableList
from tasks.activity.assets.assets_activity import ACTIVITY_LIST_AREA
from tasks.activity.assets.assets_activity_ui import MONTHLY_SIGN_IN_CHECK
from tasks.activity.keyword import ActivityTab

class DraggableActivityTabList(DraggableList):  
    # 类似DraggableDungeonList的特殊属性  
    target_activity = None  # 目标活动类型，用于过滤  
    limit_entrance = False  # 确保入口按钮可见  
      
    def wait_bottom_appear(self, main: ModuleBase, skip_first_screenshot=True):  
        """  
        当滑动到列表末尾时，等待列表反弹  
        """  
        logger.info('activity_list_wait_list_end')  
        timeout = Timer(1, count=3).start()  
        empty = False  
          
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
    
        row_index = self.keyword2index(row)  
        if not row_index:  
            logger.warning(f'Insight row {row} but index unknown')  
            return False  
  
        logger.info(f'Insight activity tab: {row}, index={row_index}')  
        last_buttons = None  
        bottom_check = Timer(3, count=5).start()  
          
        while True:  
            if skip_first_screenshot:  
                skip_first_screenshot = False  
            else:  
                main.device.screenshot()  
  
            self.load_rows(main=main)  
  
            # 检查是否找到目标  
            if self.cur_buttons and self.cur_min <= row_index <= self.cur_max:  
                return True  
  
            # 拖拽页面  
            if row_index < self.cur_min:  
                self.drag_page(self.reverse_direction(self.drag_direction), main=main)  
            elif self.cur_max < row_index:  
                self.drag_page(self.drag_direction, main=main)  
  
            # 等待底部出现
            self.wait_bottom_appear(main, skip_first_screenshot=False)  
            main.wait_until_stable(  
                self.search_button,   
                timer=Timer(0, count=0),  
                timeout=Timer(1.5, count=5)  
            )  
              
            skip_first_screenshot = True  
              
            # 检查是否到达列表末尾  
            if self.cur_buttons and last_buttons == set(self.cur_buttons):  
                if bottom_check.reached():  
                    logger.warning(f'No more rows in {self}, target {row} not found')  
                    return False  
            else:  
                bottom_check.reset()  
            last_buttons = set(self.cur_buttons)  
  
        return True  
  
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
    active_color=(212, 190, 143),  
    drag_direction="down"  
)