from module.logger import logger
from module.ocr.ocr import Ocr
from module.ui.draggable_list import DraggableList

from tasks.activity.assets.assets_activity_ui import MONTHLY_SIGN_IN_CHECK

from tasks.base.character_keyword import CharacterTab, OcrCharacterTab
from tasks.battle_order.assets.assets_battle_order_claim import BATTLE_ORDER_CHARACTER_LIST_AREA, \
    BATTLE_ORDER_CHECK_STATUS


class DraggableCharacterTabList(DraggableList):
    def is_row_selected(self, button, main):
        """检测标签页是否被选中且页面已加载"""
        # 检查页面是否已加载（这是最重要的判断条件）
        check_box_area = (
            button.area[2] + 50,   # 选中框左边界 (名字右边+70)
            button.area[1] - 10,   # 选中框上边界 (名字上边-10)
            button.area[2] + 118,  # 选中框右边界 (名字右边+118)
            button.area[3]  +10    # 选中框下边界 (名字下边+8)
        )
        print(check_box_area)
        BATTLE_ORDER_CHECK_STATUS.load_search(check_box_area)
        if main.appear(BATTLE_ORDER_CHECK_STATUS):
            return True
        return False

    def load_rows(self, main):
        """重写 load_rows 方法以适应活动界面"""
        super().load_rows(main=main)
        logger.info(f'Loaded {len(self.cur_buttons)} character tabs')
        for i, button in enumerate(self.cur_buttons):
            logger.info(f'Tab {i}: {button.matched_keyword}')
    def search_rows(self, main,keyword):
        if CHARACTER_TAB_LIST.insight_row(keyword, main=main):
            logger.info('Successfully navigated to'+keyword.cn)
            if CHARACTER_TAB_LIST.select_row(keyword, main=main):
                logger.info('Successfully selected '+keyword.cn)

        # 创建活动标签页列表实例
CHARACTER_TAB_LIST = DraggableCharacterTabList(
    name='CharacterTabList',
    keyword_class=CharacterTab,
    ocr_class=OcrCharacterTab,
    search_button=BATTLE_ORDER_CHARACTER_LIST_AREA,
    check_row_order=False,
    active_color=(247, 255, 173),
    drag_direction="down"
)