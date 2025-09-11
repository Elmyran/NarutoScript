from module.config.stored.classes import (
    StoredAccountName,
    StoredBase,
    StoredBattleFieldCount,
    StoredBattleOrderRank,
    StoredBattlePassLevel,
    StoredCounter,
    StoredDailyActivity,
    StoredDuel,
    StoredDuelCurrentVictory,
    StoredDungeon,
    StoredExpiredAt0500,
    StoredExpiredAtMonday0500,
    StoredFreebiesWeeklyPackage,
    StoredInt,
    StoredJiFenSaiRewardClaimCount,
    StoredMiJingCount,
    StoredMissionAccept,
    StoredPanRenCount,
    StoredPlanner,
    StoredPlannerOverall,
    StoredTiLi,
    StoredTrailblazePower,
)


# This file was auto-generated, do not modify it manually. To generate:
# ``` python -m module/config/config_updater.py ```

class StoredGenerated:
    AccountName = StoredAccountName("Restart.AccountStorage.AccountName")
    DuelDaily = StoredDuel("Duel.Duel.DuelDaily")
    CurrentVictoryCount = StoredDuelCurrentVictory("Duel.Duel.CurrentVictoryCount")
    Dungeon = StoredDungeon("TiLi.TiLiStorage.Dungeon")
    MissionAccept = StoredMissionAccept("Mission.MissionStorage.MissionAccept")
    MiJingCount = StoredMiJingCount("MiJing.MiJingStorage.MiJingCount")
    JiFenSaiDailyRewardClaim = StoredJiFenSaiRewardClaimCount("JiFenSai.JiFenSaiStorage.JiFenSaiDailyRewardClaim")
    TiLi = StoredTiLi("DataUpdate.ItemStorage.TiLi")
    Golds = StoredInt("DataUpdate.ItemStorage.Golds")
    Tickets = StoredInt("DataUpdate.ItemStorage.Tickets")
    Coins = StoredInt("DataUpdate.ItemStorage.Coins")
    Fame = StoredInt("DataUpdate.ItemStorage.Fame")
    Mission = StoredMissionAccept("DataUpdate.ItemStorage.Mission")
    WeeklyPackage = StoredFreebiesWeeklyPackage("Freebies.FreebiesStorage.WeeklyPackage")
    BattleOrderRank = StoredBattleOrderRank("BattleOrder.BattleOrderStorage.BattleOrderRank")
    PanRenFinishCount = StoredPanRenCount("PanRen.PanRen.PanRenFinishCount")
    BattleFieldFinishCount = StoredBattleFieldCount("BattleField.BattleField.BattleFieldFinishCount")
