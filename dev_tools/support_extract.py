from module.exception import ScriptError
from module.logger import logger
from tasks.combat.support_dev import SupportDev
from tasks.base.page import page_squad_help_battle
class SupportExtract(SupportDev):
   
    def _init_support_page(self):
        """
        Set to stranger tab and full load support list

        Pages:
            in: COMBAT_SUPPORT_LIST
        """
        self.device.click_record_clear()


    def goto_support_page(self):
        """
        Pages:
            out: COMBAT_SUPPORT_LIST
        """
        self.ui_ensure(page_squad_help_battle)
        logger.info('Goto support page')
        # Goto first calyx golden
        self._init_support_page()

    def gen_templates(self):
        """
        Endlessly refreshing and scroll ramdom support, generate new support templates
        Stop manually if you think missing templates are all gathered.

        Pages:
            in: COMBAT_SUPPORT_LIST
        """
      
        for _ in self.loop():
            self.gen_support_templates()
               



if __name__ == '__main__':
    """
    Auto Extract support templates

    1. Run config_updater to find missing templates,
        it will print "WARNING: character template not exist: Castorice"
    2. Login to game, stay at whatever page
    3. Run support_extract
    4. Stop manually if you think missing templates are all gathered.
    
    """
    self = SupportExtract('src')
    self.device.screenshot()
    self.goto_support_page()
    self.gen_templates()

    # Test if support can be selected
    # from tasks.character.keywords import KEYWORDS_CHARACTER_LIST
    # self.support_set(KEYWORDS_CHARACTER_LIST.Castorice)
