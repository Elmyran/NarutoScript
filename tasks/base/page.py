import traceback

from tasks.activity.assets.assets_activity_diao_yu_da_shi import *
from tasks.base.assets.assets_base_page import *

from tasks.daily.assets.assets_daily_weekly import *
from tasks.duel.assets.assets_duel import *
from tasks.duel.assets.assets_duel_ninjutsu import *
from tasks.information_club.assets.assets_information_club import *
from tasks.leaderboard.assets.assets_leaderboard import *
from tasks.organization.assets.assets_organization_akatsuki import AKATSUKI_CHECK
from tasks.organization.assets.assets_organization_battlefield import *
from tasks.organization.assets.assets_organization_fortress import *
from tasks.organization.assets.assets_organization_pan_ren import PAN_REN_CHECK
from tasks.organization.assets.assets_organization_pray import *
from tasks.organization.assets.assets_organization_replacement import *
from tasks.organization.assets.assets_organization_boxclaim import *
from tasks.recruit.assets.assets_recruit import *
from tasks.ren_zhe_tiao_zhan.assets.assets_ren_zhe_tiao_zhan import *

from tasks.tili.assets.assets_tili_dungeon import *
from tasks.tili.assets.assets_tili_equipment import *
from tasks.trail.assets.assets_trail import *
from tasks.trail.assets.assets_trail_survival import *
from tasks.trail.assets.assets_trail_cultivation import *
from tasks.zhaocai.assets.assets_zhaocai import *
from tasks.fengrao.assets.assets_fengrao import *
from tasks.squadraid.assets.assets_squadraid_fight import *
from tasks.squadraid.assets.assets_squadraid_benefit import *
from tasks.mission.assets.assets_mission import *
from tasks.freebies.assets.assets_freebies_mail import *
from tasks.freebies.assets.assets_freebies_dailyshare import *
from tasks.freebies.assets.assets_freebies_friendgifts import *
from tasks.login.assets.assets_login import *
from tasks.activity.assets.assets_activity import *
from tasks.base.assets.assets_base_page import *

class Page:
    # Key: str, page name like "page_main"
    # Value: Page, page instance
    all_pages = {}

    @classmethod
    def clear_connection(cls):
        for page in cls.all_pages.values():
            page.parent = None

    @classmethod
    def init_connection(cls, destination):
        """
        Initialize an A* path finding among pages.

        Args:
            destination (Page):
        """
        cls.clear_connection()

        visited = [destination]
        visited = set(visited)
        while 1:
            new = visited.copy()
            for page in visited:
                for link in cls.iter_pages():
                    if link in visited:
                        continue
                    if page in link.links:
                        link.parent = page
                        new.add(link)
            if len(new) == len(visited):
                break
            visited = new

    @classmethod
    def iter_pages(cls):
        return cls.all_pages.values()

    @classmethod
    def iter_check_buttons(cls):
        for page in cls.all_pages.values():
            yield page.check_button

    def __init__(self, check_button):
        self.check_button = check_button
        self.links = {}
        (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
        self.name = text[:text.find('=')].strip()
        self.parent = None
        Page.all_pages[self.name] = self

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name

    def link(self, button, destination):
        self.links[destination] = button

#Main_Page
page_main=Page(MAIN_GOTO_CHARACTER)
#Mail
page_mail=Page(MAIL_CHECK)
page_mail.link(MAIL_EXIT,destination=page_main)
page_main.link(MAIN_GOTO_MAIL,destination=page_mail)
#Mission
page_mission=Page(MISSION_CHECK)
page_main.link(MISSION_RED_DOT,destination=page_mission)
page_mission.link(MISSION_EXIT,destination=page_main)
#DailyShare
page_panel=Page(PANEL_CHECK)
page_main.link(MAIN_GOTO_PANEL,destination=page_panel)
page_panel.link(PANEL_GOTO_MAIN,destination=page_main)
#FriendGifts
page_friend_panel=Page(FRIEND_PANEL_CHECK)
page_main.link(MAIN_GOTO_FRIEND_PANEL,destination=page_friend_panel)
page_friend_panel.link(FRIEND_PANEL_GOTO_MAIN,destination=page_main)
#ZhaoCai
page_zhaocai=Page(ZHAO_CAI_CHECK)
page_main.link(MAIN_GOTO_ZHAO_CAI,destination=page_zhaocai)
page_zhaocai.link(ZHAO_CAI_GOTO_MAIN,destination=page_main)
#Organization
page_organization_panel=Page(ORGANIZATION_PANEL)
page_organization=Page(ORGANIZATION)
page_pray=Page(ORGANIZATION_PRAY_CHECK)
page_pray.link(PRAY_EXIT,destination=page_organization)
page_organization.link(ORGANIZATION_EXIT,destination=page_main)
#Akatsuki
page_akatsuki=Page(AKATSUKI_CHECK)
page_akatsuki.link(CLOSE,destination=page_organization)

#Fortress
# page_fortress_type=Page(FORTRESS_LOCAL_SELECT)
# page_fortress_select=Page(FORTRESS_SELECT)
# page_fortress_page=Page(FORTRESS_PAGE)
# page_organization.link(ORGANIZATION_GOTO_FORTRESS,destination=page_fortress_type)
# page_fortress_type.link(FORTRESS_LOCAL_SELECT,destination=page_fortress_select)
# page_fortress_page.link(FORTRESS_EXIT,destination=page_fortress_select)
# page_fortress_select.link(CLOSE,destination=page_organization)
#BattleField
page_battle_field_select=Page(BATTLE_FIELD_SELECT_CHECK)
page_organization.link(ORGANIZATION_GOTO_BATTLE_FIELD,destination=page_battle_field_select)
page_battle_field_tian=Page(BATTLE_FIELD_TIAN_CHECK)
# page_battle_field_di=Page(BATTLE_FIELD_DI_CHECK)
#PanRen
page_pan_ren=Page(PAN_REN_CHECK)
page_pan_ren.link(CLOSE,destination=page_organization)
#DailyReward
page_daily=Page(DAILY_CHECK)
page_main.link(MAIN_GOTO_DAILY,destination=page_daily)
page_daily.link(CLOSE,destination=page_main)

#SquadRaid
page_squad=Page(SQUAD_RAID_CHECK)
page_main.link(MAIN_GOTO_SQUAD_RAID,destination=page_squad)
page_squad_help_battle=Page(HELP_BATTLE_GOTO_MINE)
page_squad_help_battle_mine=Page(HELP_BATTLE_MINE_CHECK)
page_squad.link(SQUAD_GOTO_HELP_BATTLE,destination=page_squad_help_battle)
page_squad_help_battle.link(HELP_BATTLE_GOTO_MINE,destination=page_squad_help_battle_mine)
page_squad_help_battle_mine.link(HELP_BATTLE_MINE_EXIT,destination=page_squad_help_battle)
page_squad_help_battle.link(SQUAD_RAID_EXIT,destination=page_squad)
page_squad.link(SQUAD_RAID_EXIT,destination=page_main)
#FengRao
page_feng_rao=Page(FENG_RAO_CHECK)
page_main.link(MAIN_GOTO_FENG_RAO,destination=page_feng_rao)
page_feng_rao.link(FENG_RAO_EXIT,destination=page_main)
#SurvivalTrail
page_trail=Page(TRAIL_SURVIVAL_CHECK)
page_survival_trail=Page(SURVIVAL_PAGE_CHECK)
page_trail.link(TRAIL_SURVIVAL_CHECK,destination=page_survival_trail)
page_survival_trail.link(SURVIVAL_EXIT,destination=page_trail)
page_trail.link(TRAIL_EXIT,destination=page_main)
#CultivationRoad
page_cultivation=Page(CULTIVATION_PAGE_CHECK)
page_cultivation_box=Page(CULTIVATION_BOX_CHECK)
page_trail.link(TRAIL_CULTIVATION_CHECK,destination=page_cultivation)
page_cultivation_box.link(CULTIVATION_EXIT,page_cultivation)
page_cultivation.link(CULTIVATION_BOX,destination=page_cultivation_box)

#Equipment
page_equipment=Page(EQUIPMENT_CHECK)
page_equipment.link(EQUIPMENT_EXIT,destination=page_main)
#Dungeon
page_dungeon=Page(SWITCH_TO_DUNGEON)
page_elite_dungeon=Page(CONVENIENT_SWEEP)
page_dungeon_sweep=Page(SWEEP_BUTTON)
page_dungeon_sweep.link(DUNGEON_EXIT,destination=page_elite_dungeon)
page_elite_dungeon.link(DUNGEON_EXIT,destination=page_main)
page_dungeon.link(SWITCH_TO_DUNGEON,destination=page_elite_dungeon)
page_dungeon.link(DUNGEON_EXIT,destination=page_main)
page_main.link(MAIN_GOTO_DUNGEON,destination=page_dungeon)
#DUEL
page_duel=Page(DUEL_CHECK)
page_ninjutsu=Page(DUEL_START_FIGHT)
page_task_panel=Page(DUEL_TASK_PANEL)
page_main.link(MAIN_GOTO_DUEL,destination=page_duel)
page_duel.link(DUEL_CHECK,destination=page_ninjutsu)
page_ninjutsu.link(DUEL_TASK,destination=page_task_panel)
page_task_panel.link(DUEL_TASK_PANEL,destination=page_ninjutsu)
page_ninjutsu.link(NINJUTSU_EXIT,destination=page_duel)
page_duel.link(DUEL_EXIT,destination=page_main)
#LeaderBoard
page_leader_board=Page(LEADER_BOARD_CHECK)
page_main.link(MAIN_GOTO_LEADER_BOARD,destination=page_leader_board)
page_leader_board.link(LEADER_BOARD_EXIT,destination=page_main)
#InformationClub
page_information_club=Page(CLUB_GOTO_WELFARE_STATION)
page_welfare_station=Page(WELFARE_STATION_CHECK)
page_main.link(MAIN_GOTO_CLUB,destination=page_information_club)
page_information_club.link(CLUB_GOTO_WELFARE_STATION,destination=page_welfare_station)
page_information_club.link(WELFARE_STATION_EXIT,destination=page_main)
page_welfare_station.link(WELFARE_STATION_EXIT,destination=page_main)
#Recruit
page_recruit=Page(RECRUIT_CHECK)
page_main.link(MAIN_GOTO_RECRUIT,destination=page_recruit)
page_recruit.link(RECRUIT_EXIT,destination=page_main)
#BattleOrder
page_battle_order=Page(BATTLE_ORDER_CHECK)
page_main.link(MAIN_GOTO_BATTLE_ORDER,destination=page_battle_order)
page_battle_order.link(CLOSE,destination=page_main)
page_battle_order_rank=Page(BATTLE_ORDER_RANK_CHECK)
page_battle_order_rank.link(CLOSE,destination=page_battle_order)
page_battle_order.link(BATTLE_ORDER_GOTO_RANK,destination=page_battle_order_rank)
#MiJing
page_ren_zhe_tiao_zhan=Page(REN_ZHE_TIAO_ZHAN_CHECK)
page_mi_jing=Page(MI_JING_CHECK)
page_mi_jing_room=Page(MI_JING_ROOM_CHECK)
page_ren_zhe_tiao_zhan.link(REN_ZHE_TIAO_ZHAN_GOTO_MI_JING,destination=page_mi_jing)
page_mi_jing.link(MI_JING_CREATE_ROOM,destination=page_mi_jing_room)
page_mi_jing_room.link(CLOSE,destination=page_mi_jing)
page_mi_jing.link(CLOSE,destination=page_ren_zhe_tiao_zhan)
page_ren_zhe_tiao_zhan.link(REN_ZHE_TIAO_ZHAN_CLOSE,destination=page_main)


#Activity
page_activity=Page(ACTIVITY_CHECK)
page_main.link(MAIN_GOTO_ACTIVITY,destination=page_activity)
page_activity.link(ACTIVITY_EXIT,destination=page_main)
#钓鱼大师
page_diao_yu_da_shi=Page(DIAO_YU_DA_SHI_CHECK)
page_main.link(MAIN_GOTO_DIAO_YU_DA_SHI,destination=page_diao_yu_da_shi)
page_diao_yu_da_shi.link(CLOSE,destination=page_main)
page_diao_yu=Page(DIAO_YU_CHECK)
page_diao_yu.link(CLOSE,destination=page_diao_yu_da_shi)


