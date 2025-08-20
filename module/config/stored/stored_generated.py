from module.config.stored.classes import (
    StoredBase,
    StoredBattleOrderRank,
    StoredBattlePassLevel,
    StoredCounter,
    StoredDailyActivity,
    StoredDuel,
    StoredDungeon,
    StoredExpiredAt0500,
    StoredExpiredAtMonday0500,
    StoredInt,
    StoredPlanner,
    StoredPlannerOverall,
    StoredTrailblazePower,
)


# This file was auto-generated, do not modify it manually. To generate:
# ``` python -m module/config/config_updater.py ```

class StoredGenerated:
    DuelDaily = StoredDuel("Duel.DuelStorage.DuelDaily")
    Dungeon = StoredDungeon("TiLi.TiLiStorage.Dungeon")
    BattleOrderRank = StoredBattleOrderRank("BattleOrder.BattleOrderStorage.BattleOrderRank")
