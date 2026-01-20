from dataclasses import dataclass
from typing import ClassVar
from module.ocr.keyword import Keyword

@dataclass(repr=False)
class StuffState(Keyword):
    instances: ClassVar = {}

# 手动创建实例
NotTurnOn = StuffState(
    id=1,
    name='NotTurnOn',
    cn='未开启',
    cht='未开启',
    en='NotTurnOn',
    jp='未开启',
    es='NotTurnOn',

)
SweepKeyword = StuffState(
    id=2,
    name='Sweep',
    cn='可扫荡',
    cht='可扫荡',
    en='Sweep',
    jp='可扫荡',
    es='Sweep',

)
SyntheticKeyword = StuffState(
    id=3,
    name='Synthetic',
    cn='可合成',
    cht='可合成',
    en='Synthetic',
    jp='可合成',
    es='Synthetic',

)

MaterialNotEnoughKeyword = StuffState(
    id=4,
    name='NotEnough',
    cn='还差',
    cht='还差',
    en='NotEnough',
    jp='还差',
    es='NotEnough',

)
EquipKeyword = StuffState(
    id=5,
    name='Equip',
    cn='可装备',
    cht='可装备',
    en='Equip',
    jp='可装备',
    es='Equip',

)