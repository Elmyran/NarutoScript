from module.config.stored.classes import (
    StoredAccountName,
    StoredActivityProgressToday,
    StoredActivityProgressTodayCount,
    StoredActivityProgressWeekly,
    StoredActivityProgressWeeklyCount,
    StoredBase,
    StoredBattleFieldCount,
    StoredBattleOrderActivityProgress,
    StoredBattleOrderRank,
    StoredBattleOrderTaskProgress,
    StoredBattlePassLevel,
    StoredCounter,
    StoredDailyActivity,
    StoredDailyShareFinishCount,
    StoredDuel,
    StoredDuelCurrentVictory,
    StoredDuelExtendedScore,
    StoredDungeon,
    StoredExpiredAt0500,
    StoredExpiredAtMonday0500,
    StoredFriendGiftsFinishCount,
    StoredInformationClubSignInCount,
    StoredInt,
    StoredLeaderBoardLikeCount,
    StoredMailRewardClaimCount,
    StoredMiJingCount,
    StoredMiJingTicket,
    StoredMissionAccept,
    StoredMonthlySignInCount,
    StoredOrganizationPrayCount,
    StoredPanRenCount,
    StoredPlanner,
    StoredPlannerOverall,
    StoredPrivilegeStoreFinishCount,
    StoredPrivilegeWeeklyPackageClaimCount,
    StoredSquadRaidFinishCount,
    StoredTiLi,
    StoredTiLiPurchaseCount,
    StoredTrailblazePower,
    StoredYiLeLaMianClaimCount,
    StoredZhaoCaiFinishCount,
)


# This file was auto-generated, do not modify it manually. To generate:
# ``` python -m module/config/config_updater.py ```

class StoredGenerated:
    DuelDaily = StoredDuel("Duel.DuelWeekly.DuelDaily")
    CurrentVictoryCount = StoredDuelCurrentVictory("Duel.DuelWeekly.CurrentVictoryCount")
    ExtendedCurrentScore = StoredDuelExtendedScore("Duel.DuelExtended.ExtendedCurrentScore")
    SquadRaidFinishedCount = StoredSquadRaidFinishCount("SquadRaid.SquadRaid.SquadRaidFinishedCount")
    TiLiPurchaseFinishCount = StoredTiLiPurchaseCount("TiLi.TiLiPurchase.TiLiPurchaseFinishCount")
    Dungeon = StoredDungeon("TiLi.TiLiStorage.Dungeon")
    MissionAccept = StoredMissionAccept("Mission.MissionStorage.MissionAccept")
    MiJingTicket = StoredMiJingTicket("MiJing.MiJingCount.MiJingTicket")
    MiJingCount = StoredMiJingCount("MiJing.MiJingStorage.MiJingCount")
    FriendGiftsFinishCount = StoredFriendGiftsFinishCount("Freebies.Freebies.FriendGiftsFinishCount")
    DailyShareFinishCount = StoredDailyShareFinishCount("Freebies.Freebies.DailyShareFinishCount")
    MailRewardFinishCount = StoredMailRewardClaimCount("Freebies.Freebies.MailRewardFinishCount")
    LeaderBoardFinishCount = StoredLeaderBoardLikeCount("Freebies.Freebies.LeaderBoardFinishCount")
    InformationClubSignInCount = StoredInformationClubSignInCount("Freebies.Freebies.InformationClubSignInCount")
    YiLeLaMianFinishCount = StoredYiLeLaMianClaimCount("Freebies.Freebies.YiLeLaMianFinishCount")
    MonthlySignInFinishCount = StoredMonthlySignInCount("Freebies.Freebies.MonthlySignInFinishCount")
    OrganizationPrayFinishCount = StoredOrganizationPrayCount("Freebies.Freebies.OrganizationPrayFinishCount")
    PrivilegPackageFinishCount = StoredPrivilegeWeeklyPackageClaimCount("Freebies.PrivilegeWeeklyPackage.PrivilegPackageFinishCount")
    ZhaoCaiFinishCount = StoredZhaoCaiFinishCount("Freebies.ZhaoCai.ZhaoCaiFinishCount")
    PrivilegeStoreFinishCount = StoredPrivilegeStoreFinishCount("StorePurchase.PrivilegeStore.PrivilegeStoreFinishCount")
    ActivityProgressToday = StoredActivityProgressToday("StorePurchase.ActivityProgressStorage.ActivityProgressToday")
    ActivityProgressTodayCount = StoredActivityProgressTodayCount("StorePurchase.ActivityProgressStorage.ActivityProgressTodayCount")
    ActivityProgressWeekly = StoredActivityProgressWeekly("StorePurchase.ActivityProgressStorage.ActivityProgressWeekly")
    ActivityProgressWeeklyCount = StoredActivityProgressWeeklyCount("StorePurchase.ActivityProgressStorage.ActivityProgressWeeklyCount")
    BattleOrderRank = StoredBattleOrderRank("BattleOrder.BattleOrderStorage.BattleOrderRank")
    BattleOrderActivityProgress = StoredBattleOrderActivityProgress("BattleOrder.BattleOrderStorage.BattleOrderActivityProgress")
    BattleOrderTaskProgress = StoredBattleOrderTaskProgress("BattleOrder.BattleOrderStorage.BattleOrderTaskProgress")
    TiLi = StoredTiLi("DataUpdate.ItemStorage.TiLi")
    Golds = StoredInt("DataUpdate.ItemStorage.Golds")
    Coins = StoredInt("DataUpdate.ItemStorage.Coins")
    Fame = StoredInt("DataUpdate.ItemStorage.Fame")
    PanRenFinishCount = StoredPanRenCount("PanRen.PanRen.PanRenFinishCount")
    BattleFieldFinishCount = StoredBattleFieldCount("BattleField.BattleField.BattleFieldFinishCount")
