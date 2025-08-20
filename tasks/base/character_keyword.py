
from module.ocr.keyword import Keyword
from dataclasses import dataclass
from typing import ClassVar

from module.ocr.ocr import Ocr
class OcrCharacterTab(Ocr):
    def after_process(self, result):
        # 移除常见后缀
        result = result.replace('碎片', '')
        result = result.replace('移土', '秽土')
        result = result.strip()
        return super().after_process(result)
@dataclass
class CharacterTab(Keyword):
    instances: ClassVar = {}
HuiTuJieBan = CharacterTab(
    id=1,
    name='HuiTuJieBan',
    cn='秽土解斑',
    cht='穢土解斑',
    en='Edo Tensei Madara',
    jp='穢土転生斑',
    es='Madara Edo Tensei',
)

YongHengZuoZhu = CharacterTab(
    id=2,
    name='YongHengZuoZhu',
    cn='永恒佐助',
    cht='永恆佐助',
    en='Eternal Sasuke',
    jp='永遠のサスケ',
    es='Sasuke Eterno',
)

RenZhanYing = CharacterTab(
    id=3,
    name='RenZhanYing',
    cn='忍战樱',
    cht='忍戰櫻',
    en='Ninja War Sakura',
    jp='忍界大戦サクラ',
    es='Sakura Guerra Ninja',
)

JiuLaMaMingRen = CharacterTab(
    id=4,
    name='JiuLaMaMingRen',
    cn='九喇嘛鸣人',
    cht='九喇嘛鳴人',
    en='Nine-Tails Naruto',
    jp='九喇嘛ナルト',
    es='Naruto Nueve Colas',
)

SiMenKai = CharacterTab(
    id=5,
    name='SiMenKai',
    cn='死门凯',
    cht='死門凱',
    en='Eight Gates Guy',
    jp='八門ガイ',
    es='Guy Ocho Puertas',
)

HuiTuZhuJian = CharacterTab(
    id=6,
    name='HuiTuZhuJian',
    cn='秽土柱间',
    cht='穢土柱間',
    en='Edo Tensei Hashirama',
    jp='穢土転生柱間',
    es='Hashirama Edo Tensei',
)

HuiTuShu = CharacterTab(
    id=7,
    name='HuiTuShu',
    cn='秽土鼬',
    cht='穢土鼬',
    en='Edo Tensei Itachi',
    jp='穢土転生イタチ',
    es='Itachi Edo Tensei',
)

XianRenDou = CharacterTab(
    id=8,
    name='XianRenDou',
    cn='仙人兜',
    cht='仙人兜',
    en='Sage Kabuto',
    jp='仙人カブト',
    es='Kabuto Sabio',
)

HuiTuBan = CharacterTab(
    id=9,
    name='HuiTuBan',
    cn='秽土斑',
    cht='穢土斑',
    en='Edo Tensei Madara',
    jp='穢土転生マダラ',
    es='Madara Edo Tensei',
)

BaiMianJu = CharacterTab(
    id=10,
    name='BaiMianJu',
    cn='白面具',
    cht='白面具',
    en='White Mask',
    jp='白い仮面',
    es='Máscara Blanca',
)

HuiTuFeiJian = CharacterTab(
    id=11,
    name='HuiTuFeiJian',
    cn='秽土扉间',
    cht='穢土扉間',
    en='Edo Tensei Tobirama',
    jp='穢土転生扉間',
    es='Tobirama Edo Tensei',
)

BaiHaoGangShou = CharacterTab(
    id=12,
    name='BaiHaoGangShou',
    cn='百豪纲手',
    cht='百豪綱手',
    en='Hundred Healings Tsunade',
    jp='百豪の術綱手',
    es='Tsunade Cien Curaciones',
)

HuiTuShuiMen = CharacterTab(
    id=13,
    name='HuiTuShuiMen',
    cn='秽土水门',
    cht='穢土水門',
    en='Edo Tensei Minato',
    jp='穢土転生ミナト',
    es='Minato Edo Tensei',
)

HuiTuRiZhan = CharacterTab(
    id=14,
    name='HuiTuRiZhan',
    cn='秽土日斩',
    cht='穢土日斬',
    en='Edo Tensei Hiruzen',
    jp='穢土転生ヒルゼン',
    es='Hiruzen Edo Tensei',
)

HuiTuChangMen = CharacterTab(
    id=15,
    name='HuiTuChangMen',
    cn='秽土长门',
    cht='穢土長門',
    en='Edo Tensei Nagato',
    jp='穢土転生長門',
    es='Nagato Edo Tensei',
)

Ban = CharacterTab(
    id=16,
    name='Ban',
    cn='斑',
    cht='斑',
    en='Madara',
    jp='マダラ',
    es='Madara',
)

ZhuJian = CharacterTab(
    id=17,
    name='ZhuJian',
    cn='柱间',
    cht='柱間',
    en='Hashirama',
    jp='柱間',
    es='Hashirama',
)

SiDaiMuLeiYing = CharacterTab(
    id=18,
    name='SiDaiMuLeiYing',
    cn='四代目雷影',
    cht='四代目雷影',
    en='Fourth Raikage',
    jp='四代目雷影',
    es='Cuarto Raikage',
)

FeiJian = CharacterTab(
    id=19,
    name='FeiJian',
    cn='扉间',
    cht='扉間',
    en='Tobirama',
    jp='扉間',
    es='Tobirama',
)

ShenMiMianJuNan = CharacterTab(
    id=20,
    name='ShenMiMianJuNan',
    cn='神秘面具男',
    cht='神秘面具男',
    en='Masked Man',
    jp='仮面の男',
    es='Hombre Enmascarado',
)

XuZuoNengHuShu = CharacterTab(
    id=21,
    name='XuZuoNengHuShu',
    cn='须佐能乎鼬',
    cht='須佐能乎鼬',
    en='Susanoo Itachi',
    jp='須佐能乎イタチ',
    es='Itachi Susanoo',
)

TianDaoPeiEn = CharacterTab(
    id=22,
    name='TianDaoPeiEn',
    cn='天道佩恩',
    cht='天道佩恩',
    en='Tendo Pain',
    jp='天道ペイン',
    es='Pain Tendo',
)

ShuiMen = CharacterTab(
    id=23,
    name='ShuiMen',
    cn='水门',
    cht='水門',
    en='Minato',
    jp='ミナト',
    es='Minato',
)

DaSheWan = CharacterTab(
    id=24,
    name='DaSheWan',
    cn='大蛇丸',
    cht='大蛇丸',
    en='Orochimaru',
    jp='大蛇丸',
    es='Orochimaru',
)

ZiLaiYe = CharacterTab(
    id=25,
    name='ZiLaiYe',
    cn='自来也',
    cht='自來也',
    en='Jiraiya',
    jp='自来也',
    es='Jiraiya',
)