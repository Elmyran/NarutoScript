
from dev_tools.keywords.base import UI_LANGUAGES
from dataclasses import dataclass
from module.ocr.keyword import Keyword
from typing import ClassVar

@dataclass(repr=False)  
class ScoreStoreItem(Keyword):  
    instances: ClassVar = {}  
    @property  
    def item_name(self):  
        return [self.__getattribute__(f"{server}_parsed")  
                for server in UI_LANGUAGES if hasattr(self, f"{server}_parsed")]
ScoreStoreChest = ScoreStoreItem(
    id=1,
    name='ScoreStoreChest',
    cn='积分赛宝箱',
    cht='積分賽寶箱',
    en='Score Match Chest',
    jp='スコアマッチの宝箱',
    es='Cofre de Partida por Puntos',
)
GhostSharkFragment = ScoreStoreItem(
    id=2,
    name='GhostSharkFragment',
    cn='鬼鲛碎片',
    cht='鬼鯊碎片',
    en='Ghost Shark Fragment',
    jp='鬼鮫の欠片',
    es='Fragmento de Tiburón Fantasma',
)
CursedSealKimimaroFragment = ScoreStoreItem(
    id=3,
    name='CursedSealKimimaroFragment',
    cn='咒印君麻吕碎片',
    cht='咒印君麻呂碎片',
    en='Cursed Seal Kimimaro Fragment',
    jp='呪印キミマロの欠片',
    es='Fragmento de Kimimaro con Sello Maldito',
)
SakuraBlossomWoodMaruiFragment = ScoreStoreItem(
    id=4,
    name='SakuraBlossomWoodMaruiFragment',
    cn='疾风传木叶丸碎片',
    cht='疾風傳木葉丸碎片',
    en='Sakura Blossom Wood Marui Fragment',
    jp='疾風伝サクラマロの欠片',
    es='Fragmento de Marui de la Villa Oculta en las Hojas',
)
DeadSpiritBloodFlyingSegmentFragment = ScoreStoreItem(
    id=5,
    name='DeadSpiritBloodFlyingSegmentFragment',
    cn='死司凭血飞段碎片',
    cht='死司憑血飛段碎片',
    en='Dead Spirit Blood Flying Segment Fragment',
    jp='死司憑血飛段の欠片',
    es='Fragmento de Segmento Volador de Sangre Espiritual',
)
ScorpionFragment = ScoreStoreItem(
    id=6,
    name='ScorpionFragment',
    cn='蝎碎片',
    cht='蠍碎片',
    en='Scorpion Fragment',
    jp='蠍の欠片',
    es='Fragmento de Escorpión',
)
Jade = ScoreStoreItem(
    id=7,
    name='Jade',
    cn='忍玉',
    cht='忍玉',
    en='Jade',
    jp='忍玉',
    es='Jade',
)
Reputation = ScoreStoreItem(
    id=8,
    name='Reputation',
    cn='声望',
    cht='聲望',
    en='Reputation',
    jp='名声',
    es='Reputación',
)
AdvancedSummoningScrollFragment = ScoreStoreItem(
    id=9,
    name='AdvancedSummoningScrollFragment',
    cn='高级通灵卷轴碎片',
    cht='高級通靈卷軸碎片',
    en='Advanced Summoning Scroll Fragment',
    jp='高級召喚卷物の欠片',
    es='Fragmento de Pergamino de Invocación Avanzada',
)
SamsaraStone = ScoreStoreItem(
    id=10,
    name='SamsaraStone',
    cn='轮回石',
    cht='輪迴石',
    en='Samsara Stone',
    jp='輪廻石',
    es='Piedra del Samsara',
)