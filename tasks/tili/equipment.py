from module.base.button import match_template
from module.base.timer import Timer
from module.base.utils import crop
from module.exception import GameStuckError
from module.logger import logger
from module.ocr.ocr import Digit, Ocr, DigitCounter

from tasks.base.assets.assets_base import TILI_REMAIN, TI_LI_REMAIN_COUNTER
from tasks.base.assets.assets_base_popup import *
from tasks.base.page import *
from tasks.base.ui import UI
from tasks.tili.assets.assets_tili_equipment import *
from tasks.tili.keyword import  MopUpKeyword,SyntheticKeyword
from tasks.tili.ocr import StuffOcr


class Equipment(UI):
    def handle_equipment(self):
        self.device.click_record_clear()
        self.device.stuck_record_clear()
        self.ui_ensure(page_main)
        ocr=DigitCounter(TI_LI_REMAIN_COUNTER,lang='cn')
        current,remain,total=ocr.ocr_single_line(self.device.image)
        if current<5 and total==200:
            self.config.TiLi_TiLiRemain=current
            return False
        self._equipment_enter()
        self.device.stuck_timer=Timer(300,count=300).start()
        try:
            for _ in self.loop():
                self._equipment_part_red_dot_handle()
                self.ui_ensure(page_equipment)
                self.device.click(EQUIPMENT_KNIFE)
                self._select_equipment_part()
                self._stuff_material_check()
                res=self._start_sweep()
                self.ui_ensure(page_equipment)
                self._synthesized_and_equipped()
                if res:
                    break
        finally:
            self.device.stuck_timer=Timer(60,count=60).start()







    def _equipment_enter(self):
        time = Timer(20, count=30).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError('Equipment Enter Stuck')
            if self.appear(EQUIPMENT_CHECK):
                break
            if self.appear_then_click(MAIN_GOTO_EQUIPMENT):
                continue
            if self.appear_then_click(MAIN_GOTO_EQUIPMENT_LIST):
                continue

    def _equipment_part_red_dot_handle(self):
        time = Timer(1, count=2).start()
        synthetic_success=False
        for _ in self.loop():
            if time.reached():
                break
            if self._synthesized_and_equipped() and synthetic_success==False:
                synthetic_success=True
            if self.appear(POPUP_CLOSE, interval=0):
                break
            EQUIPMENT_PART_DETAIL_RED_DOT.load_search(EQUIPMENT_PART_DETAIL_AREA.area)
            if self.appear_then_click(EQUIPMENT_PART_DETAIL_RED_DOT, interval=1):
                time.reset()
                continue
            EQUIPMENT_PART_RED_DOT.load_search(EQUIPMENT_PART_AREA.area)
            if self.appear_then_click(EQUIPMENT_PART_RED_DOT, interval=1):
                time.reset()
                synthetic_success=False
                continue

    def _select_equipment_part(self):
        """按顺序尝试装备部件，直到找到可升级的为止"""
        valid_parts = self._get_valid_equipment_parts()
        if not valid_parts:
            logger.info("No equipment parts below level found")
            return False
        res=None
        for button in valid_parts:
            logger.info(f"Trying equipment part: {button}")
            # 切换装备，最多尝试 3 次
            if not self._switch_equipment_with_verification(button, max_retries=3):
                logger.warning(f"Failed to select {button} after retries, moving to next part")
                continue  # 切换失败，直接下一个装备
            res = self._check_part_status()
            if res and len(res) > 0:
                logger.info(f"Equipment Part Stuff Select Success")
                break
            else:
                logger.info(f"{button} cannot be upgraded, moving to next part")
                continue  # 不可扫荡，继续下一个
        #进入材料详情界面
        time=Timer(2, count=5).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError('Equipment Part Stuff Select Click Error ')
            if self.appear(STUFF_CHECK):
                return True
            self.device.click(res[0])
        return False

    def _switch_equipment_with_verification(self, button, max_retries=3):
        """点击装备并验证切换成功，失败会重试"""
        for attempt in range(max_retries):
            timeout = Timer(3, count=6).start()
            click_interval = Timer(1)
            # 获取当前装备详情截图作为基准
            if button == EQUIPMENT_KNIFE:
                return True
            # 如果需要切换的是刀，则直接不需要验证
            self.device.screenshot()
            initial_detail = self.image_crop(EQUIPMENT_PART_DETAIL.area, copy=True)
            while not timeout.reached():
                self.device.screenshot()
                # 点击装备按钮
                if click_interval.reached():
                    self.device.click(button)
                    click_interval.reset()
                    self.device.sleep(0.3)  # 等待 UI 响应

                    # 检查是否切换成功
                    current_detail = self.image_crop(EQUIPMENT_PART_DETAIL.area, copy=False)
                    if not match_template(current_detail, initial_detail, similarity=0.9):
                        logger.info(f"Equipment switched successfully to {button}")
                        return True

            logger.warning(f"Attempt {attempt + 1}/{max_retries} failed to switch {button}")

        return False

    def _get_valid_equipment_parts(self):
        """Get all equipment parts below level 79"""
        part_areas = [EQUIPMENT_KNIFE, EQUIPMENT_RING, EQUIPMENT_CAP,
                      EQUIPMENT_SHIRT, EQUIPMENT_BOOK, EQUIPMENT_NECKLACE]
        self.device.screenshot()
        image_list = [crop(self.device.image, area.area) for area in part_areas]
        ocr = Digit(part_areas[0])
        results = ocr.ocr_multi_lines(image_list)
        valid_parts = []
        for i, (value, score) in enumerate(results):
            logger.info(f"Part {i + 1}: {value}")
            if value < self.config.TiLi_LevelRestrictions:
                # 直接使用原始的 Button 对象
                valid_parts.append(part_areas[i])
        return valid_parts

    def _check_part_status(self):
        """检测铜币和升级条件"""
        time = Timer(2, count=5).start()
        ocr = Ocr(EQUIPMENT_PART_STUFF_AREA)

        for _ in self.loop():
            if time.reached():
                return False
            res = ocr.matched_ocr(self.device.image, keyword_classes=MopUpKeyword)
            if res and len(res) > 0:
                return res
        return False

    def _stuff_material_check(self):
        time = Timer(20, count=30).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError('Equipment Advance Stuff Part 1 Stuck')
            ocr = StuffOcr(STUFF_PART_1)
            current, remain, total = ocr.ocr_single_line(self.device.image)
            if total > 0 and remain > 0:
                self.device.click(STUFF_PART_1)
                return True
            elif total > 0 >= remain:
                break
        for _ in self.loop():
            if time.reached():
                raise GameStuckError('Equipment Advance Stuff Part 1 Stuck')
            ocr = StuffOcr(STUFF_PART_2)
            current, remain, total = ocr.ocr_single_line(self.device.image)
            if total > 0 and remain > 0:
                self.device.click(STUFF_PART_2)
                return True
            elif total > 0 >= remain:
                break
        return False

    def _start_sweep(self):
        time = Timer(4, count=5).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError('Equipment Sweep Enter Stuck')
            SWEEP_RUNNING.load_search(SWEEP_AREA.area)
            if self.appear(SWEEP_RUNNING):
                break
            if self.appear_then_click(SWEEP_START,similarity=0.9, interval=1):
                continue
            if STUFF_SWEEP_BUTTON.match_template_luma(self.device.image, similarity=0.9):
                self.device.click(STUFF_SWEEP_BUTTON)
                continue

        for _ in self.loop():
            # 体力不足
            if self.appear(TI_LI_SHORTAGE):
                return True
            # 材料足够
            if self.appear(STUFF_MATERIAL_FULL):
                return False
            # 体力充足，材料不足，继续扫荡
            SWEEP_RUNNING.load_search(SWEEP_AREA.area)
            self.appear_then_click(SWEEP_RUNNING,similarity=0.9, interval=0.5)

            SWEEP_CONTINUE.load_search(SWEEP_AREA.area)
            if self.appear(SWEEP_CONTINUE,similarity=0.9, interval=2):
                if self.appear(STUFF_MATERIAL_FULL):
                    return False
                else:
                    self.device.click(SWEEP_CONTINUE)

        return True
    def _synthesized_and_equipped(self):
        ocr=Ocr(EQUIPMENT_PART_STUFF_AREA)
        time=Timer(30, count=30).start()
        select_time=Timer(2, count=3).start()
        for _ in self.loop():
            if select_time.reached():
                logger.info("Not Select Synthesized Stuff")
                return True
            if time.reached():
                raise GameStuckError('Equipment Synthesized Stuff Stuck')
            stuffs=ocr.matched_ocr(self.device.image, SyntheticKeyword)
            if stuffs and len(stuffs) > 0:
                synthetic_buttons = [stuff for stuff in stuffs if stuff.matched_keyword.name == 'Synthetic']
                if not synthetic_buttons or len(synthetic_buttons) <=0:
                    continue
                logger.info(f"Synthesized  Stuff Select Success ")
                select_time.reset()
                 #进入材料详情界面
                for _ in self.loop():
                    if time.reached():
                        raise GameStuckError('Synthesized Stuff Select Click Error ')
                    if self.appear(STUFF_CHECK):
                        break
                    self.device.click(synthetic_buttons[0])
                for _ in self.loop():
                    select_time.reset()
                    if time.reached():
                        raise GameStuckError('Synthesized Stuff Synthesized Or Equipped Error ')
                    if self.appear(EQUIPMENT_CHECK):
                        break
                    if self.appear_then_click(STUFF_SYNTHETIC_BUTTON, interval=1):
                        continue
                    if self.appear_then_click(STUFF_EQUIPMENT,interval=1):
                        continue





