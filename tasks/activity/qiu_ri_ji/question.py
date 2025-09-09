import random

from module.exception import ScriptError
from tasks.activity.qiu_ri_ji.option import *
from tasks.activity.qiu_ri_ji.title import *
def match_quiz_title(question_text, quiz_titles):
    """匹配题目文本到题库中的题目"""
    for quiz_title in quiz_titles:
        try:
            # 使用关键词系统的find方法进行模糊匹配
            matched = quiz_title.find(
                question_text,
                ignore_punctuation=True
            )
            if matched:
                return matched
        except ScriptError:
            continue
    return None
def select_quiz_answer(self, quiz_title, available_options):
    priority = QUIZ_STRATEGIES.get(quiz_title, [])

    for expected_answer in priority:
        for option in available_options:
            if option.matched_keyword == expected_answer:
                return option

                # 如果没有匹配到，随机选择
    return random.choice(available_options)
QUIZ_OPTIONS = {
    'PreciousCommemorativeCoin':PreciousCommemorativeCoin,
    'Samehada':Samehada,
    'GuessTheBox':GuessTheBox,
    'JianDao':JianDao,
    'YiBiXi':YiBiXi,
    'ThrowAway':ThrowAway,
    'GanHuo':GanHuo,
    'HongDou':HongDou,
}

# 建立答题策略
QUIZ_STRATEGIES = {
    DingCi: [QUIZ_OPTIONS['PreciousCommemorativeCoin']],
    JiaoJi: [QUIZ_OPTIONS['Samehada']],
    GangShou: [QUIZ_OPTIONS['GuessTheBox']],
    Gaming:[QUIZ_OPTIONS['JianDao']],
    Expert:[QUIZ_OPTIONS['YiBiXi']],
    ZhiNai:[QUIZ_OPTIONS['ThrowAway']],
    XiaoLi:[QUIZ_OPTIONS['GanHuo']],
    KaoGuan:[QUIZ_OPTIONS['HongDou']],

}