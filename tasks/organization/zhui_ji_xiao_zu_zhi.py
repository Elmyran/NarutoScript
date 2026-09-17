from module.base.timer import Timer
from module.config.utils import get_server_next_monday_update
from module.exception import GameStuckError
from module.logger import logger
from tasks.base.page import page_organization_panel
from tasks.base.taskui import TaskUI
from tasks.organization.assets.assets_organization_akatsuki import *
from tasks.organization.assets.assets_organization_pray import *
from module.base.utils import random_rectangle_point
class ZhuiJiXiaoZuZhi(TaskUI):
    def run(self):
        if self.handle_pursue_akatsuki():
            logger.info('追击晓组织完成,任务推迟至下周一')
            monday = get_server_next_monday_update(self.config.Scheduler_ServerUpdate)
            self.config.task_delay(target=monday)

        else:
            logger.info('存在未达成关卡,任务推迟至第二天')
            self.config.task_delay(server_update=True)
        self.config.task_stop()

   
        
       
    def handle_pursue_akatsuki(self):
        self.device.click_record_clear()
        self.ui_ensure(page_organization_panel)
        self._enter_akatsuki_page()
        return self._reward_claim()
       

  
    def _enter_akatsuki_page(self):
        self.ui_click(click_button=ORGANIZATION_PLAY_PANEL,check_button=ORGANIZATION_GOTO_PRAY)
        self.ui_click(click_button=ORGANIZATION_GOTO_AKATSUKI,check_button=AKATSUKI_CHECK)

    def _reward_claim(self):
        if self.appear(AKATSUKI_DONE):
            self.ui_click(click_button=AKATSUKI_GOTO_REWARD,check_button=AKATSUKI_REWARD_CHECK,retry_wait=2)
            self.device.click_record_clear()
            for _ in self.loop():
                list=REWARD_HAVE_CLAIMED.match_multi_template(self.device.image,direct_match=True)
                if len(list)==5:
                    break
                if self.appear_then_click(REWARD_CLAIM_ALL,interval=0):
                    continue
                if self.match_template(REWARD_CLAIM_BUTTON,interval=1):
                    self.device.click(REWARD_CLAIM_BUTTON)
                    continue
            start=random_rectangle_point(REWARD_DRAG_START.area)
            end=random_rectangle_point(REWARD_DRAG_END.area)
            self.device.swipe(start,end)
            for _ in self.loop():
                list=REWARD_HAVE_CLAIMED.match_multi_template(self.device.image,direct_match=True)
                if len(list)==5:
                    break
                if self.appear_then_click(REWARD_CLAIM_ALL,interval=0):
                    continue
                if self.match_template(REWARD_CLAIM_BUTTON,interval=1):
                    self.device.click(REWARD_CLAIM_BUTTON)
                    continue
            return True
        else:
            self.ui_click(click_button=AKATSUKI_GOTO_REWARD,check_button=AKATSUKI_REWARD_CHECK,retry_wait=2)
            time=Timer(3, count=5).start()
            for _ in self.loop():
                if time.reached():
                    break
                if self.appear_then_click(REWARD_CLAIM_ALL,interval=0):
                    continue
                if self.match_template(REWARD_CLAIM_BUTTON,interval=1):
                    self.device.click(REWARD_CLAIM_BUTTON)
                    continue
            return False


            
            
    
