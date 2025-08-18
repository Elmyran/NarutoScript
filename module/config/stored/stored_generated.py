from module.config.stored.classes import (
    StoredBase,
    StoredBattlePassLevel,
    StoredCounter,
    StoredDailyActivity,
    StoredDungeon,
    StoredExpiredAt0500,
    StoredExpiredAtMonday0500,
    StoredInt,
    StoredPlanner,
    StoredPlannerOverall,
    StoredTrailblazePower, SortedBattleOrderRank,
)


# This file was auto-generated, do not modify it manually. To generate:
# ``` python -m module/config/config_updater.py ```

class StoredGenerated:
    Dungeon = StoredDungeon("TiLi.TiLiStorage.Dungeon")
    BattleOrderRank = SortedBattleOrderRank("BattleOrder.BattleOrderStorage.BattleOrderRank")
