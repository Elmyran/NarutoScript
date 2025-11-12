from dataclasses import dataclass
from typing import ClassVar

from module.ocr.keyword import Keyword


@dataclass
class ExperienceCard(Keyword):
    instances: ClassVar = {}
Owned=ExperienceCard(
    id=1,
    name='Owned',
    cn='已拥有',
    en='Owned',
    cht='已擁有',
    jp='所持中',
    es='Obtenido',
)
Unowned=ExperienceCard(
    id=2,
    name='Unowned',
    cn='未拥有',
    en='Unowned',
    cht='未擁有',
    jp='未所持',
    es='No obtenido',
)