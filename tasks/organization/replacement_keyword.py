from dataclasses import dataclass
from module.ocr.keyword import Keyword
from typing import ClassVar
@dataclass
class OrganizationClaimStatusKeyword(Keyword):
    instances: ClassVar = {}
ReplacementHaveClaimedKeyword = OrganizationClaimStatusKeyword(
    id=0,
    name='HaveClaimed',
    cn='已领取',            # 简体中文
    cht='已領取',            # 繁體中文
    en='Claimed',            # 英文
    jp='受け取り済み',        # 日文
    es='Reclamado'           # 西班牙文
)
ReplacementClaimKeyword = OrganizationClaimStatusKeyword(
    id=1,
    name='Claim',
    cn='领取',              # 简体中文
    cht='領取',              # 繁體中文
    en='Claim',             # 英文
    jp='受け取る',            # 日文
    es='Reclamar'           # 西班牙文
)
