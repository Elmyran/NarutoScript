from module.ocr.keyword import Keyword
from dataclasses import dataclass
from typing import ClassVar
@dataclass
class StoreKeyword(Keyword):
    instances: ClassVar = {}

ThemeStore=StoreKeyword(
    id=1,
    name='ThemeStore',
    cn='主题商店',
    cht='主題商店',
    en='Theme Store',
    jp='テーマストア',
    es='Tienda de Temas',
)
Store=StoreKeyword(
    id=2,
    name='Store',
    cn='商店',
    cht='商店',
    en='Store',
    jp='ストア',
    es='Tienda',
)
PlayStore=StoreKeyword(
    id=3,
    name='PlayStore',
    cn='玩法商店',
    cht='玩法商店',
    en='Play Store',
    jp='プレイストア',
    es='Tienda de Juego',
)
RewardsStore=StoreKeyword(
    id=4,
    name='RewardsStore',
    cn='福利商店',
    cht='福利商店',
    en='Rewards Store',
    jp='報酬ストア',
    es='Tienda de Recompensas',
)
LimitedTimeSale=StoreKeyword(
    id=5,
    name='LimitedTimeSale',
    cn='限时特惠',
    cht='限時特惠',
    en='Limited-Time Sale',
    jp='期間限定セール',
    es='Oferta por Tiempo Limitado',
)

@dataclass
class SubsidiaryStoreKeyword(Keyword):
    instances: ClassVar = {}
FeaturedThisTime=SubsidiaryStoreKeyword(
    id=1,
    name='FeaturedThisTime',
    cn='本期推荐',
    cht='本期推荐',
    en='Featured This Time',
    jp='今回の特選',
    es='Destacado Esta Vez',
)
CharacterStore=SubsidiaryStoreKeyword(
    id=2,
    name='CharacterStore',
    cn='忍者商店',
    cht='忍者商店',
    en='Character Store',
    jp='キャラクターストア',
    es='Tienda de Personajes',
)
PrivilegeStore=SubsidiaryStoreKeyword(
    id=3,
    name='PrivilegeShop',
    cn='特权商店',
    cht='特权商店',
    en='Privilege Shop',
    jp='プレミアムストア',
    es='Tienda de Privilegios',
)
ItemStore=SubsidiaryStoreKeyword(
    id=4,
    name='ItemStore',
    cn='道具商店',
    cht='道具商店',
    en='Item Store',
    jp='アイテムストア',
    es='Tienda de Objetos',
)
AppearanceStore=SubsidiaryStoreKeyword(
    id=5,
    name='AppearanceStore',
    cn='装扮商店',
    cht='装扮商店',
    en='Appearance Store',
    jp='アパレルストア',
    es='Tienda de Apariencia',
)
TongLingStore=SubsidiaryStoreKeyword(
    id=7,
    name='TongLingStore',
    cn='通灵兽商店',
    cht='通灵兽商店',
    en='Summon Store',
    jp='サモンストア',
    es='Tienda de Invocación',
)
JadeStore=SubsidiaryStoreKeyword(
    id=8,
    name='JadeStore',
    cn='玉石商店',
    cht='玉石商店',
    en='Jade Store',
    jp='タローストア',
    es='Tienda de Jade',
)
RefreshTicketStore=SubsidiaryStoreKeyword(
    id=9,
    name='RefreshTicketStore',
    cn='刷新券商店',
    cht='刷新券商店',
    en='RefreshTicket Store',
    jp='ストアを更新',
    es='Actualizar Tienda',
)
SurvivalStore=SubsidiaryStoreKeyword(
    id=10,
    name='SurvivalStore',
    cn='生存商店',
    cht='生存商店',
    en='Survival Store',
    jp='サバイバルストア',
    es='Tienda de Supervivencia',
)
DuelStore=SubsidiaryStoreKeyword(
    id=11,
    name='DuelStore',
    cn='决斗商店',
    cht='決鬥商店',
    en='Duel Store',
    jp='デュエルストア',
    es='Tienda de Duelo',
)
ScoreStore=SubsidiaryStoreKeyword(
    id=12,
    name='ScoreStore',
    cn='积分赛商店',
    cht='积分赛商店',
    en='Score Store',
    jp='ランクストア',
    es='Tienda de Rango',
)
OrganizationStore=SubsidiaryStoreKeyword(
    id=13,
    name='OrganizationStore',
    cn='组织商店',
    cht='组织商店',
    en='Organization Store',
    jp='ギルドストア',  
    es='Tienda de Gremio',
)
MonthlyFortuneBag=SubsidiaryStoreKeyword(
    id=14,
    name='MonthlyFortuneBag',
    cn='每月福袋',
    cht='每月福袋',
    en='Monthly Fortune Bag',
    jp='月福袋ストア',
    es='Bolsa de Fortuna Mensual',
)
ChaoYingService=SubsidiaryStoreKeyword(
    id=15,
    name='ChaoYingService',
    cn='超影服务',
    cht='超影服務',
    en='ChaoYing Service',
    jp='超影サービス',
    es='Servicio de ChaoYing',
)
MightDiscount=SubsidiaryStoreKeyword(
    id=16,
    name='MightDiscount',
    cn='战力特惠',
    cht='战力特惠',
    en='Might Discount',
    jp='パワー割引',
    es='Descuento de Poder',
)
CharacterDiscount=SubsidiaryStoreKeyword(
    id=17,
    name='CharacterDiscount',
    cn='忍者特惠',
    cht='忍者特惠',
    en='Character Discount',
    jp='キャラクター割引',
    es='Descuento de Personaje',
)
LimitedAppearance=SubsidiaryStoreKeyword(
    id=18,
    name='LimitedAppearance',
    cn='限定装扮',
    cht='限定裝飾',
    en='Limited Appearance',
    jp='限定アパレル',
    es='Apariencia Limitada',
)
VPrivilegePack=SubsidiaryStoreKeyword(
    id=19,
    name='VPrivilegePack',
    cn='V特权礼包',
    cht='V特權禮包',
    en='V Privilege Pack',
    jp='Vプレミアムパック',
    es='Paquete de Privilegios V',
)