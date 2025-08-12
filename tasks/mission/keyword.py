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