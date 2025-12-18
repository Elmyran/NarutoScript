from module.base.timer import Timer
from module.exception import GameStuckError
from module.logger.logger import logger
from module.ocr.ocr import Digit, Ocr, DigitCounter
from tasks.base.assets.assets_base import  TI_LI_REMAIN_COUNTER
from tasks.base.assets.assets_base_popup import *
from tasks.base.page import *
from tasks.base.taskui import TaskUI
from tasks.base.ui import UI
from tasks.tili.assets.assets_tili_equipment import *
from tasks.tili.assets.assets_tili_equipment_area import *

from tasks.tili.assets.assets_tili_equipment_part import *
from tasks.tili.tili_keyword import EquipKeyword, SweepKeyword, SyntheticKeyword



class Equipment(TaskUI):
    blacklist=[],
    equipment=None,
    stuff=None,
    level=None,
    def run(self):
        self.blacklist=[]
        self.device.click_record_clear()
        self.device.stuck_record_clear()
        self.ui_ensure(page_main)
        ocr=DigitCounter(TI_LI_REMAIN_COUNTER)
        current,_,total=ocr.ocr_single_line(self.device.image)
        if current>=0 and total==200:
            self.config.stored.TiLi.value=current
            if current<10 :
                return True
        self.handle_equipment()
        self.ui_goto_main()
        ocr=DigitCounter(TI_LI_REMAIN_COUNTER)
        current,_,_=ocr.ocr_single_line(self.device.image)
        self.config.stored.TiLi.value=current
            
    def handle_equipment(self):
        self._equipment_enter()
        for _ in self.loop():
            self._get_sweepable_equipment()
            if not self.has_equipment_below_level_limit():
                return True
            self.switch_to_equipment()
            self.synthetic()
            self.promote()
            if not self.is_sweep_button_appeared():
                self.blacklist.append(self.equipment)
                continue
            self._stuff_detail_enter()
            self._sweep_enter()
            self._sweep_run()
            if self._stop_sweep():
                self.back_to_main()
                return True

            self.back_to_main()
        
        
        
    def promote(self):
        if self.appear(EQUIPMENT_PROMOTION_BUTTON):
            logger.info('Find  promote button ')
            for _ in self.loop():
                if self.appear(STUFF_AUTO_FILL):
                    break
                if self.appear(COPPER_COINS_SHORTAGE):
                    self.back_to_main()
                    break
                if self.appear_then_click(EQUIPMENT_PROMOTION_BUTTON):
                    continue

            
    def synthetic(self):
        ocr=Ocr(STUFF_LIST_AREA)
        timeout=Timer(2,count=5).start()
        for _ in self.loop():
            if timeout.reached():
                logger.info('No stuff synthetic')   
                break
            appear=ocr.matched_ocr(self.device.image,[SyntheticKeyword,EquipKeyword])
            if appear:
                matched_keywords = [result.matched_keyword for result in appear]    
      
                if EquipKeyword in matched_keywords or  SyntheticKeyword in matched_keywords:  
                    timeout.reset() 
                else :
                    continue 
    
            else:
                continue                
            self.stuff=appear[0]
            self._stuff_detail_enter()
            if self._synthetic_and_equip():
                self.back_to_main()
                break

    def _synthetic_and_equip(self):
        for _ in self.loop():
            if self.appear(EQUIPMENT_CHECK):
                break
            if self.appear(COPPER_COINS_SHORTAGE):
                return True
            if self.appear_then_click(STUFF_SYNTHETIC_BUTTON,interval=1):
                continue
            if self.appear_then_click(STUFF_EQUIP_BUTTON,interval=1):
                continue
    def has_equipment_below_level_limit(self):
        if self.equipment and self.level:
            return True
        return False
    def _stop_sweep(self):
        if self.appear(SWEEP_CONTINUE):
            return True
        return False
    def back_to_main(self):
        for _ in self.loop():
            if self.appear(EQUIPMENT_CHECK):
                self.wait_until_stable(EQUIPMENT_CHECK, timer=Timer(1, count=3))
                break
            if self.appear_then_click(EQUIPMENT_POPUP_CLOSE_BUTTON,interval=1):
                continue
            
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
         
            if self.appear_then_click(MAIN_GOTO_EQUIPMENT_LIST):
                continue
    def _get_sweepable_equipment(self):
        EQUIPMENT=[EQUIPMENT_KNIFE, EQUIPMENT_RING, EQUIPMENT_CAP,
                      EQUIPMENT_SHIRT, EQUIPMENT_BOOK, EQUIPMENT_NECKLACE]
        limit_level=self.config.TiLiCost_LevelRestrictions
        for equipment in EQUIPMENT:
            if equipment in self.blacklist:
                continue
            ocr=Digit(equipment)
            level=ocr.ocr_single_line(self.device.image)
            if level<limit_level:
                self.equipment=equipment
                self.level=level
                break
        logger.info(f'Equipment {self.equipment} level {self.level}')
        



    def switch_to_equipment(self):
        logger.info(f'Switch to {self.equipment}')
        click_interval=Timer(1).start()
        for _ in self.loop():
            if self.appear(self.equipment,similarity=0.4):
                logger.info(f'{self.equipment} confirm ')
                break
            if click_interval.reached():
                self.equipment.clear_offset()
                self.device.click(self.equipment)

            
    def is_sweep_button_appeared(self):
        ocr=Ocr(STUFF_LIST_AREA)
        timeout=Timer(2,count=5).start()
        for _ in self.loop():
            if timeout.reached():
                return False
            appear=ocr.matched_ocr(self.device.image,SweepKeyword)
            if appear:
                self.stuff=appear[0]
                return True
    def _stuff_detail_enter(self):
        logger.info('Stuff Detail Enter')
        click_interval=Timer(1).start()
        for _ in self.loop():
            if self.appear(STUFF_DETAIL_CHECK):
                break
            if self.appear(STUFF_DETAIL_SWEEP_BUTTON):
                break
            if self.appear(STUFF_SYNTHETIC_BUTTON):
                break
            if click_interval.reached():
                self.device.click(self.stuff)
                click_interval.reset()
    def _sweep_enter(self):
        logger.info('Sweep Enter')
        for _ in self.loop():
            if self.appear(SWEEP_START):
                break
            if self.appear_then_click(STUFF_DETAIL_SWEEP_BUTTON,interval=1):
                continue
            
    def _sweep_run(self):
        logger.info('Sweep Run')  
        click_interval=Timer(0.5).start()
        count=0  
        for _ in self.loop():
            if self.appear(SWEEP_COMPLETE):
                break
            if self.appear_then_click(SWEEP_START,interval=1):
                continue
            if count<=3 and click_interval.reached():
                self.device.click(SWEEP_FASTER)
                self.device.click_record_remove(SWEEP_FASTER)
                count+=1
                click_interval.reset()



