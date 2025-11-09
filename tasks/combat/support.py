import numpy as np
from module.base.base import ModuleBase
from module.base.button import ClickButton
from module.base.timer import Timer
from module.base.utils.utils import area_offset, area_size, crop, random_rectangle_vector_opted
from module.logger import logger
from module.ocr.ocr import Ocr
from module.ui.draggable_list import DraggableList
from tasks.combat.assets.assets_combat_support import *
from tasks.squadraid.assets.assets_squadraid_fight import SQUAD_RAID_FIGHT_LOADING

class NextSupportCharacter:
  
    def __init__(self, screenshot):
        self.name = "NextSupportCharacter"
        self.button = self.get_next_support_character_button(screenshot)

    def __bool__(self):
        return self.button is not None
    

    def get_next_support_character_button(self, screenshot) -> ClickButton | None:
        COMBAT_SUPPORT_ADD_LIMITED.load_search(COMBAT_SUPPORT_ADD_SEARCH.area)
        if COMBAT_SUPPORT_ADD_LIMITED.match_template(screenshot, similarity=0.75):
            # Move area to the next character card center
            area = COMBAT_SUPPORT_ADD_LIMITED.button
            area = area_offset((0, 75, 85, 155), offset=area[:2])
            if area[3] < COMBAT_SUPPORT_LIST_GRID.area[3]:
                return ClickButton(area, name=self.name)
            else:
                # Out of list
                logger.info('Next character is out of list')
                return None
        logger.info(' character is not limited')
        SUPPORT_SELECTED.load_search(COMBAT_SUPPORT_ADD_SEARCH.area)
        if SUPPORT_SELECTED.match_template(screenshot, similarity=0.75):
            # Move area to the next character card center
            area = SUPPORT_SELECTED.button
            area = area_offset((-15, 75,85, 155), offset=area[:2])
            logger.info(area)
            if area[3] < COMBAT_SUPPORT_LIST_GRID.area[3]:
                return ClickButton(area, name=self.name)
            else:
                # Out of list
                logger.info('Next character is out of list')
                return None
        else:
            return None
    def get_next_support_character_button_base_selected(self, screenshot) -> ClickButton | None:
        SUPPORT_SELECTED.load_search(COMBAT_SUPPORT_ADD_SEARCH.area)
        if SUPPORT_SELECTED.match_template(screenshot, similarity=0.75):
            # Move area to the next character card center
            area = SUPPORT_SELECTED.button
            area = area_offset((-10, 65,75, 145), offset=area[:2])
            if area[3] < COMBAT_SUPPORT_LIST_GRID.area[3]:
                return ClickButton(area, name=self.name)
            else:
                # Out of list
                logger.info('Next character is out of list')
                return None
        else:
            logger.info('Next character is not selected')
            return None


    def get_next_support_character_base_area(self, screenshot,area) -> ClickButton | None:
        SUPPORT_SELECTED.load_search(area)
        if SUPPORT_SELECTED.match_template(screenshot, similarity=0.75):
            area = SUPPORT_SELECTED.button
            area = area_offset((-10, 65,75, 145), offset=area[:2])
            if area[3] < COMBAT_SUPPORT_LIST_GRID.area[3]:
                return ClickButton(area, name=self.name)
            else:
                # Out of list
                logger.info('Next character is out of list')
                return None
        COMBAT_SUPPORT_ADD_LIMITED.load_search(area)
        if COMBAT_SUPPORT_ADD_LIMITED.match_template(screenshot, similarity=0.75):
            # Move area to the next character card center
            area = COMBAT_SUPPORT_ADD_LIMITED.button
            area = area_offset((0, 75, 85, 155), offset=area[:2])
            if area[3] < COMBAT_SUPPORT_LIST_GRID.area[3]:
                return ClickButton(area, name=self.name)
            else:
                # Out of list
                logger.info('Next character is out of list')
                return None   

    def is_next_support_character_selected(self, screenshot) -> bool:
        if self.button is None:
            return False
        area = self.button.area
        # Move area from the card center to the left edge of the card
        area = area_offset(area, offset=(-120, 0))
        image = crop(screenshot, area, copy=False)
        return SUPPORT_SELECTED.match_template(image, similarity=0.75, direct_match=True)

class SupportSelectList:
    drag_vector = (0.5, 0.6)
    def __init__(
            self,
            name,
            search_button: ButtonWrapper,
            drag_direction: str = "down"
    ):
        self.name = name
        self.search_button = search_button
        self.drag_direction = drag_direction
    def __str__(self):
        return f'DraggableList({self.name})'

    __repr__ = __str__

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(self.name)
    def drag_page(self, direction: str, main: ModuleBase, vector=None):
        """
        Args:
            direction: up, down, left, right
            main:
            vector (tuple[float, float]): Specific `drag_vector`, None by default to use `self.drag_vector`
        """
        if vector is None:
            vector = self.drag_vector
        vector = np.random.uniform(*vector)
        width, height = area_size(self.search_button.button)
        if direction == 'up':
            vector = (0, vector * height)
        elif direction == 'down':
            vector = (0, -vector * height)
        elif direction == 'left':
            vector = (vector * width, 0)
        elif direction == 'right':
            vector = (-vector * width, 0)
        else:
            logger.warning(f'Unknown drag direction: {direction}')
            return

        p1, p2 = random_rectangle_vector_opted(vector, box=self.search_button.button)
        main.device.drag(p1, p2, name=f'{self.name}_DRAG')
    
    def get_next_support_character_button_until_available(self, main:ModuleBase):
        """Returns the next support character button in the support list."""
        darg_interval=Timer(2,4)
        for _ in main.loop():
            COMBAT_SUPPORT_ADD.load_search(COMBAT_SUPPORT_ADD_SEARCH.area)
            buttons=COMBAT_SUPPORT_ADD.match_multi_template(main.device.image)
            if buttons:  
                return buttons[0]
            if darg_interval.reached():  
                self.drag_page(self.drag_direction, main=main)
                main.wait_until_stable(  
                        self.search_button,  
                        timer=Timer(0, count=0),  
                        timeout=Timer(1.5, count=5)  
                )
                darg_interval.reset()
    
    def get_next_available_support_character_button_base_selected(self, main:ModuleBase):
        """Returns the next support character button in the support list."""
        next=NextSupportCharacter(main.device.image)
        button=next.get_next_support_character_button_base_selected(main.device.image)
        if not button:
            self.drag_page(self.drag_direction, main=main)
            main.wait_until_stable(  
                    self.search_button,  
                    timer=Timer(0, count=0),  
                    timeout=Timer(1.5, count=5)  
            )
            button=next.get_next_support_character_button_base_selected(main.device.image)
            
 
        COMBAT_SUPPORT_ADD.load_search(button.area)  
        if COMBAT_SUPPORT_ADD.match_template(main.device.image, similarity=0.55):
            return button
        COMBAT_SUPPORT_ADD_LIMITED.load_search(button.area)
        if COMBAT_SUPPORT_ADD_LIMITED.match_template(main.device.image, similarity=0.75):
            next_button=next.get_next_support_character_base_area(button.area)
            drag_interval=Timer(2,4)
            for _ in main.loop():
                if not next_button and drag_interval.reached():
                    self.drag_page(self.drag_direction, main=main)
                    main.wait_until_stable(  
                            self.search_button,  
                            timer=Timer(0, count=0),  
                            timeout=Timer(1.5, count=5)  
                    )
                    drag_interval.reset()
                    next_button=next.get_next_support_character_base_area(button.area)
                    continue
                COMBAT_SUPPORT_ADD.load_search(next_button.area) 
                if COMBAT_SUPPORT_ADD.match_template(main.device.image, similarity=0.65):
                    print(next_button.area)
                    return next_button
                next_button=next.get_next_support_character_base_area(next_button.area)
    def select_first_support_character(self, main:ModuleBase):
        button=self.get_next_support_character_button_until_available(main)
        click_interval=Timer(2)
        for _ in main.loop():
            SUPPORT_SELECTED.load_search(button.area)
            if main.match_template(SUPPORT_SELECTED,similarity=0.55):
                break
            if click_interval.reached():  
                main.device.click(button) 
                main.device.click_record_remove(button) 
                click_interval.reset()
    def select_next_support_character(self, main:ModuleBase):
        timeout=Timer(1,3).start()
        for _ in main.loop():
            if timeout.reached():
                logger.info(f'same character notify disappear')  
                break
            if main.appear(COMBAT_SUPPORT_SAME_CHARACTER_NOTIFY):
                timeout.reset()
                continue
        button=self.get_next_available_support_character_button_base_selected(main)
        click_interval=Timer(2)
        
        for _ in main.loop():               
            SUPPORT_SELECTED.load_search(button.area)
            if main.appear(SUPPORT_SELECTED,similarity=0.55):
                break
            if main.match_template(SQUAD_RAID_FIGHT_LOADING):
                break
            if click_interval.reached():  
                main.device.click(button)
                main.device.click_record_remove(button)  
                click_interval.reset()
            continue



        

            
        

SUPPORT_LIST = SupportSelectList(  
    name='SUPPORT_LIST',  
    search_button=COMBAT_SUPPORT_LIST_SCROLL,  
    drag_direction="down"  
)
    