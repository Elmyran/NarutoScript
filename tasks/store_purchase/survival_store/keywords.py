from re import S
from dev_tools.keywords.base import UI_LANGUAGES
from dataclasses import dataclass
from module.ocr.keyword import Keyword
from typing import ClassVar

@dataclass(repr=False)  
class SurvivalStoreItem(Keyword):  
    instances: ClassVar = {}  
    @property  
    def item_name(self):  
        return [self.__getattribute__(f"{server}_parsed")  
                for server in UI_LANGUAGES if hasattr(self, f"{server}_parsed")]
RedBeanFragment = SurvivalStoreItem(
    id=1,
    name='RedBeanFragment',
    cn='红豆碎片',
    cht='紅豆碎片',
    en='Red Bean Fragment',
    jp='紅豆の欠片',
    es='Fragmento de Red Bean',
)
KaiFragment = SurvivalStoreItem(
    id=2,
    name='KaiFragment',
    cn='凯碎片',
    cht='凱碎片',
    en='Kai Fragment',
    jp='カイの欠片',
    es='Fragmento de Kai',
)
FirstTailNarutoFragment = SurvivalStoreItem(
    id=3,
    name='FirstTailNarutoFragment',
    cn='第一尾鸣人碎片',
    cht='第一尾鳴人碎片',
    en='First Tail Naruto Fragment',
    jp='第一尾のナルトの欠片',
    es='Fragmento de Naruto de la Primera Cola',
)
ShippudenInoFragment = SurvivalStoreItem(
    id=4,
    name='ShippudenInoFragment',
    cn='疾风传井野碎片',
    cht='疾風傳井野碎片',
    en='Shippuden Ino Fragment',
    jp='疾風伝のいのの欠片',
    es='Fragmento de Ino Shippuden',
)
Reputation = SurvivalStoreItem(
    id=5,
    name='Reputation',
    cn='声望',
    cht='聲望',
    en='Reputation',
    jp='名声',
    es='Reputación',
)
ShippudenTemariFragment = SurvivalStoreItem(
    id=6,
    name='ShippudenTemariFragment',
    cn='疾风传手鞠碎片',
    cht='疾風傳手鞠碎片',
    en='Shippuden Temari Fragment',
    jp='疾風伝のテマリの欠片',
    es='Fragmento de Temari Shippuden',
)
ReincarnationStone = SurvivalStoreItem(
    id=7,
    name='ReincarnationStone',
    cn='轮回石',
    cht='輪迴石',
    en='Reincarnation Stone',
    jp='輪廻石',
    es='Piedra de Reencarnación',
)
Jade = SurvivalStoreItem(
    id=8,
    name='Jade',
    cn='忍玉',
    cht='忍玉',
    en='Jade',
    jp='忍玉',
    es='Jade',
)
ReforgingCharm = SurvivalStoreItem(
    id=9,
    name='ReforgingCharm',
    cn='重铸符',
    cht='重鑄符',
    en='Reforging Charm',
    jp='重鑄符',
    es='Talismán de Reforzamiento',
)
TsuchikuraFragment = SurvivalStoreItem(
    id=10,
    name='TsuchikuraFragment',
    cn='土台碎片',
    cht='土台碎片',
    en='Tsuchikura Fragment',
    jp='土台の欠片',
    es='Fragmento de Tsuchikura',
)