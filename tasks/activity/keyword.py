from module.logger import logger
from module.ui.draggable_list import DraggableList
from module.ocr.ocr import Ocr
from module.ocr.keyword import Keyword
from dataclasses import dataclass
from typing import ClassVar

from tasks.activity.assets.assets_activity import ACTIVITY_LIST_AREA
from tasks.activity.assets.assets_activity_ui import MONTHLY_SIGN_IN_CHECK


# 首先定义活动标签页的关键词类
@dataclass
class ActivityTab(Keyword):
    instances: ClassVar = {}
IchirakuRamenKeyword = ActivityTab(
    id=0,
    name='IchirakuRamen',
    cn='一乐外卖',          # 简体中文
    cht='一樂外賣',         # 繁體中文
    en='Ichiraku Delivery', # 英文
    jp='一楽デリバリー',      # 日文
    es='Ichiraku a Domicilio' # 西班牙文
)
NinjaDiscountKeyword = ActivityTab(
    id=1,
    name='NinjaDiscount',
    cn='忍者特惠',                # 简体中文
    cht='忍者特惠',               # 繁體中文
    en='Ninja Special Offer',     # 英文
    jp='忍者特別セール',           # 日文
    es='Oferta Especial Ninja'    # 西班牙文
)
ChojiBBQKeyword = ActivityTab(
    id=2,
    name='ChojiBBQ',
    cn='丁次烤肉',              # 简体中文
    cht='丁次烤肉',             # 繁體中文（台湾/港澳常用写法不变）
    en="Choji's BBQ",           # 英文
    jp='チョウジの焼肉',          # 日文
    es='Parrillada de Choji'    # 西班牙文
)
EasyGiftKeyword = ActivityTab(
    id=3,
    name='EasyGift',
    cn='轻松好礼',              # 简体中文
    cht='輕鬆好禮',             # 繁體中文
    en='Easy Rewards',          # 英文
    jp='気楽なギフト',           # 日文
    es='Regalos Fáciles'        # 西班牙文
)
# 定义每月签到关键词
MonthlySignInKeyword = ActivityTab(
    id=4,
    name='MonthlySignIn',
    cn='每月签到',
    cht='每月簽到',
    en='Monthly Sign In',
    jp='月次サインイン',
    es='Registro Mensual'
)
FestivalCalendarKeyword = ActivityTab(
    id=5,
    name='FestivalCalendar',
    cn='节日日历',            # 简体中文
    cht='節日曆',             # 繁體中文
    en='Festival Calendar',   # 英文
    jp='祭日カレンダー',       # 日文
    es='Calendario de Festivales' # 西班牙文
)

