
from dataclasses import dataclass
from typing import ClassVar

from module.ocr.keyword import Keyword


@dataclass
class RecruitKeyword(Keyword):
    instances: ClassVar = {}
AdvancedRecruitment=RecruitKeyword(
    id=1,
    name='AdvancedRecruitment',
    cn='高级招募',
    cht='高級招募',
    en='Advanced Recruitment',
    jp='高級募集',
    es='Reclutamiento Avanzado',
)
JianghuCallOrder=RecruitKeyword(
    id=2,
    name='JianghuCallOrder',
    cn='江湖召集令',
    cht='江湖召集令',
    en='Jianghu Call Order',
    jp='江湖召集令',
    es='Orden de Reunión de Jianghu',
)

LimitedReturn=RecruitKeyword(
    id=3,
    name='LimitedReturn',
    cn='限定返场',
    cht='限定返場',
    en='Limited Return',
    jp='限定復帰',
    es='Regreso Limitado',
)
NormalRecruitment=RecruitKeyword(
    id=4,
    name='NormalRecruitment',
    cn='普通招募',
    cht='普通招募',
    en='Normal Recruitment',
    jp='通常募集',
    es='Reclutamiento Normal',
)
SecretTreasureBox=RecruitKeyword(
    id=5,
    name='SecretTreasureBox',
    cn='绝密宝匣',
    cht='絕密寶匣',
    en='Secret Treasure Box',
    jp='絶密宝箱',
    es='Caja del Tesoro Secreta',
)
WishingTreasureHunt=RecruitKeyword(
    id=6,
    name='WishingTreasureHunt',
    cn='祈愿夺宝',
    cht='祈願奪寶',
    en='Wishing Treasure Hunt',
    jp='祈願奪宝',
    es='Caza del Tesoro Deseado',
)