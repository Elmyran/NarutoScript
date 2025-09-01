from module.ocr.keyword import Keyword
from dataclasses import dataclass
from typing import ClassVar


@dataclass
class TaskTab(Keyword):
    instances: ClassVar = {}

JiFenSaiKeyword = TaskTab(
    id=0,
    name='JiFenSaiKeyword',
    cn='积分赛',
    cht='積分賽',
    en='Score Competition',
    jp='スコア競技',
    es='Competencia de Puntuación'
)

MissionKeyword = TaskTab(
    id=1,
    name='MissionKeyword',
    cn='任务集会所',
    cht='任務集會所',
    en='Mission Hall',
    jp='ミッション集会所',
    es='Salón de Misiones'
)

OrganizationKeyword = TaskTab(
    id=2,
    name='OrganizationKeyword',
    cn='组织',
    cht='組織',
    en='Organization',
    jp='組織',
    es='Organización'
)

LeaderBoardKeyword = TaskTab(
    id=3,
    name='LeaderBoardKeyword',
    cn='排行榜',
    cht='排行榜',
    en='Leaderboard',
    jp='ランキング',
    es='Tabla de Clasificación'
)

DuelKeyword = TaskTab(
    id=4,
    name='DuelKeyword',
    cn='决斗场',
    cht='決鬥場',
    en='Duel Arena',
    jp='決闘場',
    es='Arena de Duelo'
)

FengRaoKeyword = TaskTab(
    id=5,
    name='FengRaoKeyword',
    cn='丰饶之间',
    cht='豐饒之間',
    en='Abundance Chamber',
    jp='豊穣の間',
    es='Cámara de Abundancia'
)

TrailKeyword = TaskTab(
    id=6,
    name='TrailKeyword',
    cn='试炼之地',
    cht='試煉之地',
    en='Trial Grounds',
    jp='試練の地',
    es='Terrenos de Prueba'
)

SquadRaidKeyword = TaskTab(
    id=7,
    name='SquadRaidKeyword',
    cn='小队突袭',
    cht='小隊突襲',
    en='Squad Raid',
    jp='チーム突撃',
    es='Asalto de Escuadrón'
)

RenZheTiaoZhanKeyword = TaskTab(
    id=8,
    name='RenZheTiaoZhanKeyword',
    cn='忍者挑战',
    cht='忍者挑戰',
    en='Ninja Challenge',
    jp='忍者チャレンジ',
    es='Desafío Ninja'
)


