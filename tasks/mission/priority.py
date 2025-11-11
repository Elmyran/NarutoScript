from enum import IntEnum
class TaskPriority(IntEnum):
    """任务优先级枚举，数值越小优先级越高"""
    RED = 1     # 红箱 - 最高优先级
    BLUE = 2    # 蓝箱 - 中等优先级
    GREEN = 3   # 绿箱 - 最低优先级

