
from module.ocr.keyword import Keyword
from dataclasses import dataclass
from typing import ClassVar
import re
from module.ocr.ocr import Ocr
class OcrCharacterTab(Ocr):
    def after_process(self, result):

        result = result.replace('碎片', '')
        result = result.replace('移', '秽')
        result = re.sub('^托斯', '托斯砧', result)  
        result = re.sub('^萨克', '萨克镫', result)
        result = result.strip()
        return super().after_process(result)
@dataclass
class SCharacterTab(Keyword):
    instances: ClassVar = {}

SHuiTuJieBan = SCharacterTab(
    id=1,
    name='HuiTuJieBan',
    cn='秽土解斑',
    cht='穢土解斑',
    en='Edo Tensei Madara',
    jp='穢土転生斑',
    es='Madara Edo Tensei',
)

SYongHengZuoZhu = SCharacterTab(
    id=2,
    name='YongHengZuoZhu',
    cn='永恒佐助',
    cht='永恆佐助',
    en='Eternal Sasuke',
    jp='永遠のサスケ',
    es='Sasuke Eterno',
)

SRenZhanYing = SCharacterTab(
    id=3,
    name='RenZhanYing',
    cn='忍战樱',
    cht='忍戰櫻',
    en='Ninja War Sakura',
    jp='忍界大戦サクラ',
    es='Sakura Guerra Ninja',
)

SJiuLaMaMingRen = SCharacterTab(
    id=4,
    name='JiuLaMaMingRen',
    cn='九喇嘛鸣人',
    cht='九喇嘛鳴人',
    en='Nine-Tails Naruto',
    jp='九喇嘛ナルト',
    es='Naruto Nueve Colas',
)

SSiMenKai = SCharacterTab(
    id=5,
    name='SiMenKai',
    cn='死门凯',
    cht='死門凱',
    en='Eight Gates Guy',
    jp='八門ガイ',
    es='Guy Ocho Puertas',
)

SHuiTuZhuJian = SCharacterTab(
    id=6,
    name='HuiTuZhuJian',
    cn='秽土柱间',
    cht='穢土柱間',
    en='Edo Tensei Hashirama',
    jp='穢土転生柱間',
    es='Hashirama Edo Tensei',
)

SHuiTuShu = SCharacterTab(
    id=7,
    name='HuiTuShu',
    cn='秽土鼬',
    cht='穢土鼬',
    en='Edo Tensei Itachi',
    jp='穢土転生イタチ',
    es='Itachi Edo Tensei',
)

SXianRenDou = SCharacterTab(
    id=8,
    name='XianRenDou',
    cn='仙人兜',
    cht='仙人兜',
    en='Sage Kabuto',
    jp='仙人カブト',
    es='Kabuto Sabio',
)

SHuiTuBan = SCharacterTab(
    id=9,
    name='HuiTuBan',
    cn='秽土斑',
    cht='穢土斑',
    en='Edo Tensei Madara',
    jp='穢土転生マダラ',
    es='Madara Edo Tensei',
)

SBaiMianJu = SCharacterTab(
    id=10,
    name='BaiMianJu',
    cn='白面具',
    cht='白面具',
    en='White Mask',
    jp='白い仮面',
    es='Máscara Blanca',
)

SHuiTuFeiJian = SCharacterTab(
    id=11,
    name='HuiTuFeiJian',
    cn='秽土扉间',
    cht='穢土扉間',
    en='Edo Tensei Tobirama',
    jp='穢土転生扉間',
    es='Tobirama Edo Tensei',
)

SBaiHaoGangShou = SCharacterTab(
    id=12,
    name='BaiHaoGangShou',
    cn='百豪纲手',
    cht='百豪綱手',
    en='Hundred Healings Tsunade',
    jp='百豪の術綱手',
    es='Tsunade Cien Curaciones',
)

SHuiTuShuiMen = SCharacterTab(
    id=13,
    name='HuiTuShuiMen',
    cn='秽土水门',
    cht='穢土水門',
    en='Edo Tensei Minato',
    jp='穢土転生ミナト',
    es='Minato Edo Tensei',
)

SHuiTuRiZhan = SCharacterTab(
    id=14,
    name='HuiTuRiZhan',
    cn='秽土日斩',
    cht='穢土日斬',
    en='Edo Tensei Hiruzen',
    jp='穢土転生ヒルゼン',
    es='Hiruzen Edo Tensei',
)

SHuiTuChangMen = SCharacterTab(
    id=15,
    name='HuiTuChangMen',
    cn='秽土长门',
    cht='穢土長門',
    en='Edo Tensei Nagato',
    jp='穢土転生長門',
    es='Nagato Edo Tensei',
)

SBan = SCharacterTab(
    id=16,
    name='Ban',
    cn='斑',
    cht='斑',
    en='Madara',
    jp='マダラ',
    es='Madara',
)

SZhuJian = SCharacterTab(
    id=17,
    name='ZhuJian',
    cn='柱间',
    cht='柱間',
    en='Hashirama',
    jp='柱間',
    es='Hashirama',
)

SSiDaiMuLeiYing = SCharacterTab(
    id=18,
    name='SiDaiMuLeiYing',
    cn='四代目雷影',
    cht='四代目雷影',
    en='Fourth Raikage',
    jp='四代目雷影',
    es='Cuarto Raikage',
)

SFeiJian = SCharacterTab(
    id=19,
    name='FeiJian',
    cn='扉间',
    cht='扉間',
    en='Tobirama',
    jp='扉間',
    es='Tobirama',
)

SShenMiMianJuNan = SCharacterTab(
    id=20,
    name='ShenMiMianJuNan',
    cn='神秘面具男',
    cht='神秘面具男',
    en='Masked Man',
    jp='仮面の男',
    es='Hombre Enmascarado',
)

SXuZuoNengHuShu = SCharacterTab(
    id=21,
    name='XuZuoNengHuShu',
    cn='须佐能乎鼬',
    cht='須佐能乎鼬',
    en='Susanoo Itachi',
    jp='須佐能乎イタチ',
    es='Itachi Susanoo',
)

STianDaoPeiEn = SCharacterTab(
    id=22,
    name='TianDaoPeiEn',
    cn='天道佩恩',
    cht='天道佩恩',
    en='Tendo Pain',
    jp='天道ペイン',
    es='Pain Tendo',
)

SShuiMen = SCharacterTab(
    id=23,
    name='ShuiMen',
    cn='水门',
    cht='水門',
    en='Minato',
    jp='ミナト',
    es='Minato',
)

SDaSheWan = SCharacterTab(
    id=24,
    name='DaSheWan',
    cn='大蛇丸',
    cht='大蛇丸',
    en='Orochimaru',
    jp='大蛇丸',
    es='Orochimaru',
)

SZiLaiYe = SCharacterTab(
    id=25,
    name='ZiLaiYe',
    cn='自来也',
    cht='自來也',
    en='Jiraiya',
    jp='自来也',
    es='Jiraiya',
)
@dataclass
class ACharacterTab(Keyword):
    instances: ClassVar = {}

TaoShiXianBoRen = ACharacterTab(
    id=1,
    name='TaoShiXianBoRen',
    cn='桃式显现博人',
    cht='桃式顯現博人',
    en='Tao Manifestation Boruto',
    jp='桃式顕現ボルト',
    es='Boruto Manifestación de Tao',
)

RenZhanNingCi = ACharacterTab(
    id=2,
    name='RenZhanNingCi',
    cn='忍战宁次',
    cht='忍戰寧次',
    en='Ninja War Neji',
    jp='忍界大戦ネジ',
    es='Neji Guerra Ninja',
)

BoRenChuanChangShiLang = ACharacterTab(
    id=3,
    name='BoRenChuanChangShiLang',
    cn='博人传长十郎',
    cht='博人傳長十郎',
    en='Boruto Era Chōjūrō',
    jp='ボルト伝チョウジュロウ',
    es='Chōjūrō Era Boruto',
)

QingNianChangMen = ACharacterTab(
    id=4,
    name='QingNianChangMen',
    cn='青年长门',
    cht='青年長門',
    en='Young Nagato',
    jp='青年長門',
    es='Nagato Joven',
)

QingNianAi = ACharacterTab(
    id=5,
    name='QingNianAi',
    cn='青年艾',
    cht='青年艾',
    en='Young A',
    jp='青年エー',
    es='A Joven',
)

BoRenChuanDaLuYi = ACharacterTab(
    id=6,
    name='BoRenChuanDaLuYi',
    cn='博人传达鲁伊',
    cht='博人傳達魯伊',
    en='Boruto Era Darui',
    jp='ボルト伝ダルイ',
    es='Darui Era Boruto',
)

QingNianShuiMen = ACharacterTab(
    id=7,
    name='QingNianShuiMen',
    cn='青年水门',
    cht='青年水門',
    en='Young Minato',
    jp='青年ミナト',
    es='Minato Joven',
)

RenZhanQiLaBi = ACharacterTab(
    id=8,
    name='RenZhanQiLaBi',
    cn='忍战奇拉比',
    cht='忍戰奇拉比',
    en='Ninja War Killer B',
    jp='忍界大戦キラービー',
    es='Killer B Guerra Ninja',
)

BoRenChuanHeiTU = ACharacterTab(
    id=9,
    name='BoRenChuanHeiTU',
    cn='博人传黑土',
    cht='博人傳黑土',
    en='Boruto Era Kurotsuchi',
    jp='ボルト伝黒土',
    es='Kurotsuchi Era Boruto',
)

XuZuoZuoZhu = ACharacterTab(
    id=10,
    name='XuZuoZuoZhu',
    cn='须佐佐助',
    cht='須佐佐助',
    en='Susanoo Sasuke',
    jp='須佐能乎サスケ',
    es='Sasuke Susanoo',
)

HuiTuDiDaLa = ACharacterTab(
    id=11,
    name='HuiTuDiDaLa',
    cn='秽土迪达拉',
    cht='穢土迪達拉',
    en='Edo Tensei Deidara',
    jp='穢土転生デイダラ',
    es='Deidara Edo Tensei',
)

BoRenChuanMuYeWan = ACharacterTab(
    id=12,
    name='BoRenChuanMuYeWan',
    cn='博人传木叶丸',
    cht='博人傳木葉丸',
    en='Boruto Era Konohamaru',
    jp='ボルト伝コノハマル',
    es='Konohamaru Era Boruto',
)

JiuWeiMingRen = ACharacterTab(
    id=13,
    name='JiuWeiMingRen',
    cn='九尾鸣人',
    cht='九尾鳴人',
    en='Nine-Tails Naruto',
    jp='九喇嘛ナルト',
    es='Naruto Nueve Colas',
)

BanSheDouPengDunDou = ACharacterTab(
    id=14,
    name='BanSheDouPengDunDou',
    cn='半蛇斗篷兜',
    cht='半蛇斗篷兜',
    en='Half-Snake Cloak Kabuto',
    jp='半蛇斗篷カブト',
    es='Kabuto Capa Medio-Serpiente',
)

RenZhanWoAiLuo = ACharacterTab(
    id=15,
    name='RenZhanWoAiLuo',
    cn='忍战我爱罗',
    cht='忍戰我愛羅',
    en='Ninja War Gaara',
    jp='忍界大戦ガアラ',
    es='Gaara Guerra Ninja',
)

XiaoDaSheWan = ACharacterTab(
    id=16,
    name='XiaoDaSheWan',
    cn='晓大蛇丸',
    cht='曉大蛇丸',
    en='Akatsuki Orochimaru',
    jp='暁の大蛇丸',
    es='Orochimaru Akatsuki',
)

BaiHaoYing = ACharacterTab(
    id=17,
    name='BaiHaoYing',
    cn='百豪樱',
    cht='百豪櫻',
    en='Hundred Healings Sakura',
    jp='百豪の術サクラ',
    es='Sakura Cien Curaciones',
)

ZhaoMeiMing = ACharacterTab(
    id=18,
    name='ZhaoMeiMing',
    cn='照美冥',
    cht='照美冥',
    en='Terumi Mei',
    jp='テルミ・メイ',
    es='Mei Terumi',
)

YingXiaoDuiZuoZhu = ACharacterTab(
    id=19,
    name='YingXiaoDuiZuoZhu',
    cn='鹰小队佐助',
    cht='鷹小隊佐助',
    en='Hawk Team Sasuke',
    jp='鷹小隊サスケ',
    es='Sasuke Equipo Halcón',
)

QiLaBi = ACharacterTab(
    id=20,
    name='QiLaBi',
    cn='奇拉比',
    cht='奇拉比',
    en='Killer B',
    jp='キラービー',
    es='Killer B',
)

XianRenMingRen = ACharacterTab(
    id=21,
    name='XianRenMingRen',
    cn='仙人鸣人',
    cht='仙人鳴人',
    en='Sage Naruto',
    jp='仙人モードナルト',
    es='Naruto Sabio',
)

ShenWeiKaKaXi = ACharacterTab(
    id=22,
    name='ShenWeiKaKaXi',
    cn='神威卡卡西',
    cht='神威卡卡西',
    en='Kamui Kakashi',
    jp='神威カカシ',
    es='Kakashi Kamui',
)

ZhiShui = ACharacterTab(
    id=23,
    name='ZhiShui',
    cn='止水',
    cht='止水',
    en='Shisui',
    jp='シスイ',
    es='Shisui',
)

XiaoNan = ACharacterTab(
    id=24,
    name='XiaoNan',
    cn='小南',
    cht='小南',
    en='Konan',
    jp='コナン',
    es='Konan',
)

DiDaLa = ACharacterTab(
    id=25,
    name='DiDaLa',
    cn='迪达拉',
    cht='迪達拉',
    en='Deidara',
    jp='デイダラ',
    es='Deidara',
)

You = ACharacterTab(
    id=26,
    name='You',
    cn='鼬',
    cht='鼬',
    en='Itachi',
    jp='イタチ',
    es='Itachi',
)

Kai = ACharacterTab(
    id=27,
    name='Kai',
    cn='凯',
    cht='凱',
    en='Guy',
    jp='ガイ',
    es='Guy',
)
@dataclass
class CCharacterTab(Keyword):
    instances: ClassVar = {}

ZuoJinYouJin = CCharacterTab(
    id=1,
    name='ZuoJinYouJin',
    cn='左近右近',
    cht='左近右近',
    en='Left and Right',
    jp='左近右近',
    es='Izquierda y Derecha',
)

HuoHua = CCharacterTab(
    id=2,
    name='HuoHua',
    cn='火花',
    cht='火花',
    en='Spark',
    jp='スパーク',
    es='Chispa',
)

XueYuanMingRen = CCharacterTab(
    id=3,
    name='XueYuanMingRen',
    cn='学员鸣人',
    cht='學員鳴人',
    en='Academy Student Naruto',
    jp='忍者学校のナルト',
    es='Naruto Estudiante de la Academia',
)

ShanChengQingYe = CCharacterTab(
    id=4,
    name='ShanChengQingYe',
    cn='山城青叶',
    cht='山城青葉',
    en='Aoba Yamashiro',
    jp='山城青葉',
    es='Aoba Yamashiro',
)

GuiTongWan = CCharacterTab(
    id=5,
    name='GuiTongWan',
    cn='鬼童丸',
    cht='鬼童丸',
    en='Kidomaru',
    jp='鬼童丸',
    es='Kidomaru',
)

Qing = CCharacterTab(
    id=6,
    name='Qing',
    cn='青',
    cht='青',
    en='A',
    jp='青',
    es='A',
)

SaKeDeng = CCharacterTab(
    id=7,
    name='SaKeDeng',
    cn='萨克镫',
    cht='薩克鐙',
    en='Sakon and Ukon',
    jp='サクンとウコン',
    es='Sakon y Ukon',
)

TuoSiZhen = CCharacterTab(
    id=8,
    name='TuoSiZhen',
    cn='托斯砧',
    cht='托斯砧',
    en='Tayuya',
    jp='多由也',
    es='Tayuya',
)