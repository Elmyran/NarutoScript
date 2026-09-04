from module.base.button import ClickButton
from module.base.utils.utils import crop
from module.ocr.ocr import Digit, Ocr
from tasks.activity.activity_keyword import MeiYueQianDaoKeyword
from tasks.activity.draglist import ACTIVITY_TAB_LIST
from tasks.base.page import page_activity, page_battle_order, page_cultivation, page_daily, page_duel, page_ji_fen_sai, page_main, page_mi_jing, page_mi_jing_room, page_mission, page_ninjutsu, page_recruit, page_squad, page_squad_help_battle, page_store, page_survival_trail, page_tong_ling, page_trail
from tasks.base.taskui import TaskUI
from tasks.battle_order.assets.assets_battle_order_reward import BATTLE_ORDER_WEEKLY_REWARD_ACTIVITY_POINTS
from tasks.battle_order.assets.assets_battle_order_task import BATTLE_ORDER_TASK_PROGRESS
from tasks.battle_order.ui.switch import BATTLE_ORDER_TAB
from tasks.data_update.assets.assets_data_update import DATA_COINS, DATA_FAME, DATA_RECRUITMENT_TICKETS, DATA_TI_LI
from tasks.duel.assets.assets_duel import DUEL_TASK_PANEL, DUEL_TASK_WINS_NUMBER
from tasks.freebies.assets.assets_freebies_daily_daily import DAILY_PROGRESS
from tasks.freebies.assets.assets_freebies_monthly_sign_in import SIGN_IN_PROGRESS
from tasks.freebies.assets.assets_freebies_yi_le_la_mian import RAMEN_TAB_CHECK
from tasks.ji_fen_sai.assets.assets_ji_fen_sai import ENEMY_1, ENEMY_2, ENEMY_3, ENEMY_4, ENEMY_REFRESH_COUNT, JI_FEN_SAI_FIGHT_COUNT, JI_FEN_SAI_FIGHT_START_BUTTON, TEAM_POWER_SELF
from tasks.mission.assets.assets_mission import TASK_REFRESH_REMAIN_TIMES, TASK_SELECT_REAMIN_TIMES
from tasks.mission.assets.assets_mission_task import TASK_1_JADE, TASK_1_NAME, TASK_1_TIME, TASK_2_JADE, TASK_2_NAME, TASK_2_TIME, TASK_3_JADE, TASK_3_NAME, TASK_3_TIME
from tasks.recruit.assets.assets_recruit import NORMAL_RECRUIT_REMAIN_TIMES, NORMAL_RECRUIT_REMAIN_TIMES_100_BUTTON_STATUS, PREMIUM_RECRUIT_REMAIN_TIMES, PREMIUM_RECRUIT_REMAIN_TIMES_100_BUTTON_STATUS
from tasks.ren_zhe_tiao_zhan.assets.assets_ren_zhe_tiao_zhan import MI_JING_REMAIN_CHALLENGE_TICKET
from tasks.squadraid.assets.assets_squadraid_fight import SQUAD_RAID_TIMES_COUNTER
from tasks.store_purchase.assets.assets_store_purchase_organization_store import MERIT_AREA
from tasks.store_purchase.assets.assets_store_purchase_score_store import SCORE_MEDAL_AREA
from tasks.store_purchase.assets.assets_store_purchase_survival_store import HEAVEN_EARTH_SCROLL_AREA
from tasks.store_purchase.keyword.store_keyword import OrganizationStore, PlayStore, ScoreStore, SurvivalStore
from tasks.store_purchase.ui.store_tab_draglist import StoreTabList, SubsidiaryStoreTabList
from tasks.tili.assets.assets_tili_equipment import EQUIPMENT_CHECK, MAIN_GOTO_EQUIPMENT, MAIN_GOTO_EQUIPMENT_LIST
from tasks.tili.assets.assets_tili_equipment_part import BOOK, CAP, KNIFE, NECK, RING, SHIRT
from tasks.trail.assets.assets_trail_cultivation import CULTIVATION_MOP_UP_REMAIN_TIMES
from tasks.trail.assets.assets_trail_survival import SURVIVAL_MOP_UP_TIMES


class ocr_collect(TaskUI):
    def run(self):
        self.coins_collect()
        self.tili_collect()
        self.gold_collect()
        self.fame_collect()
        self.mission_collect()
        self.recruit_collect()
        self.monthly_sign_collect()
        self.store_collect()
        self.daily_collect()
        self.battle_order_collect()
        self.squad_collect()
        self.survival_collect()
        self.mijing_collect()
        self.duel_collect()
        self.equipment_collect()
        self.jifen_collect()
    
    
    def coins_collect(self):
        self.ui_ensure(page_main)
        coins_ocr=Ocr(DATA_COINS)
        coins=coins_ocr.ocr_single_line(self.device.image)
    def tili_collect(self):
        self.ui_ensure(page_main)
        tili_ocr=Ocr(DATA_TI_LI)
        tili=tili_ocr.ocr_single_line(self.device.image)
    def gold_collect(self):
        self.ui_ensure(page_main)
        gold_ocr=Ocr(DATA_COINS)
        gold=gold_ocr.ocr_single_line(self.device.image)
    def fame_collect(self):
        self.ui_ensure(page_tong_ling)
        fame_ocr=Ocr(DATA_FAME)
        fame=fame_ocr.ocr_single_line(self.device.image)
    def mission_collect(self):
        self.ui_ensure(page_mission)
        ocr=Ocr(TASK_1_JADE)
        jades=[TASK_1_JADE,TASK_2_JADE,TASK_3_JADE]
        jade_images = [crop(self.device.image, jade.area) for jade in jades]
        res = ocr.ocr_multi_lines(jade_images)

        names=[TASK_1_NAME,TASK_2_NAME,TASK_3_NAME]
        name_images = [crop(self.device.image, name.area) for name in names]
        name_res = ocr.ocr_multi_lines(name_images)

        times=[TASK_1_TIME,TASK_2_TIME,TASK_3_TIME]
        time_images = [crop(self.device.image, time.area) for time in times]
        time_res = ocr.ocr_multi_lines(time_images)

        counters=[TASK_REFRESH_REMAIN_TIMES,TASK_SELECT_REAMIN_TIMES]
        counter_images = [crop(self.device.image, counter.area) for counter in counters]
        counter_res = ocr.ocr_multi_lines(counter_images)
    def recruit_collect(self):
        self.ui_ensure(page_recruit)
        ticket_ocr=Ocr(DATA_RECRUITMENT_TICKETS)
        ticket=ticket_ocr.ocr_single_line(self.device.image)

        normal_ocr=Ocr(NORMAL_RECRUIT_REMAIN_TIMES)
        normal=normal_ocr.ocr_single_line(self.device.image)
        # normal_times=[NORMAL_RECRUIT_REMAIN_TIMES,NORMAL_RECRUIT_REMAIN_TIMES_100_BUTTON_STATUS]
        # normal_images = [crop(self.device.image, time.area) for time in normal_times]
        # normal_res = ocr.ocr_multi_lines(normal_images)
        pr_ocr=Ocr(PREMIUM_RECRUIT_REMAIN_TIMES_100_BUTTON_STATUS)
        pr=pr_ocr.ocr_single_line(self.device.image)
        # pr_times=[PREMIUM_RECRUIT_REMAIN_TIMES,PREMIUM_RECRUIT_REMAIN_TIMES_100_BUTTON_STATUS]
        # pr_images = [crop(self.device.image, time.area) for time in pr_times]
        # pr_res = ocr.ocr_multi_lines(pr_images)
    def monthly_sign_collect(self):
        self.ui_ensure(page_activity)
        self.wait_until_stable(  
                    RAMEN_TAB_CHECK,  
                    timer=Timer(0, count=0),  
                    timeout=Timer(1.5, count=5)  
                )   
        ACTIVITY_TAB_LIST.search_rows(main=self,keyword=MeiYueQianDaoKeyword)
        ocr=Ocr(SIGN_IN_PROGRESS)
        res=ocr.ocr_single_line(self.device.image)
    def store_collect(self):
        self.ui_ensure(page_store)
        StoreTabList.search_rows(self,PlayStore)
        SubsidiaryStoreTabList.search_rows(self, OrganizationStore)
        ocr=Ocr(MERIT_AREA)
        merit=ocr.ocr_single_line(self.device.image)

        SubsidiaryStoreTabList.search_rows(self, SurvivalStore)
        ocr=Ocr(HEAVEN_EARTH_SCROLL_AREA)
        heaven_earth_scroll=ocr.ocr_single_line(self.device.image)

        SubsidiaryStoreTabList.search_rows(self, ScoreStore)
        ocr=Ocr(SCORE_MEDAL_AREA)
        score_medal=ocr.ocr_single_line(self.device.image)
    def daily_collect(self):
        self.ui_ensure(page_daily)
        ocr=Ocr(DAILY_PROGRESS)
        progress=ocr.ocr_single_line(self.device.image)
    def battle_order_collect(self):
        self.ui_ensure(page_battle_order)
        BATTLE_ORDER_TAB.set('周任务',main=self)
        ocr=Ocr(BATTLE_ORDER_TASK_PROGRESS)

        BATTLE_ORDER_TAB.set('周活跃',main=self)
        ocr = Digit(BATTLE_ORDER_WEEKLY_REWARD_ACTIVITY_POINTS)
        activity_points=ocr.ocr_single_line(self.device.image)
    def squad_collect(self):
        self.ui_ensure(page_squad)
        ocr=Ocr(SQUAD_RAID_TIMES_COUNTER)
        squadrid=ocr.ocr_single_line(self.device.image)

    def survival_collect(self):
        self.ui_ensure(page_survival_trail)
        ocr=Digit(SURVIVAL_MOP_UP_TIMES)
        survival=ocr.ocr_single_line(self.device.image)

        self.ui_ensure(page_cultivation)
        ocr=Digit(CULTIVATION_MOP_UP_REMAIN_TIMES)
        cultivation=ocr.ocr_single_line(self.device.image)
    
    def mijing_collect(self):
        self.ui_ensure(page_mi_jing_room)
        ocr=Ocr(MI_JING_REMAIN_CHALLENGE_TICKET)
        mijing=ocr.ocr_single_line(self.device.image)
    def duel_collect(self):
        self.ui_ensure(page_ninjutsu)
         #进入任务面板
        for _ in self.loop():
            if self.appear(DUEL_TASK_PANEL):
                break
            if self.appear_then_click(DUEL_TASK,interval=1):
                continue
        ocr=Digit(DUEL_TASK_WINS_NUMBER)
        res=ocr.ocr_single_line(self.device.image)
        for _ in self.loop():
            if self.ui_page_appear(page_ninjutsu):
                break
            if self.appear_then_click(DUEL_TASK_PANEL,interval=2):
                continue
    def jifen_collect(self):
        self.ui_ensure(page_ji_fen_sai)
        ocr=Ocr(JI_FEN_SAI_FIGHT_COUNT)
        counter=ocr.ocr_single_line(self.device.image)


        for _ in self.loop():
            if self.appear(JI_FEN_SAI_FIGHT_PANEL_CHECK):
                break
            if self.match_template_color(JI_FEN_SAI_GOTO_FIGHT_PANEL,interval=1):
                self.device.click(JI_FEN_SAI_GOTO_FIGHT_PANEL)
                continue
        def  recognition(self,image,area):
            
            #power
            power_area=(840,
                        area[1]+67,
                        940,
                        area[3]
                        )
            button=ClickButton(area=power_area,name='POWER')
            ocr=Digit(button)
            power=ocr.ocr_single_line(image)
            #organization
            organization_area=(555,
                            area[1]+34,
                            700,
                            area[3]-40

            )
            button=ClickButton(area=organization_area,name='ORGANIZATION')
            ocr=Ocr(button)
            organization=ocr.ocr_single_line(image)
            #score
            score_area=(630,
                        area[1]+66,
                        690,
                        area[3]
                        )
            button=ClickButton(area=score_area,name='SCORE')
            ocr=Digit(button)
            score=ocr.ocr_single_line(image)
        def enemy_recognition(self):
            enemy_area=[ENEMY_1,ENEMY_2,ENEMY_3,ENEMY_4]
            for area in enemy_area:
                recognition(self.device.image)
        ocr=Ocr(ENEMY_REFRESH_COUNT)
        refresh=ocr.ocr_single_line(self.device.image)
        ocr=Ocr(TEAM_POWER_SELF)
        power_self=ocr.ocr_single_line(self.device.image)    
    def equipment_collect(self):
        self.ui_ensure(page_main)
        for _ in self.loop():
            if self.appear(EQUIPMENT_CHECK):
                self.wait_until_stable(EQUIPMENT_CHECK, timer=Timer(1, count=3))
                break
            if self.appear_then_click(MAIN_GOTO_EQUIPMENT):
                continue
            if self.appear_then_click(MAIN_GOTO_EQUIPMENT_LIST):
                continue

        EQUIPMENT=[KNIFE, RING,CAP,
                      SHIRT, BOOK, NECK]

        for equipment in EQUIPMENT:
            level_button=ClickButton(equipment.button,name=equipment.name)
            ocr=Digit(level_button)
            level=ocr.ocr_single_line(self.device.image)
   
        
        

        
        

    

        

        
