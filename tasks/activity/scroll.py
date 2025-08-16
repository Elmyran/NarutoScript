# 创建 AdaptiveScroll 实例
from module.ui.scroll import AdaptiveScroll
from tasks.activity.assets.assets_activity import ACTIVITY_LIST_AREA

class ActivityAdaptiveScroll(AdaptiveScroll):
    def at_bottom(self, main):
        # Use the actual maximum position (0.5) as bottom
        current_pos = self.cal_position(main)
        return current_pos >= 0.45  # Slightly less than 0.5 to allow some tolerance

    def set_bottom(self, main, random_range=(-0.05, 0.05), skip_first_screenshot=True):
        return self.set(0.5, main=main, random_range=random_range, skip_first_screenshot=skip_first_screenshot)