from enum import IntEnum
from typing import List, Dict, Optional, Union
from dataclasses import dataclass, field
import logging
from datetime import datetime



logger = logging.getLogger(__name__)

class TaskPriority(IntEnum):
    """任务优先级枚举，数值越小优先级越高"""
    RED = 1     # 红箱 - 最高优先级
    BLUE = 2    # 蓝箱 - 中等优先级
    GREEN = 3   # 绿箱 - 最低优先级

@dataclass
class MissionTask:
    """任务数据类"""
    name: str
    time: int  # 时间（分钟）
    soul_jade_amount: int
    priority: TaskPriority = TaskPriority.GREEN
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """确保时间是整数"""
        if isinstance(self.time, str):
            self.time = self._parse_time_string(self.time)

    def _parse_time_string(self, time_str: str) -> int:
        """解析时间字符串为分钟数"""
        import re
        hour_match = re.search(r'(\d+)时', time_str)
        minute_match = re.search(r'(\d+)分', time_str)

        hours = int(hour_match.group(1)) if hour_match else 0
        minutes = int(minute_match.group(1)) if minute_match else 0

        return hours * 60 + minutes

    @property
    def priority_name(self) -> str:
        """获取优先级中文名称"""
        names = {TaskPriority.RED: "红箱", TaskPriority.BLUE: "蓝箱", TaskPriority.GREEN: "绿箱"}
        return names[self.priority]

    def to_dict(self) -> dict:
        """转换为字典，用于配置保存"""
        return {
            'name': self.name,
            'time': self.time,
            'soul_jade_amount': self.soul_jade_amount,
            'priority': self.priority.value,
            'created_at': self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'MissionTask':
        """从字典创建任务对象"""
        task = cls(
            name=data['name'],
            time=data['time'],
            soul_jade_amount=data.get('soul_jade_amount', 0),
            priority=TaskPriority(data.get('priority', TaskPriority.GREEN.value))
        )
        if 'created_at' in data:
            task.created_at = datetime.fromisoformat(data['created_at'])
        return task

    def __str__(self):
        return f"任务: {self.name}, 时间: {self.time}分钟, 魂玉: {self.soul_jade_amount}, 优先级: {self.priority_name}"

