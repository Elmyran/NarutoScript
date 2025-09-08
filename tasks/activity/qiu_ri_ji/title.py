from dataclasses import dataclass

from module.ocr.keyword import Keyword
from typing import ClassVar

@dataclass(repr=False)
class QuizTitle(Keyword):
    instances: ClassVar = {}
    def __hash__(self):
        return super().__hash__()
DingCi = QuizTitle(
    id=0,
    name='DingCi',
    cn='好吃"秋道丁次开心的吃着你给的零食，他身上刚好有些东西，你可以选择一件作为回礼。',
    cht='「好吃」秋道丁次開心地吃著你給的零食，他身上剛好有些東西，你可以選擇一件作為回禮。',
    en='Delicious!" Chōji Akimichi happily eats the snack you gave him. He happens to have something on him, and you can choose one item as a return gift.',
    jp='「おいしい！」秋道チョウジはあなたがくれたお菓子を嬉しそうに食べています。ちょうど彼の持ち物の中に何かがあり、お返しとして一つ選ぶことができます。',
    es='¡Delicioso!” Chōji Akimichi come felizmente el bocadillo que le diste. Resulta que tiene algunas cosas con él, y puedes elegir un objeto como regalo de agradecimiento.',

)
JiaoJi = QuizTitle(
    id=1,
    name='JiaoJi',
    cn='让我来考考你！”能够吸收查克拉的忍具是？',
    cht='讓我來考考你！」能夠吸收查克拉的忍具是？',
    en='Let me test you! Which ninja tool can absorb chakra?',
    jp='試してみよう！チャクラを吸収できる忍具はどれですか？',
    es='¡Déjame ponerte a prueba! ¿Qué herramienta ninja puede absorber chakra?',
)

GangShou = QuizTitle(
    id=2,
    name='GangShou',
    cn='遇到了前来拜访的纲手，她盯着你手中的初级肥料箱要和你赌一把。',
    cht='遇到了前來拜訪的綱手，她盯著你手中的初級肥料箱要和你賭一把。',
    en='You meet Tsunade who comes to visit. She stares at the beginner’s fertilizer box in your hand and wants to bet with you.',
    jp='訪ねてきた綱手に会った。彼女はあなたの手にある初級肥料箱をじっと見つめ、勝負を挑んでくる。',
    es='Te encuentras con Tsunade que viene de visita. Ella fija la mirada en la caja de fertilizante inicial que tienes en la mano y quiere apostar contigo.',
)

Gaming = QuizTitle(
    id=3,
    name='Gaming',
    cn='“小鬼，开始吧！”你要选择出什么呢？',
    cht='「小鬼，開始吧！」你要選擇出什麼呢？',
    en='"Brat, let’s begin!" What will you choose?',
    jp='「ガキ、始めるぞ！」君は何を選ぶ？',
    es='"¡Niño, empecemos!" ¿Qué vas a elegir?',
)

Expert = QuizTitle(
    id=4,
    name='Expert',
    cn='哪位忍者是拷问和盘问的专家？',
    cht='哪位忍者是拷問和盤問的專家？',
    en='Which ninja is an expert in interrogation and torture?',
    jp='尋問と拷問の専門家である忍者は誰ですか？',
    es='¿Qué ninja es un experto en interrogatorios y torturas?',
)

XiaoLi = QuizTitle(
    id=5,
    name='XiaoLi',
    cn='“青春就是要不断运动！”李洛克干劲十足地出现在你面前，是否邀请他一起？',
    cht='「青春就是要不斷運動！」李洛克幹勁十足地出現在你面前，是否邀請他一起？',
    en='"Youth means constant movement!" Rock Lee appears before you full of energy. Will you invite him to join?',
    jp='「青春とは絶えず動くことだ！」ロック・リーが元気いっぱいに現れた。君は彼を誘うか？',
    es='"¡La juventud significa moverse sin parar!" Rock Lee aparece lleno de energía frente a ti. ¿Lo invitas a unirse?',
)

ZhiNai = QuizTitle(
    id=6,
    name='ZhiNai',
    cn='油女志乃沉默地站在你面前，看着你手中的高级杀虫剂。',
    cht='油女志乃沉默地站在你面前，看著你手中的高級殺蟲劑。',
    en='Shino Aburame stands silently in front of you, staring at the advanced insecticide in your hand.',
    jp='油女シノが黙ってあなたの前に立ち、あなたの手にある高級殺虫剤を見つめている。',
    es='Shino Aburame se queda en silencio frente a ti, mirando fijamente el insecticida avanzado que tienes en la mano.',
)

KaoGuan = QuizTitle(
    id=7,
    name='KaoGuan',
    cn='“让我来考考你！”中忍考试第二场的考官是谁？',
    cht='「讓我來考考你！」中忍考試第二場的考官是誰？',
    en='Let me test you! Who was the examiner of the second round of the Chunin Exams?',
    jp='「試してみよう！」中忍試験第二試合の試験官は誰だった？',
    es='¡Déjame ponerte a prueba! ¿Quién fue el examinador de la segunda ronda del Examen Chunin?',
)
