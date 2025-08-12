from module.base.base import ModuleBase
import numpy as np

class daily_utils(ModuleBase):
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
