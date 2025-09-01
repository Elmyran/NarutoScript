from module.base.base import ModuleBase
from module.base.button import ButtonWrapper
from module.base.timer import Timer
from module.logger import logger
from module.ocr.keyword import Keyword
from module.ocr.ocr import OcrResultButton

from module.ocr.ocrutils import OCR
from module.ui.draggable_list import DraggableList
from tasks.base.assets.assets_base_page import MAIN_GOTO_TASK_SEARCH_AREA, JI_FEN_SAI_CHECK, REN_ZHE_TIAO_ZHAN_CHECK
from tasks.base.task_tab.keyword import TaskTab
from tasks.base.task_tab.ocr import TaskTabOcr, TaskOcr
from tasks.duel.assets.assets_duel import DUEL_CHECK
from tasks.fengrao.assets.assets_fengrao import FENG_RAO_CHECK
from tasks.leaderboard.assets.assets_leaderboard import LEADER_BOARD_CHECK
from tasks.mission.assets.assets_mission import MISSION_CHECK
from tasks.organization.assets.assets_organization_pray import  ORGANIZATION_PANEL
from tasks.squadraid.assets.assets_squadraid_fight import SQUAD_RAID_CHECK
from tasks.trail.assets.assets_trail import TRAIL_SURVIVAL_CHECK


class DraggableTaskTabList(DraggableList):

    def __init__(self, name, keyword_class, custom_ocr: OCR, search_button: ButtonWrapper, **kwargs):
        # 创建适配器OCR类
        ocr_adapter = lambda button: TaskTabOcr(button, custom_ocr)
        self.drag_vector = (0.7,0.9)
        super().__init__(name, keyword_class, ocr_adapter, search_button, **kwargs)
    def load_rows(self, main: ModuleBase):
        """重写load_rows以支持竖向文字识别"""
        # 使用自定义OCR进行文字识别
        self.cur_buttons = self.ocr.matched_ocr(main.device.image, self.keyword_class)
        print(self.cur_buttons)
        # 对于竖向文字，可能需要调整索引计算逻辑
        indexes = [self.keyword2index(row.matched_keyword) for row in self.cur_buttons]
        indexes = [index for index in indexes if index]

        if not indexes:
            logger.warning(f'No valid rows loaded into {self}')
            return

        self.cur_min = min(indexes)
        self.cur_max = max(indexes)
        logger.attr(self.name, f'{self.cur_min} - {self.cur_max}')
    def search_rows(self, main, keyword):
        if TASK_TAB_LIST.insight_row(keyword, main=main):
            logger.info('Successfully navigated to ' + keyword.name + ' area')
            if TASK_TAB_LIST.select_row(keyword, main=main):
                logger.info('Successfully selected ' + keyword.name + ' tab')
                return True
            else:
                logger.error(f'Failed to select {keyword.name} tab')
                return False
        else:
            logger.error(f'Failed to find {keyword.name} in task list')
            return False
    def insight_row(self, row: Keyword, main: ModuleBase, skip_first_screenshot=True) -> bool:
        """重写以处理动态任务列表，强制左移右移指定次数"""
        logger.info(f'Insight activity tab: {row}')

        # 首先尝试在当前可见范围内查找
        self.load_rows(main=main)
        if self.keyword2button(row, show_warning=False):
            return True

        max_total_drags = 8   # 总的拖拽次数（比如左右各 2 次，一共 4 次；你可以改成 8、12…）
        per_direction_drags = 2  # 每个方向要拖动的次数
        total_drag_count = 0

        # 按顺序：左 -> 右 -> 左 -> 右，直到总次数用完
        while total_drag_count < max_total_drags:
            for direction in ["left", "right"]:
                for _ in range(per_direction_drags):
                    if total_drag_count >= max_total_drags:
                        break

                    # 执行滑动
                    self.drag_page(direction, main=main)
                    total_drag_count += 1

                    # 等待界面稳定
                    self.wait_bottom_appear(main, skip_first_screenshot=False)
                    main.wait_until_stable(
                        self.search_button,
                        timer=Timer(0, count=0),
                        timeout=Timer(3, count=8)
                    )

                    # 重新识别
                    self.load_rows(main=main)
                    if self.keyword2button(row, show_warning=False):
                        return True

        logger.warning(f'Target {row} not found after {total_drag_count} total drags')
        return False
    def is_row_selected(self, button: OcrResultButton, main: ModuleBase) -> bool:
        """根据不同任务类型判断选中状态"""
        # 根据任务类型使用不同的判断逻辑
        if button.matched_keyword.name == "JiFenSaiKeyword":
            return main.appear(JI_FEN_SAI_CHECK)
        elif button.matched_keyword.name == "MissionKeyword":
            return main.appear(MISSION_CHECK)
        elif button.matched_keyword.name == "OrganizationKeyword":
            return main.appear(ORGANIZATION_PANEL)
        elif button.matched_keyword.name == "LeaderBoardKeyword":
            return main.appear(LEADER_BOARD_CHECK)
        elif button.matched_keyword.name == "DuelKeyword":
            return  main.appear(DUEL_CHECK)
        elif button.matched_keyword.name == "FengRaoKeyword":
            return main.appear(FENG_RAO_CHECK)
        elif button.matched_keyword.name == "TrailKeyword":
            return main.appear(TRAIL_SURVIVAL_CHECK)
        elif button.matched_keyword.name == "SquadRaidKeyword":
            return main.appear(SQUAD_RAID_CHECK)
        elif button.matched_keyword.name == "RenZheTiaoZhanKeyword":
            return main.appear(REN_ZHE_TIAO_ZHAN_CHECK)
        return False




TASK_TAB_LIST = DraggableTaskTabList(
    name='TaskTabList',
    keyword_class=TaskTab,
    custom_ocr=TaskOcr,
    search_button=MAIN_GOTO_TASK_SEARCH_AREA,
    check_row_order=False,
    active_color=(212,190,143),
    drag_direction="right",
)