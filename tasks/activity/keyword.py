from module.ocr.keyword import Keyword
from dataclasses import dataclass
from typing import ClassVar

# 首先定义活动标签页的关键词类
@dataclass
class ActivityTab(Keyword):
    instances: ClassVar = {}


YiLeWaiMaiKeyword = ActivityTab(
    id=0,
    name='YiLeWaiMaiKeyword',
    cn='一乐外卖',
    cht='一樂外賣',
    en='Ichiraku Delivery',
    jp='一楽デリバリー',
    es='Ichiraku a Domicilio'
)

RenZheTeHuiKeyword = ActivityTab(
    id=1,
    name='RenZheTeHuiKeyword',
    cn='忍者特惠',
    cht='忍者特惠',
    en='Ninja Special Offer',
    jp='忍者特別セール',
    es='Oferta Especial Ninja'
)

DingCiKaoRouKeyword = ActivityTab(
    id=2,
    name='DingCiKaoRouKeyword',
    cn='丁次烤肉',
    cht='丁次烤肉',
    en="Choji's BBQ",
    jp='チョウジの焼肉',
    es='Parrillada de Choji'
)

QingSongHaoLiKeyword = ActivityTab(
    id=3,
    name='QingSongHaoLiKeyword',
    cn='轻松好礼',
    cht='輕鬆好禮',
    en='Easy Rewards',
    jp='気楽なギフト',
    es='Regalos Fáciles'
)

MeiYueQianDaoKeyword = ActivityTab(
    id=4,
    name='MeiYueQianDaoKeyword',
    cn='每月签到',
    cht='每月簽到',
    en='Monthly Sign In',
    jp='月次サインイン',
    es='Registro Mensual'
)

JieRiRiLiKeyword = ActivityTab(
    id=5,
    name='JieRiRiLiKeyword',
    cn='节日日历',
    cht='節日曆',
    en='Festival Calendar',
    jp='祭日カレンダー',
    es='Calendario de Festivales'
)
TianTianAiMeiShiKeyword = ActivityTab(
    id=6,
    name='TianTianAiMeiShiKeyword',
    cn='天天爱美食',
    cht='天天爱美食',
    en='Love Food Everyday',
    jp='毎日グルメ',
    es='Amar la Comida Diaria'
)