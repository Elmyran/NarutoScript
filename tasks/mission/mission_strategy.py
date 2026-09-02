from enum import Enum

from tasks.mission.priority import TaskPriority


class StrategyAction(Enum):
    ACCEPT = 'accept'
    REFRESH = 'refresh'
    STOP = 'stop'


class MissionStrategy:
    """接取策略基类: 每轮对当前任务面板做出一个决策。

    decide 必须无副作用(不点击/不截图), 只根据显式传入的状态做决策:
        tasks          当前面板上的有效任务, 已按优先级排序
        accepted_times 本次运行已接取任务的时长(分钟)列表
        can_refresh    当前是否还有免费刷新次数(仅查询按钮状态, 不点击)
    """
    def decide(self, tasks, accepted_times, can_refresh):
        raise NotImplementedError


class NormalAcceptStrategy(MissionStrategy):
    """普通玩家: 不可刷新, 一次最多接3个, 按优先级接满为止。"""
    def decide(self, tasks, accepted_times, can_refresh):
        if not tasks:
            return StrategyAction.STOP, None
        return StrategyAction.ACCEPT, tasks[0]


class RedBoxFirstStrategy(MissionStrategy):
    """特权玩家: 红箱优先; 无红箱则免费刷新; 刷新耗尽后按优先级接取其他任务, 直到接满。"""
    def decide(self, tasks, accepted_times, can_refresh):
        if tasks and tasks[0].priority == TaskPriority.RED:
            return StrategyAction.ACCEPT, tasks[0]
        if can_refresh:
            return StrategyAction.REFRESH, None
        if tasks:
            return StrategyAction.ACCEPT, tasks[0]
        return StrategyAction.STOP, None


class RedBoxOnlyStrategy(MissionStrategy):
    """特权玩家: 只接红箱; 无红箱则免费刷新; 刷新耗尽即停止, 不接其他任务(不要求接满)。"""
    def decide(self, tasks, accepted_times, can_refresh):
        if tasks and tasks[0].priority == TaskPriority.RED:
            return StrategyAction.ACCEPT, tasks[0]
        if can_refresh:
            return StrategyAction.REFRESH, None
        return StrategyAction.STOP, None


# 策略注册表: 显式绑定名称与策略类, Mission._select_strategy() 按超影剩余天数取用
# (超影有效 -> red_box, 无超影 -> normal; red_box_only 保留为手动扩展点)
STRATEGIES = {
    'normal': NormalAcceptStrategy,
    'red_box': RedBoxFirstStrategy,
    'red_box_only': RedBoxOnlyStrategy,
}
