
from dev_tools.keywords.base import UI_LANGUAGES
from dataclasses import dataclass
from module.ocr.keyword import Keyword
from typing import ClassVar

@dataclass(repr=False)  
class MeritExchangeItem(Keyword):  
    instances: ClassVar = {}  
    @property  
    def item_name(self):  
        return [self.__getattribute__(f"{server}_parsed")  
                for server in UI_LANGUAGES if hasattr(self, f"{server}_parsed")]
AsumaFragment = MeritExchangeItem(
    id=1,
    name='AsumaFragment',
    cn='阿斯玛碎片',
    cht='阿斯瑪碎片',
    en='Asuma Fragment',
    jp='アスマの欠片',
    es='Fragmento de Asuma',
)
ShippudenNarutoFragment = MeritExchangeItem(
    id=2,
    name='ShippudenNarutoFragment',
    cn='疾风传鸣人碎片',
    cht='疾風傳鳴人碎片',
    en='Shippuden Naruto Fragment',
    jp='疾風伝ナルトの欠片',
    es='Fragmento de Naruto Shippuden',
)
ShippudenSakuraFragment = MeritExchangeItem(
    id=3,
    name='ShippudenSakuraFragment',
    cn='疾风传樱碎片',
    cht='疾風傳櫻碎片',
    en='Shippuden Sakura Fragment',
    jp='疾風伝サクラの欠片',
    es='Fragmento de Sakura Shippuden',
)
ShippudenInoFragment = MeritExchangeItem(
    id=4,
    name='ShippudenInoFragment',
    cn='疾风传井野碎片',
    cht='疾風傳井野碎片',
    en='Shippuden Ino Fragment',
    jp='疾風伝イノの欠片',
    es='Fragmento de Ino Shippuden',
)
RandomNinjaFragment = MeritExchangeItem(
    id=5,
    name='RandomNinjaFragment',
    cn='随机忍者碎片',
    cht='隨機忍者碎片',
    en='Random Ninja Fragment',
    jp='ランダム忍者の欠片',
    es='Fragmento de Ninja Aleatorio',
)
OrganizationGiftBox = MeritExchangeItem(  
    id=6,  
    name='OrganizationGiftBox',  
    cn='组织饰品礼盒',  
    cht='組織飾品禮盒',  
    en='Organization Gift Box',  
    jp='組織装身具ギフトボックス',  
    es='Caja de regalo de organización',  
)

ReincarnationStone = MeritExchangeItem(
    id=7,
    name='ReincarnationStone',
    cn='轮回石',
    cht='輪迴石',
    en='Reincarnation Stone',
    jp='輪廻石',
    es='Piedra de Reencarnación',
)
Jade = MeritExchangeItem(
    id=8,
    name='Jade',
    cn='忍玉',
    cht='忍玉',
    en='Jade',
    jp='忍玉',
    es='Jade',
)
Coins=MeritExchangeItem(  
    id=9,  
    name='Coins',  
    cn='铜币',  
    cht='铜币',  
    en='Coins',  
    jp='コイン',  
    es='Monedas',  
)
SecretTechniqueDust = MeritExchangeItem(
    id=10,
    name='SecretTechniqueDust',
    cn='秘术之尘',
    cht='秘術之塵',
    en='Secret Technique Dust',
    jp='秘術の塵',
    es='Polvo de Técnica Secreta',
)
SecretTechniqueStar = MeritExchangeItem(
    id=11,
    name='SecretTechniqueStar',
    cn='秘术之星',
    cht='秘術之星',
    en='Secret Technique Star',
    jp='秘術の星',
    es='Estrella de Técnica Secreta',
)
MysteryEssence = MeritExchangeItem(
    id=12,
    name='MysteryEssence',
    cn='奥秘精华',
    cht='奧秘精華',
    en='Mystery Essence',
    jp='神秘のエッセンス',
    es='Esencia de Misterio',
)
Prestige = MeritExchangeItem(
    id=13,
    name='Prestige',
    cn='声望',
    cht='聲望',
    en='Prestige',
    jp='名声',
    es='Prestigio',
)
RandomLevel3Tomoe = MeritExchangeItem(
    id=14,
    name='RandomLevel3Tomoe',
    cn='随机3级勾玉',
    cht='隨機3級勾玉',
    en='Random Level 3 Tomoe',
    jp='ランダム3級写輪眼',
    es='Tomoe de Nivel 3 Aleatorio',
)