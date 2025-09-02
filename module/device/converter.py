class ResolutionConverter:
    def __init__(self, target_width, target_height):
        self.scale_x = target_width / 1280
        self.scale_y = target_height / 720

    def convert_to_target(self, x, y):
        """将1280x720坐标转换为目标分辨率坐标"""
        return int(x * self.scale_x), int(y * self.scale_y)

    def convert_from_target(self, x, y):
        """将目标分辨率坐标转换为1280x720坐标"""
        return int(x / self.scale_x), int(y / self.scale_y)