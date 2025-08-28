from module.config.stored.classes import (
    StoredBase,
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
    StoredPanRenCount,
    StoredPlanner,
    StoredPlannerOverall,
    StoredTrailblazePower,
)


# This file was auto-generated, do not modify it manually. To generate:
# ``` python -m module/config/config_updater.py ```

class StoredGenerated:
    DuelDaily = StoredDuel("Duel.Duel.DuelDaily")
    CurrentVictoryCount = StoredDuelCurrentVictory("Duel.Duel.CurrentVictoryCount")
    Dungeon = StoredDungeon("TiLi.TiLiStorage.Dungeon")
    WeeklyPackage = StoredFreebiesWeeklyPackage("Freebies.FreebiesStorage.WeeklyPackage")
    BattleOrderRank = StoredBattleOrderRank("BattleOrder.BattleOrderStorage.BattleOrderRank")
    PanRenFinishCount = StoredPanRenCount("PanRen.PanRen.PanRenFinishCount")
