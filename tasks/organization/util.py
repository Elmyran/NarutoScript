DIC_OS_MAP = {
    0: {'cn': '铁之要塞', 'en': 'NY City', 'jp': 'NYシティ', 'tw': '紐約', 'area_pos': (830, 100), 'Level': 'Low'},
    1: {'cn': '田之要塞', 'en': 'NY City', 'jp': 'NYシティ', 'tw': '紐約', 'area_pos': (1180, 236), 'Level': 'Low'},
    2: {'cn': '土之要塞', 'en': 'NY City', 'jp': 'NYシティ', 'tw': '紐約', 'area_pos': (900, 460), 'Level': 'Medium'},
    3: {'cn': '熊之要塞', 'en': 'NY City', 'jp': 'NYシティ', 'tw': '紐約', 'area_pos': (408, 495), 'Level': 'Low'},
    4: {'cn': '汤之要塞', 'en': 'NY City', 'jp': 'NYシティ', 'tw': '紐約', 'area_pos': (1584, 197), 'Level': 'Low'},
    5: {'cn': '涡之要塞', 'en': 'NY City', 'jp': 'NYシティ', 'tw': '紐約', 'area_pos': (1965, 431), 'Level': 'Low'},
    6: {'cn': '霜之要塞', 'en': 'NY City', 'jp': 'NYシティ', 'tw': '紐約', 'area_pos': (2163, 465), 'Level': 'Low'},
    7: {'cn': '水之要塞', 'en': 'NY City', 'jp': 'NYシティ', 'tw': '紐約', 'area_pos': (1670, 521), 'Level': 'Medium'},
    8: {'cn': '火之要塞', 'en': 'NY City', 'jp': 'NYシティ', 'tw': '紐約', 'area_pos': (1221, 529), 'Level': 'High'},
    9: {'cn': '雨之要塞', 'en': 'NY City', 'jp': 'NYシティ', 'tw': '紐約', 'area_pos': (322, 950), 'Level': 'Low'},
    10: {'cn': '草之要塞', 'en': 'NY City', 'jp': 'NYシティ', 'tw': '紐約', 'area_pos': (289, 783), 'Level': 'Low'},
    11: {'cn': '川之要塞', 'en': 'NY City', 'jp': 'NYシティ', 'tw': '紐約', 'area_pos': (891, 972), 'Level': 'Low'},
    12: {'cn': '雷之要塞', 'en': 'NY City', 'jp': 'NYシティ', 'tw': '紐約', 'area_pos': (1118, 739), 'Level': 'Medium'},
    13: {'cn': '风之要塞', 'en': 'NY City', 'jp': 'NYシティ', 'tw': '紐約', 'area_pos': (741, 668), 'Level': 'Medium'},
    14: {'cn': '海之要塞', 'en': 'NY City', 'jp': 'NYシティ', 'tw': '紐約', 'area_pos': (582, 1010), 'Level': 'Low'},
    15: {'cn': '泷之要塞', 'en': 'NY City', 'jp': 'NYシティ', 'tw': '紐約', 'area_pos': (1492, 978), 'Level': 'Low'},
    16: {'cn': '云之要塞', 'en': 'NY City', 'jp': 'NYシティ', 'tw': '紐約', 'area_pos': (1788, 812), 'Level': 'Low'},
    17: {'cn': '鸟之要塞', 'en': 'NY City', 'jp': 'NYシティ', 'tw': '紐約', 'area_pos': (1984, 856), 'Level': 'Low'}
}
from module.base.base import ModuleBase
import numpy as np

class RewardUtils(ModuleBase):
    def create_circular_mask(self,h, w, center=None, radius=None):
        if center is None:  # use the middle of the image
            center = (int(w / 2), int(h / 2))
        if radius is None:  # use the smallest distance between the center and image walls
            radius = min(center[0], center[1], w - center[0], h - center[1])

        y, x = np.ogrid[:h, :w]
        dist_from_center = np.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2)

        mask = dist_from_center <= radius
        return mask
    def create_ring_mask(self,chest_area, inner_radius=30, outer_radius=50):
        """创建圆环遮罩，只检测周围金光"""
        # 获取宝箱中心点
        if hasattr(chest_area, 'area'):
            area_coords = chest_area.area
        else:
            area_coords = chest_area

        center_x = (area_coords[0] + area_coords[2]) // 2
        center_y = (area_coords[1] + area_coords[3]) // 2

        # 创建检测区域
        detection_area = (
            center_x - outer_radius,
            center_y - outer_radius,
            center_x + outer_radius,
            center_y + outer_radius
        )

        # 获取检测区域图像
        image = self.image_crop(detection_area, copy=False)
        h, w = image.shape[:2]

        # 创建外圆遮罩
        outer_mask = self.create_circular_mask(h, w, center=(w // 2, h // 2), radius=outer_radius)
        # 创建内圆遮罩
        inner_mask = self.create_circular_mask(h, w, center=(w // 2, h // 2), radius=inner_radius)

        # 圆环遮罩 = 外圆 - 内圆
        ring_mask = outer_mask & ~inner_mask

        return image, ring_mask, detection_area