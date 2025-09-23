from dataclasses import dataclass
from module.ocr.keyword import Keyword
from typing import ClassVar
@dataclass
class BattleFieldKeyword(Keyword):
    instances: ClassVar = {}
AccountNameKeyword = BattleFieldKeyword(
    id=0,
    name='AccountName',
    cn='名字',            # 简体中文
    cht='名字',            # 繁體中文
    en='名字',            # 英文
    jp='名字',        # 日文
    es='名字'           # 西班牙文
)