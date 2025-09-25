

from calendar import c
from datetime import datetime
from functools import cached_property as functools_cached_property

from anyio import value
from shapely import length

from module.base.decorator import cached_property
from module.config.deep import deep_get
from module.config.utils import DEFAULT_TIME, get_server_last_monday_update, get_server_last_update



def now():
    return datetime.now().replace(microsecond=0)


def iter_attribute(cls):
    """
    Args:
        cls: Class or object

    Yields:
        str, obj: Attribute name, attribute value
    """
    for attr in dir(cls):
        if attr.startswith('_'):
            continue
        value = getattr(cls, attr)
        if type(value).__name__ in ['function', 'property']:
            continue
        yield attr, value


class StoredBase:
    time = DEFAULT_TIME

    def __init__(self, key):
        self._key = key
        self._config = None

    @cached_property
    def _name(self):
        return self._key.split('.')[-1]

    def _bind(self, config):
        """
        Args:
            config (AzurLaneConfig):
        """
        self._config = config

    @functools_cached_property
    def _stored(self):
        assert self._config is not None, 'StoredBase._bind() must be called before getting stored data'
        from module.logger import logger

        out = {}
        stored = deep_get(self._config.data, keys=self._key, default={})
        for attr, default in self._attrs.items():
            value = stored.get(attr, default)
            if attr == 'time':
                if not isinstance(value, datetime):
                    try:
                        value = datetime.fromisoformat(value)
                    except ValueError:
                        logger.warning(f'{self._name} has invalid attr: {attr}={value}, use default={default}')
                        value = default
            else:
                if not isinstance(value, type(default)):
                    logger.warning(f'{self._name} has invalid attr: {attr}={value}, use default={default}')
                    value = default

            out[attr] = value
        return out

    @cached_property
    def _attrs(self) -> dict:
        """
        All attributes defined
        """
        attrs = {
            # time is the first one
            'time': DEFAULT_TIME
        }
        for attr, value in iter_attribute(self.__class__):
            if attr.islower():
                attrs[attr] = value
        return attrs

    def __setattr__(self, key, value):
        if key in self._attrs:
            stored = self._stored
            stored['time'] = now()
            stored[key] = value
            self._config.modified[self._key] = stored
            if self._config.auto_update:
                self._config.update()
        else:
            super().__setattr__(key, value)

    def __getattribute__(self, item):
        if not item.startswith('_') and item in self._attrs:
            return self._stored[item]
        else:
            return super().__getattribute__(item)

    def is_expired(self) -> bool:
        return False

    def show(self):
        """
        Log self
        """
        from module.logger import logger
        logger.attr(self._name, self._stored)


class StoredExpiredAt0500(StoredBase):
    def is_expired(self):
        from module.logger import logger
        self.show()
        expired = self.time < get_server_last_update('05:00')
        logger.attr(f'{self._name} expired', expired)
        return expired


class StoredExpiredAtMonday0500(StoredBase):
    def is_expired(self):
        from module.logger import logger
        self.show()
        expired = self.time < get_server_last_monday_update('05:00')
        logger.attr(f'{self._name} expired', expired)
        return expired


class StoredInt(StoredBase):
    value = 0

    def clear(self):
        self.value = 0


class StoredCounter(StoredBase):
    value = 0
    total = 0

    FIXED_TOTAL = 0

    def set(self, value, total=0):
        if self.FIXED_TOTAL:
            total = self.FIXED_TOTAL
        with self._config.multi_set():
            self.value = value
            self.total = total

    def clear(self):
        self.value = 0

    def to_counter(self) -> str:
        return f'{self.value}/{self.total}'

    def is_full(self) -> bool:
        return self.value >= self.total

    def get_remain(self) -> int:
        return self.total - self.value

    def add(self, value=1):
        self.value += value

    @cached_property
    def _attrs(self) -> dict:
        attrs = super()._attrs
        if self.FIXED_TOTAL:
            attrs['total'] = self.FIXED_TOTAL
        return attrs

    @functools_cached_property
    def _stored(self):
        stored = super()._stored
        if self.FIXED_TOTAL:
            stored['total'] = self.FIXED_TOTAL
        return stored


class StoredDailyActivity(StoredCounter, StoredExpiredAt0500):
    FIXED_TOTAL = 500


class StoredTrailblazePower(StoredCounter):
    FIXED_TOTAL = 300

    def predict_current(self) -> int:
        """
        Predict current stamina from records
        """
        # Overflowed
        value = self.value
        if value >= self.FIXED_TOTAL:
            return value
        # Invalid time, record in the future
        record = self.time
        now = datetime.now()
        if record >= now:
            return value
        # Calculate
        # Recover 1 trailbaze power each 6 minutes
        diff = (now - record).total_seconds()
        value += int(diff // 360)
        return value







class StoredBattlePassLevel(StoredCounter):
    FIXED_TOTAL = 70










class StoredPlanner(StoredBase):
    value: int
    total: int
    synthesize: int


class StoredPlannerOverall(StoredBase):
    value: str = '??%'
    comment: str = '<??d'
class StoredDungeon(StoredCounter, StoredExpiredAt0500):
    FIXED_TOTAL = 1
class StoredBattleOrderRank(StoredCounter,StoredExpiredAtMonday0500):
    FIXED_TOTAL = 1 # Weekly limit
class StoredDuel(StoredCounter,StoredExpiredAt0500):
    FIXED_TOTAL = 1
class StoredDuelCurrentVictory(StoredCounter, StoredExpiredAtMonday0500):
    value = 0
class StoredPanRenCount(StoredCounter, StoredExpiredAtMonday0500):
    FIXED_TOTAL = 2

class StoredJiFenSaiRewardClaimCount(StoredCounter,StoredExpiredAt0500):
    FIXED_TOTAL = 1
class StoredMiJingCount(StoredCounter, StoredExpiredAtMonday0500):
    value = 0
class StoredTiLi(StoredCounter):

    FIXED_TOTAL = 200
    def predict_current(self) -> int:
        """
        Predict current stamina from records
        """
        # Overflowed
        value = self.value
        if value >= self.FIXED_TOTAL:
            return value
        # Invalid time, record in the future
        record = self.time
        now = datetime.now()
        if record >= now:
            return value
        # Calculate
        # Recover 1 trailbaze power each 6 minutes
        diff = (now - record).total_seconds()
        value += int(diff // 360)
        return value
class StoredMissionAccept(StoredCounter):  
    value = 0  
    task1 = ''  
    task2 = ''  
    task3 = ''  
    task4 = ''  
    task5 = ''  
    task6 = ''  
    task7 = ''  
    task8 = ''  
    task9 = ''  
    FIXED_TOTAL = 9  
      
    def write_missions(self, duration_minutes_list):    
        from datetime import datetime, timedelta    
          
        # 1. 先清除已过期的任务时间  
        self._clear_expired_missions()  
          
        # 2. 计算新任务的完成时间  
        current_time = datetime.now()  
        new_completion_times = []  
        for minutes in duration_minutes_list:  
            completion_time = current_time + timedelta(minutes=minutes)  
            new_completion_times.append(completion_time.isoformat())  
          
        # 3. 找到空闲的task字段并写入   
        with self._config.multi_set():  
            written_count = 0  
            for i in range(9):  # task1-task9  
                task_attr = f'task{i+1}'  
                current_value = getattr(self, task_attr, '')  
                  
                # 如果该字段为空，且还有新任务需要写入  
                if not current_value and written_count < len(new_completion_times):  
                    setattr(self, task_attr, new_completion_times[written_count])  
                    written_count += 1  
  
    def _clear_expired_missions(self):  
        """清除所有过期的任务时间"""  
        from datetime import datetime  
        now = datetime.now()  

        with self._config.multi_set():  
            for i in range(9):  
                task_attr = f'task{i+1}'  
                task_time = getattr(self, task_attr, '')  
                if task_time:  
                    try:  
                        completion_time = datetime.fromisoformat(task_time)  
                        if completion_time <= now:  # 已过期  
                            setattr(self, task_attr, '')  
                    except (ValueError, TypeError):  
                        # 无效时间格式，清除  
                        setattr(self, task_attr, '')  
          
    def get_nearest_completion_time(self):  
        """获取最近的任务完成时间"""  
        from datetime import datetime  
        now = datetime.now()  
        valid_times = []  
          
        for i in range(9):  
            task_time = getattr(self, f'task{i+1}', '')  
            if not task_time:  
                continue  
            try:  
                completion_time = datetime.fromisoformat(task_time)  
                if completion_time > now:  
                    valid_times.append(completion_time)  
            except (ValueError, TypeError):  
                continue  
          
        return min(valid_times) if valid_times else None            
    def clear(self):  
        """清除所有任务数据"""  
        with self._config.multi_set():  
            for i in range(9):  
                setattr(self, f'task{i+1}', '')
class StoredBattleFieldCount(StoredCounter,StoredExpiredAtMonday0500):
    FIXED_TOTAL = 1
class StoredAccountName(StoredBase):
    value = ''
class StoredBattleOrderActivityPoints(StoredCounter,StoredExpiredAtMonday0500):
    value = 0
    FIXED_TOTAL=300
class StoredBattleOrderTaskProgress(StoredCounter,StoredExpiredAtMonday0500):
    value = 0
    FIXED_TOTAL=3500
class StoredMonthlySignInCount(StoredCounter,StoredExpiredAt0500):
    value = 0
    FIXED_TOTAL = 1
class StoredLeaderBoardLikeCount(StoredCounter,StoredExpiredAt0500):
    value = 0
    FIXED_TOTAL = 1
class StoredDailyShareFinishCount(StoredCounter,StoredExpiredAt0500):
    value = 0
    FIXED_TOTAL = 1
class StoredMailRewardClaimCount(StoredCounter,StoredExpiredAt0500):
   value=0
   FIXED_TOTAL = 1
class StoredFriendGiftsFinishCount(StoredCounter,StoredExpiredAt0500):
    value = 0
    FIXED_TOTAL = 1
class StoredPrivilegeWeeklyPackageClaimCount(StoredCounter,StoredExpiredAtMonday0500):
    value = 0
    FIXED_TOTAL = 1
class StoredInformationClubSignInCount(StoredCounter,StoredExpiredAt0500):
    value = 0
    FIXED_TOTAL = 1
class StoredZhaoCaiFinishCount(StoredCounter,StoredExpiredAt0500):
    value = 0
    FIXED_TOTAL = 1
class StoredYiLeLaMianClaimCount(StoredCounter,StoredExpiredAt0500):
    value = 0
    FIXED_TOTAL = 1
class StoredPrivilegeStoreFinishCount(StoredCounter,StoredExpiredAt0500):
    value = 0
    FIXED_TOTAL = 1
   
    