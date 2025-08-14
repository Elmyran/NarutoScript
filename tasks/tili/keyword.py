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
MopUp = StuffState(
    id=2,
    name='MopUp',
    cn='可扫荡',
    cht='可扫荡',
    en='MopUp',
    jp='可扫荡',
    es='MopUp',

)