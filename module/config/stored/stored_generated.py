from module.config.stored.classes import (
    StoredAccountName,
    StoredBase,
    StoredBattleFieldCount,
    StoredBattleOrderActivityPoints,
    StoredBattleOrderRank,
    StoredBattleOrderTaskProgress,
    StoredBattlePassLevel,
    StoredCounter,
    StoredDailyActivity,
    StoredDailyShareFinishCount,
    StoredDuel,
    StoredDuelCurrentVictory,
    StoredDungeon,
    StoredExpiredAt0500,
    StoredExpiredAtMonday0500,
    StoredFriendGiftsFinishCount,
    StoredInformationClubSignInCount,
    StoredInt,
    StoredJiFenSaiRewardClaimCount,
    StoredLeaderBoardLikeCount,
    StoredMailRewardClaimCount,
    StoredMiJingCount,
    StoredMissionAccept,
    StoredMonthlySignInCount,
    StoredPanRenCount,
    StoredPlanner,
    StoredPlannerOverall,
    StoredPrivilegeStoreFinishCount,
    StoredPrivilegeWeeklyPackageClaimCount,
    StoredSquadRaidFinishCount,
    StoredTiLi,
    StoredTrailblazePower,
    StoredYiLeLaMianClaimCount,
    StoredZhaoCaiFinishCount,
)


# This file was auto-generated, do not modify it manually. To generate:
# ``` python -m module/config/config_updater.py ```

class StoredGenerated:
    AccountName = StoredAccountName("Restart.AccountStorage.AccountName")
    DuelDaily = StoredDuel("Duel.Duel.DuelDaily")
    CurrentVictoryCount = StoredDuelCurrentVictory("Duel.Duel.CurrentVictoryCount")
    SquadRaidFinishedCount = StoredSquadRaidFinishCount("SquadRaid.SquadRaid.SquadRaidFinishedCount")
    Dungeon = StoredDungeon("TiLi.TiLiStorage.Dungeon")
    MissionAccept = StoredMissionAccept("Mission.MissionStorage.MissionAccept")
    MiJingCount = StoredMiJingCount("MiJing.MiJingStorage.MiJingCount")
    JiFenSaiDailyRewardClaim = StoredJiFenSaiRewardClaimCount("JiFenSai.JiFenSaiStorage.JiFenSaiDailyRewardClaim")
    FriendGiftsFinishCount = StoredFriendGiftsFinishCount("Freebies.FriendGifts.FriendGiftsFinishCount")
    DailyShareFinishCount = StoredDailyShareFinishCount("Freebies.DailyShare.DailyShareFinishCount")
    MailRewardFinishCount = StoredMailRewardClaimCount("Freebies.MailReward.MailRewardFinishCount")
    PrivilegPackageFinishCount = StoredPrivilegeWeeklyPackageClaimCount("Freebies.PrivilegeWeeklyPackage.PrivilegPackageFinishCount")
    ZhaoCaiFinishCount = StoredZhaoCaiFinishCount("Freebies.ZhaoCai.ZhaoCaiFinishCount")
    LeaderBoardFinishCount = StoredLeaderBoardLikeCount("Freebies.LeaderBoard.LeaderBoardFinishCount")
    MonthlySignInFinishCount = StoredMonthlySignInCount("Freebies.MonthlySignIn.MonthlySignInFinishCount")
    InformationClubSignInCount = StoredInformationClubSignInCount("Freebies.InformationClub.InformationClubSignInCount")
    YiLeLaMianFinishCount = StoredYiLeLaMianClaimCount("Freebies.YiLeLaMian.YiLeLaMianFinishCount")
    PrivilegeStoreFinishCount = StoredPrivilegeStoreFinishCount("StorePurchase.PrivilegeStore.PrivilegeStoreFinishCount")
    BattleOrderRank = StoredBattleOrderRank("BattleOrder.BattleOrderStorage.BattleOrderRank")
    BattleOrderActivityPoints = StoredBattleOrderActivityPoints("BattleOrder.BattleOrderStorage.BattleOrderActivityPoints")
    BattleOrderTaskProgress = StoredBattleOrderTaskProgress("BattleOrder.BattleOrderStorage.BattleOrderTaskProgress")
    TiLi = StoredTiLi("DataUpdate.ItemStorage.TiLi")
    Golds = StoredInt("DataUpdate.ItemStorage.Golds")
    Coins = StoredInt("DataUpdate.ItemStorage.Coins")
    Fame = StoredInt("DataUpdate.ItemStorage.Fame")
    PanRenFinishCount = StoredPanRenCount("PanRen.PanRen.PanRenFinishCount")
    BattleFieldFinishCount = StoredBattleFieldCount("BattleField.BattleField.BattleFieldFinishCount")
