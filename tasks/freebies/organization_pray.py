from tasks.base.taskui import TaskUI
import cv2
import numpy as np
from module.base.timer import Timer
from module.base.utils import color_similarity_2d
from module.exception import GameStuckError
from tasks.base.assets.assets_base_popup import EXIT_ORGANIZATION_RED_ENVELOPE
from tasks.base.page import page_organization_panel
from tasks.base.taskui import TaskUI
from tasks.organization.assets.assets_organization_pray import *
from tasks.organization.assets.assets_organization_boxclaim import *
from tasks.organization.assets.assets_organization_replacement import *
from module.logger import  logger
class RewardUtils(TaskUI):
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


        outer_mask = self.create_circular_mask(h, w, center=(w // 2, h // 2), radius=outer_radius)
   
        inner_mask = self.create_circular_mask(h, w, center=(w // 2, h // 2), radius=inner_radius)

 
        ring_mask = outer_mask & ~inner_mask

        return image, ring_mask, detection_area

class OrganizationPray(RewardUtils):
    def run(self):
        if self.config.stored.OrganizationPrayFinishCount.is_expired():
            self.config.stored.OrganizationPrayFinishCount.clear()
        if self.config.stored.OrganizationPrayFinishCount.is_full():
            return True
        self.handle_Organization_Pray()
        self.config.stored.OrganizationPrayFinishCount.add()
   

    def handle_Organization_Pray(self):
        self.device.click_record_clear()
        self.ui_ensure(page_organization_panel)
        self._enter_pray_panel()
        self.pray()
        self.pray_box_claim()
        self._pray_box_replacement()
       


    def _enter_pray_panel(self):
        for _ in self.loop():
            if self.appear_then_click(ORGANIZATION_PLAY_PANEL,interval=1):
                continue
            if self.appear_then_click(ORGANIZATION_GOTO_PRAY,interval=1):
                continue
            if self.appear(ORGANIZATION_PRAY_CHECK):
                break


    def pray(self):
        time=Timer(20, count=30).start()
        for _ in self.loop():
            if time.reached():
                raise GameStuckError("Organization Pray Stucked")
            if self.appear(PRAY_SUCCESS):
                break
            if self.appear(PRAY_HAVE_DONE):
                break
            if self.appear_then_click(PRAY_BUTTON,interval=1):
                continue
        for _ in self.loop():
            if time.reached():
                raise GameStuckError("Organization Pray Exit Stucked")
            if self.appear_then_click(PRAY_SUCCESS,interval=0):
                continue
            if self.appear_then_click(PRAY_HAVE_DONE,interval=0):
                continue
            if self.appear(PRAY_BUTTON,interval=1):
                break



    def pray_box_claim(self):
        time=Timer(10, count=15).start()
        times=0
        for _ in self.loop():
            if not self.detect_golden_box():
                times += 1
                if times >=3:
                    break
            if time.reached():
                break
            if self.detect_ring_golden_glow(PRAY_BOX_CLAIM_15):
                self.device.click(PRAY_BOX_CLAIM_15)
                continue
            if self.detect_ring_golden_glow(PRAY_BOX_CLAIM_25):
                self.appear_then_click(PRAY_BOX_CLAIM_25)
                continue
            if self.appear_then_click(EXIT_ORGANIZATION_RED_ENVELOPE):
                continue







    def _pray_box_replacement(self):
        time=Timer(2, count=4).start()
        for _ in self.loop():
            if time.reached():
                logger.info('organization box replacement not detected')
                return
            if self.appear(PRAY_BOX_REPLACEMENT_CHECK):
                break
            if self.appear_then_click(PRAY_BOX_REPLACEMENT,interval=0):
                time.reset()
                continue
        claim_time=Timer(2, count=4).start()
        for _ in self.loop():
            if claim_time.reached():
                logger.info('pray box replacement not detected')
                break
            PRAY_BOX_REPLACEMENT_BUTTON.load_search(PRAY_BOX_REPLACEMENT_LIST.area)
            if self.appear_then_click(PRAY_BOX_REPLACEMENT_BUTTON,interval=0):
                claim_time.reset()
                continue




        #  0.01 30 60
    def detect_ring_golden_glow(self, chest_area, inner_radius=20, outer_radius=60):
        self.device.screenshot()
        """在圆环区域内检测金光效果"""
        image, ring_mask, detection_area = self.create_ring_mask(chest_area, inner_radius, outer_radius)

        # 检测金色区域
        golden_similarity = color_similarity_2d(image, color=(252, 209, 123))

        # 应用圆环遮罩
        masked_golden = cv2.bitwise_and(golden_similarity, golden_similarity, mask=ring_mask.astype(np.uint8))

        # 阈值化处理
        cv2.inRange(masked_golden, 200, 255, dst=masked_golden)

        # 统计圆环内的金光像素
        glow_pixels = cv2.countNonZero(masked_golden)
        ring_pixels = cv2.countNonZero(ring_mask.astype(np.uint8))

        # 计算金光像素占圆环面积的比例
        if ring_pixels > 0:
            glow_ratio = glow_pixels / ring_pixels
            print(glow_ratio)
            return glow_ratio > 0.02  # 5%以上认为有金光
    def detect_golden_box(self):
        not_golden_box=self.detect_ring_golden_glow(PRAY_BOX_CLAIM_15) or self.detect_ring_golden_glow(PRAY_BOX_CLAIM_25)
        return not_golden_box

