from module.base.button import match_template
from module.base.timer import Timer
from module.base.utils import crop
from module.exception import GameStuckError
from module.logger import logger
from module.ocr.ocr import Digit, Ocr, DigitCounter

from tasks.base.assets.assets_base import  TI_LI_REMAIN_COUNTER
from tasks.base.assets.assets_base_popup import *
from tasks.base.page import *
from tasks.base.ui import UI
from tasks.tili.assets.assets_tili_equipment import *
from tasks.tili.tili_keyword import  MopUpKeyword,SyntheticKeyword
from tasks.tili.ocr import StuffOcr


class Equipment(UI):
    def handle_equipment(self):
        self.device.click_record_clear()
        self.device.stuck_record_clear()
        self.ui_ensure(page_main)
        ocr=DigitCounter(TI_LI_REMAIN_COUNTER,lang='cn')
        current,remain,total=ocr.ocr_single_line(self.device.image)
        if current>0 and total==200:
            self.config.stored.TiLi.value=current
            if current<5 and total==200:
                return False
        self._equipment_enter()
        self.device.stuck_timer=Timer(300,count=300).start()
        coins_sufficient=True
        try:
            for _ in self.loop():
                self._select_equipment_part(check_status=False)
                self._synthesized_and_equipped()
                if coins_sufficient:
                    coins_sufficient=self._equipment_part_red_dot_handle()
                self._select_equipment_part()
                res=self._start_sweep()
                if res:
                    break

        finally:
            self.ui_ensure(page_equipment)
            self._synthesized_and_equipped()
            self._equipment_part_red_dot_handle()
            self.device.stuck_timer=Timer(60,count=60).start()
        self.ui_goto_main()
        current,remain,total=ocr.ocr_single_line(self.device.image)
        if  total!=0:
            self.config.stored.TiLi.value=current
            







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
        time = Timer(2, count=3).start()
        for _ in self.loop():
            if time.reached():
                break
            if self.appear(POPUP_CLOSE, interval=0):
                return False
            EQUIPMENT_PART_DETAIL_RED_DOT.load_search(EQUIPMENT_PART_UPGRADE.area)
            if self.appear_then_click(EQUIPMENT_PART_DETAIL_RED_DOT, interval=1):
                time.reset()
                continue
            if self.appear_then_click(EQUIPMENT_PART_PROMOTION, interval=1):
                time.reset()
                continue
            
            
        return True
    def _select_equipment_part(self,check_status=True):
        self.ui_ensure(page_equipment)
        self.device.click(EQUIPMENT_KNIFE)
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
            if check_status:
                res = self._check_part_status()
                if res and len(res) > 0:
                    logger.info(f"Equipment Part Stuff Select Success")
                    break
                else:
                    logger.info(f"{button} cannot be mopup, moving to next part")
                    continue  # 不可扫荡，继续下一个
            else:
                break

                
            
        return True
       

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
        time = Timer(1, count=3).start()
        ocr = Ocr(EQUIPMENT_PART_STUFF_AREA)
        for _ in self.loop():
            if time.reached():
                return False
            res = ocr.matched_ocr(self.device.image, keyword_classes=[MopUpKeyword, SyntheticKeyword])
            if res and len(res) > 0:
                return res
        return False



    def _start_sweep(self):
        ocr=StuffOcr(EQUIPMENT_PART_STUFF_AREA)
        time=Timer(1,count=3).start()
        for _ in self.loop():
            if time.reached():
                return False
            buttons=ocr.matched_ocr(self.device.image, keyword_classes=[MopUpKeyword])
            if buttons and len(buttons)>0:
                break
            else :
                logger.info("No Mop Up Button Found")
                continue
                
        #进入材料详情界面
        time=Timer(2, count=4).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError('Equipment Part Stuff Select Click Error ')
            if self.appear(STUFF_CHECK):
                break
            self.device.click(buttons[0])
        
       
        time = Timer(60, count=60).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError('Equipment Sweep Enter Stuck')
            if self.match_template_color(STUFF_SWEEP_BUTTON,interval=1):
                self.device.click(STUFF_SWEEP_BUTTON)
                continue
            # 体力不足
            if self.appear(TI_LI_SHORTAGE):
                return True
            # 材料足够
            STUFF_MATERIAL_FULL.load_search(FULL_SCREEN.area)
            if self.appear(STUFF_MATERIAL_FULL):
                return False
            # 体力充足，材料不足，继续扫荡
            SWEEP_CONTINUE.load_search(SWEEP_AREA.area)
            if self.appear(SWEEP_CONTINUE,similarity=0.9, interval=2):
                STUFF_MATERIAL_FULL.load_search(FULL_SCREEN.area)
                if self.appear(STUFF_MATERIAL_FULL):
                    return False
                else:
                    self.device.click(SWEEP_CONTINUE)
            SWEEP_RUNNING.load_search(SWEEP_AREA.area)
            self.appear_then_click(SWEEP_RUNNING,similarity=0.9, interval=0.5)
            if self.appear_then_click(SWEEP_START,similarity=0.9, interval=1):
                continue
        return True
    def _synthesized_and_equipped(self):
        ocr=Ocr(EQUIPMENT_PART_STUFF_AREA)
        time=Timer(30, count=30).start()
        select_time=Timer(1, count=3).start()
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





