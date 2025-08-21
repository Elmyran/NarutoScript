from dataclasses import dataclass

from module.ocr.keyword import Keyword

from typing import ClassVar
@dataclass
class OrganizationKeyword(Keyword):
    instances: ClassVar = {}
ReplacementHaveClaimedKeyword = OrganizationKeyword(
    id=0,
    name='HaveClaimed',
    cn='已领取',            # 简体中文
    cht='已領取',            # 繁體中文
    en='Claimed',            # 英文
    jp='受け取り済み',        # 日文
    es='Reclamado'           # 西班牙文
)
ReplacementClaimKeyword = OrganizationKeyword(
    id=0,
    name='Claim',
    cn='领取',              # 简体中文
    cht='領取',              # 繁體中文
    en='Claim',             # 英文
    jp='受け取る',            # 日文
    es='Reclamar'           # 西班牙文
)
