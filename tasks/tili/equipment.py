from module.base.button import match_template
from module.base.timer import Timer
from module.base.utils import crop
from module.exception import GameStuckError
from module.logger import logger
from module.ocr.ocr import Digit, DigitCounter
from tasks.base.assets.assets_base import TILI_REMAIN
from tasks.base.page import *
from tasks.base.ui import UI
from tasks.tili.assets.assets_tili_equipment import *

class Equipment(UI):
    def handle_equipment(self):
        self.device.click_record_clear()
        self.ui_ensure(page_main)
        ocr=Digit(TILI_REMAIN,lang='cn')
        ti_li=ocr.ocr_single_line(self.device.image)
        self.config.TiLi_TiLiRemain=ti_li
        if ti_li<10:
            return False
        for _ in self.loop():
            if self._equipment_enter():
                res=self._equipment_advance()
                if res=='TI_LI_SHORTAGE':
                    break
            else:
                break
        self._equipment_exit()
            

    def _equipment_enter(self):
        time=Timer(20,count=30).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError('Equipment Enter Stuck')
            if self.appear(EQUIPMENT_CHECK):
                if self.appear(EQUIPMENT_KNIFE):
                    self.device.click(EQUIPMENT_KNIFE)
                break
            if self.ui_page_appear(page_stuff):
                self.device.click(EQUIPMENT_EXIT)
                continue
            if self.ui_page_appear(page_sweep):
                self.device.click(EQUIPMENT_EXIT)
                continue
            if self.appear_then_click(MAIN_GOTO_EQUIPMENT):
                continue
            if self.appear_then_click(MAIN_GOTO_EQUIPMENT_LIST):
                continue
        # Try equipment parts sequentially until success
        success = self._try_equipment_parts_sequentially()
        if not success:
            logger.warning("No equipment parts can be upgraded due to insufficient materials")
            return False
        else:
            return True



    def _try_equipment_parts_sequentially(self):
        """按顺序尝试装备部件，直到找到可升级的为止"""
        valid_parts = self._get_valid_equipment_parts()
        if not valid_parts:
            logger.info("No equipment parts below level found")
            return False

        for button in valid_parts:
            logger.info(f"Trying equipment part: {button}")
            # 切换装备，最多尝试 3 次
            if not self._select_equipment_with_verification(button, max_retries=3):
                logger.warning(f"Failed to select {button} after retries, moving to next part")
                continue  # 切换失败，直接下一个装备
            # 检查是否可升级
            res = self._check_equipment_upgradeable_and_advance()


            if res:
                return True  # 找到可升级装备
            else:
                logger.info(f"{button} cannot be upgraded, moving to next part")
                continue  # 铜币不足 / 材料不足，继续下一个

        return False


    def _select_equipment_with_verification(self, button, max_retries=3):
        """点击装备并验证切换成功，失败会重试"""
        for attempt in range(max_retries):
            timeout = Timer(3, count=6).start()
            click_interval = Timer(1)
            # 获取当前装备详情截图作为基准
            self.device.screenshot()
            initial_detail = self.image_crop(EQUIPMENT_PART_DETAIL.area, copy=True)

            while not timeout.reached():
                self.device.screenshot()

                # 点击装备按钮
                if click_interval.reached() and self.appear(button):
                    self.device.click(button)
                    click_interval.reset()
                    self.device.sleep(0.3)  # 等待 UI 响应

                    # 检查是否切换成功
                    current_detail = self.image_crop(EQUIPMENT_PART_DETAIL.area, copy=False)
                    if not match_template(current_detail, initial_detail, similarity=0.9):
                        logger.info(f"Equipment switched successfully to {button}")
                        return True

            logger.warning(f"Attempt {attempt+1}/{max_retries} failed to switch {button}")

        return False
    def _get_valid_equipment_parts(self):
        """Get all equipment parts below level 72"""
        part_areas = [EQUIPMENT_KNIFE, EQUIPMENT_RING, EQUIPMENT_CAP,
                      EQUIPMENT_SHIRT, EQUIPMENT_BOOK, EQUIPMENT_NECKLACE]

        self.device.screenshot()
        image_list = [crop(self.device.image, area.area) for area in part_areas]
        ocr = Digit(part_areas[0])
        results = ocr.ocr_multi_lines(image_list)

        valid_parts = []
        for i, (value, score) in enumerate(results):
            logger.info(f"Part {i+1}: {value}")
            if value < self.config.TiLi_LevelRestrictions:
                # 直接使用原始的 Button 对象
                valid_parts.append(part_areas[i])
        return valid_parts
    def _check_equipment_upgradeable_and_advance(self):
        """检测铜币和升级条件"""
        timeout = Timer(5, count=10).start()
        for _ in self.loop():
            if timeout.reached():
                return False
            if self.appear(STUFF_FILL_ALL):
                return True
                # 失败条件：铜币短缺
            if self.appear(COPPER_COINS_SHORTAGE, interval=1):
                logger.info("Insufficient copper coins, trying next equipment")
                self.device.click(COPPER_COINS_SHORTAGE)
                return False
            if self.appear(EQUIPMENT_ADVANCED_BUTTON, interval=1):
                self.device.click(EQUIPMENT_ADVANCED_BUTTON)
                continue
        return False
    def _equipment_advance(self):
        time=Timer(20,count=30).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError('Equipment Advance Stuck')
            if self.appear(STUFF_EQUIPMENT_DIRECT):
                break
            if self.appear(STUFF_SYNTHETIC_BUTTON):
                break
            if self.appear(STUFF_SWEEP_BUTTON):
                break
            stuff=self.find_first_unclaimed_item()
            if not stuff:
                continue
            self.device.click(stuff)

        for _ in self.loop():
            if time.reached():
                raise GameStuckError('Equipment Advance Stuff Part 1 Stuck')
            if self.appear(EQUIPMENT_CHECK):
                break
            if self.appear_then_click(STUFF_SYNTHETIC_BUTTON):
                continue
            if self.appear_then_click(STUFF_EQUIPMENT):
                continue
            if self.appear_then_click(STUFF_EQUIPMENT_DIRECT):
                continue
            ocr=DigitCounter(STUFF_PART_1)
            current, remain, total = ocr.ocr_single_line(self.device.image)
            if remain>0:
                self.device.click(STUFF_PART_1)
                res=self.sweep()
                if res=='TI_LI_SHORTAGE':
                    return 'TI_LI_SHORTAGE'
                elif res=='STUFF_FULL':
                    continue
            elif remain<=0:
                break
        for _ in self.loop():
            if time.reached():
                raise GameStuckError('Equipment Advance Stuff Part 2 Stuck')
            if self.appear(EQUIPMENT_CHECK):
                break
            if self.appear_then_click(STUFF_SYNTHETIC_BUTTON):
                continue
            if self.appear_then_click(STUFF_EQUIPMENT):
                continue
            if self.appear_then_click(STUFF_EQUIPMENT_DIRECT):
                continue
            ocr=DigitCounter(STUFF_PART_2)
            current, remain, total = ocr.ocr_single_line(self.device.image)
            if remain>0:
                self.device.click(STUFF_PART_2)
                res=self.sweep()
                if res=='TI_LI_SHORTAGE':
                    return 'TI_LI_SHORTAGE'
                elif res=='STUFF_FULL':
                    continue
            elif remain<=0:
                break






    def find_first_unclaimed_item(self):

        """
        从左到右找到第一个未获得的物品

        Returns:
            int: 第一个未获得物品的位置索引（0-5），如果都已获得则返回-1
        """
        # 定义六个物品的区域（从左到右）
        item_areas = [STUFF_1, STUFF_2, STUFF_3, STUFF_4, STUFF_5, STUFF_6]
        for i, area in enumerate(item_areas):
            # 检测该区域是否有鲜艳颜色（已获得状态）
            # 根据实际情况调整颜色值和阈值
            bright_color_count = self.image_color_count(
                area,
                color=(255, 255, 255),  # 鲜艳颜色，需要根据实际调整
                threshold=200,          # 颜色相似度阈值
                count=50               # 最小像素数量
            )

            if not bright_color_count:
                # 没有检测到鲜艳颜色，说明是暗色（未获得）
                logger.info(f"Found first unclaimed item at position {i}")
                return item_areas[i]

        logger.info("All items have been claimed")
        return None

    def sweep(self):
        time=Timer(4,count=5).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError('Equipment Sweep Enter Stuck')
            ocr=DigitCounter(TI_LI_REMAIN_BEFORE_SWEEP)
            current,remain,total= ocr.ocr_single_line(self.device.image)
            if current<5 and total==200:
                return 'TI_LI_SHORTAGE'
            if self.appear(SWEEP_DETAIL):
                break
            if self.appear_then_click(STUFF_SWEEP_BUTTON):
                continue
        sweep_time=Timer(10,count=15).start()
        for _ in self.loop():
            if sweep_time.reached():
                raise GameStuckError('Equipment Sweep Stuck')
            ocr=DigitCounter(TI_LI_REMAIN_AFTER_SWEEP)
            current,remain,total= ocr.ocr_single_line(self.device.image)
            if current<5 and total==200 :
                for _ in self.loop():
                    if self.appear(STUFF_CHECK):
                        break
                    if self.appear_then_click(SWEEP_CHECK):
                        continue
                self.config.TiLi_TiLiRemain=current
                return 'TI_LI_SHORTAGE'
            if STUFF_FULL.match_template(self.device.image,direct_match=True):
                for _ in self.loop():
                    if self.appear(STUFF_CHECK):
                        break
                    if self.appear(SWEEP_CHECK):
                        self.device.click(EQUIPMENT_EXIT)
                return 'STUFF_FULL'
            if SWEEP_RUNNING.match_template(self.device.image,direct_match=True):
                continue
            if self.appear(SWEEP_START):
                self.device.click(SWEEP_START)
                continue
            if self.appear(STUFF_SWEEP_BUTTON):
                self.device.click(STUFF_SWEEP_BUTTON)
                continue
        return 'TI_LI_SHORTAGE'

    def _equipment_exit(self):
        time=Timer(10,count=15).start()
        for _ in  self.loop():
            if time.reached():
                raise GameStuckError('Equipment Exit Stuck')
            if self.ui_page_appear(page_main):
                break
            if self.ui_page_appear(page_sweep):
                self.device.click(EQUIPMENT_EXIT)
                continue
            if self.ui_page_appear(page_stuff):
                self.device.click(EQUIPMENT_EXIT)
                continue
            if self.ui_page_appear(page_equipment):
                self.device.click(EQUIPMENT_EXIT)
                continue






