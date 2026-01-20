import re

import module.config.server as server
from module.config.server import VALID_LANG
from module.exception import RequestHumanTakeover, ScriptError
from module.logger import logger


from tasks.base.page import Page, page_main
from tasks.base.popup import PopupHandler



class MainPage(PopupHandler):
    # Same as BigmapPlane class
    # Current plane

    _lang_checked = False
    _lang_check_success = True


    def check_lang_from_map_plane(self) -> str | None:
        logger.info('check_lang_from_map_plane')
        lang_unknown = self.config.Emulator_GameLanguage == 'auto'

        if lang_unknown:
            lang_list = VALID_LANG
        else:
            # Try current lang first
            lang_list = [server.lang] if server.lang != 'auto' else []
            lang_list += [lang for lang in VALID_LANG if lang != server.lang]

        for lang in lang_list:
            logger.info(f'Try ocr in lang {lang}')
            MainPage._lang_checked = True
            MainPage._lang_check_success = True
            return lang

        if lang_unknown:
            # Force return 'cn' when auto-detecting
            logger.info('check_lang_from_map_plane matched lang: cn (forced)')
            self.config.Emulator_GameLanguage = 'cn'
            server.set_lang('cn')
            MainPage._lang_checked = True
            MainPage._lang_check_success = True
            return 'cn'
        else:
            logger.warning(f'Cannot detect in-game text language, assume current lang={server.lang} is correct')
            MainPage._lang_checked = True
            MainPage._lang_check_success = False
            return server.lang

    def handle_lang_check(self, page: Page):
        """
        Args:
            page:

        Returns:
            bool: If checked
        """
        if MainPage._lang_checked:
            return False
        if page != page_main:
            return False

        self.check_lang_from_map_plane()
        return True

    def acquire_lang_checked(self):
        """
        Returns:
            bool: If checked
        """
        if MainPage._lang_checked:
            return False

        logger.info('acquire_lang_checked')
        try:
            self.ui_goto(page_main)
        except AttributeError:
            logger.critical('Method ui_goto() not found, class MainPage must be inherited by class UI')
            raise ScriptError

        self.handle_lang_check(page=page_main)
        return True
