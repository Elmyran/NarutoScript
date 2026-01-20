from module.ocr.keyword import Keyword
from dataclasses import dataclass
from typing import ClassVar




@dataclass
class TaskTab(Keyword):
    instances: ClassVar = {}

TalentKeyword = TaskTab(
    id=0,
    name='TalentKeyword',
    cn='天赋',
    cht='天賦',
    en='Talent',
    jp='天賦',
    es='Talento'
)
EquipmentKeyword = TaskTab(
    id=1,
    name='EquipmentKeyword',
    cn='装备',
    cht='裝備',
    en='Equipment',
    jp='装備',
    es='Equipamiento'
)
RaidSweepKeyword = TaskTab(
    id=2,
    name='RaidSweepKeyword',
    cn='副本扫荡',
    cht='副本掃蕩',
    en='Raid Sweep',
    jp='レイド掃討',
    es='Barrido de Mazmorra'
)
NinjaRecruitKeyword = TaskTab(
    id=3,
    name='NinjaRecruitKeyword',
    cn='忍者招募',
    cht='忍者招募',
    en='Ninja Recruitment',
    jp='忍者募集',
    es='Reclutamiento de Ninjas'
)
RewardCenterKeyword = TaskTab(
    id=4,
    name='RewardCenterKeyword',
    cn='奖励中心',
    cht='獎勵中心',
    en='Reward Center',
    jp='報酬センター',
    es='Centro de Recompensas'
)
EliteRaidKeyword = TaskTab(
    id=5,
    name='EliteRaidKeyword',
    cn='精英副本',
    cht='精英副本',
    en='Elite Raid',
    jp='エリートレイド',
    es='Mazmorra Élite'
)
WealthSummonKeyword = TaskTab(
    id=6,
    name='WealthSummonKeyword',
    cn='招财',
    cht='招財',
    en='Wealth Summon',
    jp='財宝召喚',
    es='Invocación de Riqueza'
)
FriendSystemKeyword = TaskTab(
    id=7,
    name='FriendSystemKeyword',
    cn='好友系统',
    cht='好友系統',
    en='Friend System',
    jp='友達システム',
    es='Sistema de Amigos'
)
LeaderBoardKeyword = TaskTab(
    id=8,
    name='LeaderBoardKeyword',
    cn='排行榜',
    cht='排行榜',
    en='LeaderBoard',
    jp='ランキング',
    es='Lista de Clasificación'
)
BuyStaminaKeyword = TaskTab(
    id=9,
    name='BuyStaminaKeyword',
    cn='购买体力',
    cht='購買體力',
    en='Buy Stamina',
    jp='スタミナ購入',
    es='Comprar Energía'
)
StoreKeyword = TaskTab(
    id=10,
    name='StoreKeyword',
    cn='商店',
    cht='商店',
    en='Store',
    jp='ショップ',
    es='Tienda'
)
NinjaBattleKeyword = TaskTab(
    id=11,
    name='NinjaBattleKeyword',
    cn='忍术对战',
    cht='忍術對戰',
    en='Ninja Battle',
    jp='忍術対戦',
    es='Batalla Ninja'
)
RankMatchKeyword = TaskTab(
    id=12,
    name='RankMatchKeyword',
    cn='段位赛',
    cht='段位賽',
    en='Rank Match',
    jp='ランクマッチ',
    es='Partida de Rango'
)
MagatamaKeyword = TaskTab(
    id=13,
    name='MagatamaKeyword',
    cn='勾玉',
    cht='勾玉',
    en='Magatama',
    jp='マガタマ',
    es='Magatama'
)
DailyTaskKeyword = TaskTab(
    id=14,
    name='DailyTaskKeyword',
    cn='每日任务',
    cht='每日任務',
    en='Daily Task',
    jp='デイリーミッション',
    es='Tarea Diaria'
)
FengRaoKeyword = TaskTab(
    id=15,
    name='FengRaoKeyword',
    cn='丰饶之间',
    cht='豐饒之間',
    en='Abundant',
    jp='豊穣の間',
    es='Abundante'
)
CultivationPathKeyword = TaskTab(
    id=16,
    name='CultivationPathKeyword',
    cn='修行之路',
    cht='修行之路',
    en='Cultivation Path',
    jp='修行情道',
    es='Camino de Cultivo'
)
OrganizationKeyword = TaskTab(
    id=17,
    name='OrganizationKeyword',
    cn='组织',
    cht='組織',
    en='Organization',
    jp='組織',
    es='Organización'
)
OrganizationTournamentKeyword = TaskTab(
    id=18,
    name='OrganizationTournamentKeyword',
    cn='组织争霸赛',
    cht='組織爭霸賽',
    en='Organization Tournament',
    jp='組織覇権戦',
    es='Torneo de Organizaciones'
)
DressUpHallKeyword = TaskTab(
    id=19,
    name='DressUpHallKeyword',
    cn='装扮大厅',
    cht='装扮大廳',
    en='Dress Up Hall',
    jp='ドレスアップホール',
    es='Salón de Disfraces'
)
ScoreCompetitionKeyword = TaskTab(
    id=20,
    name='ScoreCompetitionKeyword',
    cn='积分赛',
    cht='積分賽',
    en='Score Competition',
    jp='スコア競技',
    es='Competencia de Puntuación'
)
SquadRaidKeyword = TaskTab(
    id=21,
    name='SquadRaidKeyword',
    cn='小队突袭',
    cht='小隊突襲',
    en='Squad Raid',
    jp='小隊突撃',
    es='Incursión de Escuadra'
)
SecretScrollKeyword = TaskTab(
    id=22,
    name='SecretScrollKeyword',
    cn='秘卷',
    cht='秘卷',
    en='Secret Scroll',
    jp='秘伝の巻物',
    es='Pergamino Secreto'
)
SummoningBeastKeyword = TaskTab(
    id=23,
    name='SummoningBeastKeyword',
    cn='通灵兽',
    cht='通靈獸',
    en='Summoning Beast',
    jp='召喚獣',
    es='Bestia Invocada'
)
TitleSystemKeyword = TaskTab(
    id=24,
    name='TitleSystemKeyword',
    cn='称号系统',
    cht='稱號系統',
    en='Title System',
    jp='称号システム',
    es='Sistema de Títulos'
)
AvatarFrameKeyword = TaskTab(
    id=25,
    name='AvatarFrameKeyword',
    cn='头像框',
    cht='頭像框',
    en='Avatar Frame',
    jp='アバターフレーム',
    es='Marco de Avatar'
)
StoryStageKeyword = TaskTab(
    id=26,
    name='StoryStageKeyword',
    cn='剧情关卡',
    cht='劇情關卡',
    en='Story Stage',
    jp='ストーリーステージ',
    es='Etapa de Historia'
)
SurvivalChallengeKeyword = TaskTab(
    id=27,
    name='SurvivalChallengeKeyword',
    cn='生存挑战',
    cht='生存挑戰',
    en='Survival Challenge',
    jp='サバイバルチャレンジ',
    es='Desafío de Supervivencia'
)
MissionKeyword = TaskTab(
    id=28,
    name='MissionKeyword',
    cn='任务集会所',
    cht='任務集会所',
    en='Mission',
    jp='ミッション集会所',
    es='Misión'
)
NinjaChronicleKeyword = TaskTab(
    id=29,
    name='NinjaChronicleKeyword',
    cn='忍传',
    cht='忍傳',
    en='Ninja Chronicle',
    jp='忍伝',
    es='Crónica Ninja'
)
OrnamentKeyword = TaskTab(
    id=30,
    name='OrnamentKeyword',
    cn='饰品',
    cht='飾品',
    en='Ornament',
    jp='装飾品',
    es='Adorno'
)
SecretRealmExplorationKeyword = TaskTab(
    id=31,
    name='SecretRealmExplorationKeyword',
    cn='秘境探险',
    cht='秘境探險',
    en='Secret Realm Exploration',
    jp='秘境探検',
    es='Exploración del Reino Secreto'
)
ArtifactKeyword = TaskTab(
    id=32,
    name='ArtifactKeyword',
    cn='神器',
    cht='神器',
    en='Artifact',
    jp='神器',
    es='Artefacto'
)
MagatamaRefinementKeyword = TaskTab(
    id=33,
    name='MagatamaRefinementKeyword',
    cn='勾玉精炼',
    cht='勾玉精煉',
    en='Magatama Refinement',
    jp='マガタマ精錬',
    es='Refinamiento de Magatama'
)
NinjaTournamentKeyword = TaskTab(
    id=34,
    name='NinjaTournamentKeyword',
    cn='忍者大赛',
    cht='忍者大賽',
    en='Ninja Tournament',
    jp='忍者大会',
    es='Torneo de Ninjas'
)
NinjaToolKeyword = TaskTab(
    id=35,
    name='NinjaToolKeyword',
    cn='忍具',
    cht='忍具',
    en='Ninja Tool',
    jp='忍具',
    es='Herramienta Ninja'
)
NinjaToolMuseumKeyword = TaskTab(
    id=36,
    name='NinjaToolMuseumKeyword',
    cn='忍具藏馆',
    cht='忍具藏館',
    en='Ninja Tool Museum',
    jp='忍具博物館',
    es='Museo de Herramientas Ninja'
)
ShuraRaidKeyword = TaskTab(
    id=37,
    name='ShuraRaidKeyword',
    cn='修罗副本',
    cht='修羅副本',
    en='Shura Raid',
    jp='修羅レイド',
    es='Mazmorra Shura'
)
ShuraTalentKeyword = TaskTab(
    id=38,
    name='ShuraTalentKeyword',
    cn='修罗天赋',
    cht='修羅天賦',
    en='Shura Talent',
    jp='修羅の天賦',
    es='Talento Shura'
)
TeamRaidKeyword = TaskTab(
    id=39,
    name='TeamRaidKeyword',
    cn='团队副本',
    cht='團隊副本',
    en='Team Raid',
    jp='チームレイド',
    es='Mazmorra de Equipo'
)
SummoningEvolutionKeyword = TaskTab(
    id=40,
    name='SummoningEvolutionKeyword',
    cn='通灵进阶',
    cht='通靈進階',
    en='Summoning Evolution',
    jp='召喚進化',
    es='Evolución de Invocación'
)
RuneKeyword = TaskTab(
    id=41,
    name='RuneKeyword',
    cn='符文',
    cht='符文',
    en='Rune',
    jp='ルーン',
    es='Runa'
)

NinjaChronicleBondKeyword = TaskTab(
    id=42,
    name='NinjaChronicleBondKeyword',
    cn='忍传羁绊',
    cht='忍傳羈絆',
    en='Ninja Chronicle Bond',
    jp='忍伝の絆',
    es='Vínculo de Crónica Ninja'
)



