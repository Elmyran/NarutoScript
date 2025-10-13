from module.ocr.keyword import Keyword
from dataclasses import dataclass
from typing import ClassVar

@dataclass
class FortressNameKeyword(Keyword):
    instances: ClassVar = {}
    area_pos: tuple = None
    level: str = None

# 各要塞名称实例，包含坐标和等级信息
IronFortressKeyword = FortressNameKeyword(
    id=0,
    name='IronFortressKeyword',
    cn='铁之要塞',
    cht='鐵之要塞',
    en='Iron Fortress',
    jp='鉄の要塞',
    es='Fortaleza de Hierro',
    area_pos=(830, 100),
    level='Low'
)

FieldFortressKeyword = FortressNameKeyword(
    id=1,
    name='FieldFortressKeyword',
    cn='田之要塞',
    cht='田之要塞',
    en='Field Fortress',
    jp='田の要塞',
    es='Fortaleza de Campo',
    area_pos=(1180, 236),
    level='Low'
)

EarthFortressKeyword = FortressNameKeyword(
    id=2,
    name='EarthFortressKeyword',
    cn='土之要塞',
    cht='土之要塞',
    en='Earth Fortress',
    jp='土の要塞',
    es='Fortaleza de Tierra',
    area_pos=(900, 460),
    level='Medium'
)

BearFortressKeyword = FortressNameKeyword(
    id=3,
    name='BearFortressKeyword',
    cn='熊之要塞',
    cht='熊之要塞',
    en='Bear Fortress',
    jp='熊の要塞',
    es='Fortaleza de Oso',
    area_pos=(408, 495),
    level='Low'
)

HotSpringFortressKeyword = FortressNameKeyword(
    id=4,
    name='HotSpringFortressKeyword',
    cn='汤之要塞',
    cht='湯之要塞',
    en='Hot Spring Fortress',
    jp='湯の要塞',
    es='Fortaleza de Aguas Termales',
    area_pos=(1584, 197),
    level='Low'
)

WhirlpoolFortressKeyword = FortressNameKeyword(
    id=5,
    name='WhirlpoolFortressKeyword',
    cn='涡之要塞',
    cht='渦之要塞',
    en='Whirlpool Fortress',
    jp='渦の要塞',
    es='Fortaleza de Remolino',
    area_pos=(1965, 431),
    level='Low'
)

FrostFortressKeyword = FortressNameKeyword(
    id=6,
    name='FrostFortressKeyword',
    cn='霜之要塞',
    cht='霜之要塞',
    en='Frost Fortress',
    jp='霜の要塞',
    es='Fortaleza de Escarcha',
    area_pos=(2163, 465),
    level='Low'
)

WaterFortressKeyword = FortressNameKeyword(
    id=7,
    name='WaterFortressKeyword',
    cn='水之要塞',
    cht='水之要塞',
    en='Water Fortress',
    jp='水の要塞',
    es='Fortaleza de Agua',
    area_pos=(1670, 521),
    level='Medium'
)

FireFortressKeyword = FortressNameKeyword(
    id=8,
    name='FireFortressKeyword',
    cn='火之要塞',
    cht='火之要塞',
    en='Fire Fortress',
    jp='火の要塞',
    es='Fortaleza de Fuego',
    area_pos=(1221, 529),
    level='High'
)

RainFortressKeyword = FortressNameKeyword(
    id=9,
    name='RainFortressKeyword',
    cn='雨之要塞',
    cht='雨之要塞',
    en='Rain Fortress',
    jp='雨の要塞',
    es='Fortaleza de Lluvia',
    area_pos=(322, 950),
    level='Low'
)

GrassFortressKeyword = FortressNameKeyword(
    id=10,
    name='GrassFortressKeyword',
    cn='草之要塞',
    cht='草之要塞',
    en='Grass Fortress',
    jp='草の要塞',
    es='Fortaleza de Hierba',
    area_pos=(289, 783),
    level='Low'
)

RiverFortressKeyword = FortressNameKeyword(
    id=11,
    name='RiverFortressKeyword',
    cn='川之要塞',
    cht='川之要塞',
    en='River Fortress',
    jp='川の要塞',
    es='Fortaleza de Río',
    area_pos=(891, 972),
    level='Low'
)

LightningFortressKeyword = FortressNameKeyword(
    id=12,
    name='LightningFortressKeyword',
    cn='雷之要塞',
    cht='雷之要塞',
    en='Lightning Fortress',
    jp='雷の要塞',
    es='Fortaleza de Relámpago',
    area_pos=(1118, 739),
    level='Medium'
)

WindFortressKeyword = FortressNameKeyword(
    id=13,
    name='WindFortressKeyword',
    cn='风之要塞',
    cht='風之要塞',
    en='Wind Fortress',
    jp='風の要塞',
    es='Fortaleza de Viento',
    area_pos=(741, 668),
    level='Medium'
)

OceanFortressKeyword = FortressNameKeyword(
    id=14,
    name='OceanFortressKeyword',
    cn='海之要塞',
    cht='海之要塞',
    en='Ocean Fortress',
    jp='海の要塞',
    es='Fortaleza de Océano',
    area_pos=(582, 1010),
    level='Low'
)

WaterfallFortressKeyword = FortressNameKeyword(
    id=15,
    name='WaterfallFortressKeyword',
    cn='泷之要塞',
    cht='瀧之要塞',
    en='Waterfall Fortress',
    jp='瀧の要塞',
    es='Fortaleza de Cascada',
    area_pos=(1492, 978),
    level='Low'
)

CloudFortressKeyword = FortressNameKeyword(
    id=16,
    name='CloudFortressKeyword',
    cn='云之要塞',
    cht='雲之要塞',
    en='Cloud Fortress',
    jp='雲の要塞',
    es='Fortaleza de Nube',
    area_pos=(1788, 812),
    level='Low'
)

BirdFortressKeyword = FortressNameKeyword(
    id=17,
    name='BirdFortressKeyword',
    cn='鸟之要塞',
    cht='鳥之要塞',
    en='Bird Fortress',
    jp='鳥の要塞',
    es='Fortaleza de Pájaro',
    area_pos=(1984, 856),
    level='Low'
)