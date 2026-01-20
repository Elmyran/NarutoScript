from module.config.utils import get_server_next_update, nearest_future
from module.logger import logger
from tasks.base.ui import UI


class Duel(UI):
    def run(self):
        delay_time=get_server_next_update(self.config.Scheduler_ServerUpdate)
        logger.hr("Duel Daily",level=1)
        from tasks.duel.duel_daily import DuelDaily
        time=DuelDaily(config=self.config, device=self.device).run()
        delay_time=nearest_future([time, delay_time])
        if self.config.DuelWeekly_DuelWeeklyStatus:
            logger.hr("Duel Weekly",level=1)
            from tasks.duel.duel_weekly import DuelWeekly
            time=DuelWeekly(config=self.config, device=self.device).run()
            delay_time=nearest_future([time, delay_time])
        if self.config.DuelExtended_DuelExtendedStatus:
            logger.hr("Duel Extended",level=1)
            from tasks.duel.extended_play import ExtendedPlay
            time=ExtendedPlay(config=self.config,device=self.device).run()
            delay_time=nearest_future([time, delay_time])
        self.config.task_delay(target=delay_time)
        self.config.task_stop()        
            
            







