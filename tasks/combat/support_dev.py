import os
import time
from PIL import Image
import cv2
import numpy as np
from module.base.button import match_template
from module.base.decorator import cached_property
from module.base.utils import area_offset, area_pad
from module.base.utils.utils import crop, image_size, load_image
from module.config.utils import iter_folder, random_id
from module.logger import logger
from tasks.base.ui import UI
from tasks.combat.assets.assets_combat_support_dev import *
from tasks.combat.assets.assets_combat_support import *


def get_position_in_original_image(position_in_croped_image, crop_area):
    """
    Returns:
        tuple: (x, y) of position in original image
    """
    return (
        position_in_croped_image[0] + crop_area[0],
        position_in_croped_image[1] + crop_area[1]) if position_in_croped_image else None


class SupportCharacter:
    _image_cache = {}
    _crop_area = COMBAT_SUPPORT_LIST_GRID.matched_button.area

    def __init__(self, name, screenshot, similarity=0.75):
        self.name = name
        self.image = self._scale_character()
        self.screenshot = crop(screenshot, SupportCharacter._crop_area, copy=False)
        self.similarity = similarity
        self.button = self._find_character()

    def __bool__(self):
        # __bool__ is called when use an object of the class in a boolean context
        return self.button is not None

    def __str__(self):
        return f'SupportCharacter({self.name})'

    __repr__ = __str__

    @classmethod
    def load_image(cls, file):
        image = load_image(file)
        size = image_size(image)
        # Template from support page
        if size == (74, 75):
            return image
        # Template from character list page
        if size == (95, 89):
            image = cv2.resize(image, (74, 75))
            return image
        # Unexpected size, resize anyway
        logger.warning(f'Unexpected shape from support template {file}, image size: {size}')
        cv2.resize(image, (74, 75))
        return image

    def _scale_character(self):
        """
        Returns:
            Image: Character image after scaled
        """

        if self.name in SupportCharacter._image_cache:
            logger.info(f"Using cached image of {self.name}")
            return SupportCharacter._image_cache[self.name]

        image = self.load_image(f"assets/character/{self.name}.png")
        SupportCharacter._image_cache[self.name] = image
        logger.info(f"Character {self.name} image cached")
        return image

    def _find_character(self):
        character = np.array(self.image)
        support_list_img = self.screenshot
        res = cv2.matchTemplate(
            character, support_list_img, cv2.TM_CCOEFF_NORMED)

        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        max_loc = get_position_in_original_image(
            max_loc, SupportCharacter._crop_area)
        character_width = character.shape[1]
        character_height = character.shape[0]

        return (max_loc[0], max_loc[1], max_loc[0] + character_width, max_loc[1] + character_height) \
            if max_val >= self.similarity else None

    def selected_icon_search(self):
        """
        Returns:
            tuple: (x1, y1, x2, y2) of selected icon search area
        """
        # Check the left of character avatar
        return 0, self.button[1], self.button[0], self.button[3]
class SupportDev(UI):
   

    def iter_character_image(self):
        op_x, op_y, _, _ = CHARACTER_OPERATE.area
        _, limit_y1, _, limit_y2 = CHARACTER_OPERATE.search
        x1, y1, x2, y2 = CHARACTER_AVATAR.area
        relative = area_offset(CHARACTER_AVATAR.area, offset=(-op_x, -op_y))
        # Find CHARACTER_OPERATE and move to CHARACTER_AVATAR
        for button in CHARACTER_OPERATE.match_multi_template(self.device.image):
            area = area_offset(relative, button.area[:2])
            # CHARACTER_OPERATE has different relative to CHARACTER_AVATAR in ornament and dungeon
            # use static x coordinate
            area = (x1, area[1], x2, area[3])
            # Limit in height of CHARACTER_OPERATE.search
            if limit_y1 <= area[1] and area[3] <= limit_y2:
                yield area

    @cached_property
    def all_support_templates(self):
        """
        Returns:
            dict: Key: filename, value: image
        """
        data = {}
        for file in iter_folder('assets/character', ext='.png'):
            image = SupportCharacter.load_image(file)
            data[file] = image
        os.makedirs('screenshots/support_dev', exist_ok=True)
        for file in iter_folder('screenshots/support_dev', ext='.png'):
            image = SupportCharacter.load_image(file)
            data[file] = image
        return data

    def gen_support_template_from_area(self, area):
        """
        if match existing templates, do nothing
        otherwise create new template
        """
        search = area_pad(area, pad=5)
        search_image = self.image_crop(search, copy=False)

        # Test if match existing templates
        for template in self.all_support_templates.values():
            if match_template(search_image, template, similarity=0.75):
                return False

        # No match, create new template
        image = self.image_crop(area, copy=False)
        now = int(time.time() * 1000)
        file = f'screenshots/support_dev/{now}_{random_id(length=6)}.png'
        logger.info(f'New support template: {file}')
        Image.fromarray(image).save(file)
        _ = self.all_support_templates
        self.all_support_templates[file] = image
        return True

    def gen_support_templates(self):
        """
        Generate support templates from image
        """
        for area in self.iter_character_image():
            self.gen_support_template_from_area(area)