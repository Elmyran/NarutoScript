from module.base.timer import Timer
from module.logger import logger
from tasks.base.assets.assets_base_move import CHOOSE_RIGHT
from tasks.base.ui import UI


class SimpleRightMover(UI):
    def move_right_until_condition(self, stop_condition_check):
        """
        向右移动直到满足停止条件

        Args:
            stop_condition_check: 一个返回布尔值的函数，用于检查停止条件
        """
        interval = Timer(2)  # 2秒间隔防止过快点击
        timeout = Timer(30, count=60).start()  # 30秒超时

        while True:
            if timeout.reached():
                logger.warning("向右移动超时")
                break

            self.device.screenshot()

            # 检查停止条件
            if stop_condition_check():
                logger.info("检测到停止条件，停止移动")
                break

                # 向右移动
            if interval.reached():
                self.device.click(CHOOSE_RIGHT)
                interval.reset()
                logger.info("向右移动一次")