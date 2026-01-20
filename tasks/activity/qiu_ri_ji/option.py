from dataclasses import dataclass
from module.ocr.keyword import Keyword
from typing import ClassVar
@dataclass(repr=False)
class QuizOption(Keyword):
    instances: ClassVar = {}
PreciousCommemorativeCoin = QuizOption(
    id=0,
    name='Precious Commemorative Coin',
    cn='珍贵纪念币',        # 简体中文
    cht='珍貴紀念幣',       # 繁體中文
    en='Precious Commemorative Coin',  # 英文
    jp='貴重な記念コイン',  # 日文
    es='Moneda Conmemorativa Preciosa' # 西班牙文
)
Samehada= QuizOption(
    id=1,
    name='Samehada',
    cn='鲛肌',
    cht='鮫肌',
    en='Samehada',
    jp='鮫肌（さめはだ）',
    es='Samehada'
)
GuessTheBox = QuizOption(
    id=2,
    name='GuessTheBox',
    cn='开始猜拳',
    cht='開始猜拳',
    en='Start rock-paper-scissors',
    jp='じゃんけんを始める',
    es='Comenzar piedra, papel o tijera'
)

JianDao = QuizOption(
    id=3,
    name='JianDao',
    cn='剪刀',
    cht='剪刀',
    en='Scissors',
    jp='ハサミ',
    es='Tijeras'
)

YiBiXi = QuizOption(
    id=4,
    name='YiBiXi',
    cn='森乃伊比喜',
    cht='森乃伊比喜',
    en='Ibiki Morino',
    jp='森乃イビキ',
    es='Ibiki Morino'
)

GanHuo = QuizOption(
    id=5,
    name='GanHuo',
    cn='我们一起来干活吧',
    cht='我們一起來幹活吧',
    en="Let's work together",
    jp='一緒に働こう',
    es='Trabajemos juntos'
)

ThrowAway = QuizOption(
    id=6,
    name='ThrowAway',
    cn='将杀虫剂扔掉',
    cht='將殺蟲劑扔掉',
    en='Throw away the insecticide',
    jp='殺虫剤を捨てる',
    es='Tirar el insecticida'
)

HongDou = QuizOption(
    id=7,
    name='HongDou',
    cn='御手洗红豆',
    cht='御手洗紅豆',
    en='Anko Mitarashi',
    jp='御手洗アンコ',
    es='Anko Mitarashi'
)
LuJiu=QuizOption(
    id=8,
    name='LuJiu',
    cn='奈良鹿久',
    cht='御手洗紅豆',
    en='Anko Mitarashi',
    jp='御手洗アンコ',
    es='Anko Mitarashi'
)
YiDong=QuizOption(
    id=9,
    name='YiDong',
    cn='切碎之刑',
    cht='御手洗紅豆',
    en='Anko Mitarashi',
    jp='御手洗アンコ',
    es='Anko Mitarashi'
)

