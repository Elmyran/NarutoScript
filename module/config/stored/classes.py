from datetime import datetime
from functools import cached_property as functools_cached_property

from module.base.decorator import cached_property
from module.config.deep import deep_get
from module.config.utils import DEFAULT_TIME, get_server_last_monday_update, get_server_last_update
from module.exception import ScriptError


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
    FIXED_TOTAL = 1 # Weekly limit