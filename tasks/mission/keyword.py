from dataclasses import dataclass
from typing import ClassVar
from module.ocr.keyword import Keyword

@dataclass(repr=False)
class MissionState(Keyword):
    instances: ClassVar = {}

# 手动创建实例
Claimable = MissionState(
    id=1,
    name='Claimable',
    cn='可领取',
    cht='可領取',
    en='Claimable',
    jp='受取可能',
    es='Reclamable',
)
Acceptable = MissionState(
    id=2,
    name='Acceptable',
    cn='接取',
    cht='接取',
    en='Accept',
    jp='受け取る',
    es='Aceptar',
)
TaskTime = MissionState(
    id=3,
    name='TaskTime',
    cn='时间',
    cht='接取',
    en='Accept',
    jp='受け取る',
    es='Aceptar',
)