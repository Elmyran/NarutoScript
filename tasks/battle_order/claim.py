from module.logger.logger import logger 
from module.base.timer import Timer
from tasks.base.assets.assets_base_page import BATTLE_ORDER_CHECK
from tasks.base.page import page_battle_order
from tasks.base.ui import UI
from tasks.battle_order.assets.assets_battle_order_claim import *
import cv2
from tasks.battle_order.ui.draglist import *
from tasks.base.character_keyword import ACharacterTab,  OcrCharacterTab,  SCharacterTab
from tasks.battle_order.keyword.keywords import ExperienceCard
from tasks.battle_order.ui.switch import BATTLE_ORDER_TAB
from module.base.button import ClickButton  
import numpy as np
class BattleOrderClaim(UI):
    def run(self):
        if not self.config.BattleOrder_ClaimReward:
            return
        self.handle_battle_order_claim()

        
    def handle_battle_order_claim(self):
        self.device.click_record_clear()
        self.ui_ensure(page_battle_order)
        BATTLE_ORDER_TAB.set('奖励',main=self)
        click_interval=Timer(1)
        time=Timer(2,4).start()
        self.screenshot_tracking_add()  
        for _ in self.loop():
            if time.reached():
                logger.info('Battle Order Reward Claim Timeout')
                self.screenshot_tracking_add()  
                break
            if self.appear(BATTLE_ORDER_CHARACTER_SELECT_CHECK,interval=0):
                time.clear()
                self._character_fragments_select()
                time.start()
                continue
            if self.appear_then_click(BATTLE_ORDER_CLAIM_ALL,interval=0):
                time.reset()
                continue
            if self.appear_then_click(BATTLE_ORDER_REWARD_CLAIM_SUCCESS,interval=0):
                time.reset()
                continue
            rewards=self.detect_reward_boxes(image=self.device.image,button=BATTLE_ORDER_REWARD_CLAIM_AREA)
            if rewards and len(rewards)!=0:
                logger.info(f"Detect {len(rewards)} Claimable Reward ")
                if click_interval.reached():
                    self.device.click(rewards[0])
                    click_interval.reset()          
                time.reset()
    def _character_fragments_select(self):
        ocr=OcrCharacterTab(BATTLE_ORDER_CHARACTER_LIST_AREA)
        experience_card=False
        if ocr.matched_ocr(self.device.image,ExperienceCard):
            experience_card=True
        
        if ocr.matched_ocr(self.device.image,SCharacterTab):
            if experience_card:
                name=self.config.BattleOrder_SExperienceCard
            else:
                name=self.config.BattleOrder_SCharacterFragments
            draglist=S_CHARACTER_TAB_LIST
        elif ocr.matched_ocr(self.device.image,ACharacterTab):
            if experience_card:
                name=self.config.BattleOrder_AExperienceCard
            else:
                name=self.config.BattleOrder_ACharacterFragments
            draglist=A_CHARACTER_TAB_LIST
        else:
            name= self.config.BattleOrder_CCharacterFragments
            draglist=C_CHARACTER_TAB_LIST
        keyword=self.find_character_by_cn(name)
        draglist.search_rows(main=self,keyword=keyword)
        for _ in self.loop():
            if BATTLE_ORDER_CHECK.match_color(self.device.image):
                break
            if self.appear_then_click(BATTLE_ORDER_REWARD_CLAIM_SUCCESS,interval=1):
                continue
            if self.appear_then_click(BATTLE_ORDER_CHARACTER_SELECT_CONFIRM,interval=1):
                continue

        # 通过中文名称查找对应的关键词对象
    def find_character_by_cn(self,chinese_name):
        for character in SCharacterTab.instances.values():
            if character.cn == chinese_name:
                return character
            if character.card == chinese_name:
                return character
        for character in ACharacterTab.instances.values():
            if character.cn == chinese_name:
                return character
            if character.card == chinese_name:
                return character
        for character in CCharacterTab.instances.values():
            if character.cn == chinese_name:
                return character
        return None
    def is_claimable_single_frame(self, image, roi, v_thresh=125, ratio_thresh=0.4, mean_v_thresh=125,debug=False):
        
        x1, y1, x2, y2 = roi
        image = image[y1:y2, x1:x2]
        if image.size == 0:
            return False
        
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        s = hsv[:, :, 1]
        v = hsv[:, :, 2]

        # 高亮像素比例
        high_mask = v > v_thresh
        ratio = np.sum(high_mask) / high_mask.size if high_mask.size > 0 else 0.0

        # 平均亮度
        valid_mask = ~((s < 30) & (v > 220))
        mean_v = np.mean(v[valid_mask]) if np.any(valid_mask) else np.mean(v)
        if debug:
            logger.info(f"奖励区域: {roi}")
            logger.info(f"高亮像素占比: {ratio:.2f}, 平均亮度: {mean_v:.2f}")

        return (ratio > ratio_thresh) and (mean_v > mean_v_thresh)


  
    def detect_reward_boxes(self, image, button, debug=False):
        """
        检测可领取奖励按钮并返回原图坐标列表
        """
        edges=self.image_preprocess(image,button)
        # 获取可领取轮廓
        boxes = self.filter_contours(edges=edges,button=button,debug=debug)

        if debug:
            image_debug = cv2.cvtColor(image.copy(), cv2.COLOR_RGB2BGR)
            for box in boxes:
                cv2.rectangle(image_debug, (box.button[0],box.button[1]),(box.button[2],box.button[3]), (0, 255, 0), 2)
            cv2.imshow("Edges", edges)
            cv2.imshow("Detected Boxes", image_debug)
            cv2.waitKey(0)
       

        return boxes
    def image_preprocess(self,image,button):
        x1, y1, x2, y2 = button.area
        row=image.copy()
        image = row[y1:y2, x1:x2] 
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (1,1), 0)   
        # Canny 检测边缘
        edges = cv2.Canny(blur, 50, 150)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        # 3. 找轮廓
        contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        mask = np.zeros_like(closed)
        for cnt in contours:
            hull = cv2.convexHull(cnt)
            cv2.drawContours(mask, [hull], -1, 255, thickness=1)  
        return mask
      
    def filter_contours(self,edges,button,min_area=2000,max_area=7500,min_rect_ratio=0.7,debug=False):
        bx1, by1, bx2, by2 = button.area
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        filtered = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < min_area :
                if debug:
                    print(f"skip small area: {area}")
                continue
            if area  > max_area:
                if debug:
                    print(f"skip large area: {area}")
                continue
            
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box_area = cv2.contourArea(np.int0(box))
            if box_area == 0:
                continue
            rect_ratio = area / box_area
            if rect_ratio < min_rect_ratio:
                print(f"skip small rect: {rect_ratio}")
                continue

            # 轮廓在局部图像坐标
            x, y, w, h = cv2.boundingRect(cnt)
            if h< button.button[3] - button.button[1]-5:
                print(f"skip small height: {h}")
                continue

            # 原图坐标
            x1_abs = x + bx1
            y1_abs = y + by1
            x2_abs = x + w + bx1
            y2_abs = y + h + by1
            button_area=(x1_abs, y1_abs, x2_abs, y2_abs)
            if self.is_claimable_single_frame(self.device.image, button_area,debug):
                button=ClickButton(area=button_area)
                if debug:
                    logger.info(f'矩形:{rect_ratio}')
                filtered.append(button)
        filtered.sort(key=lambda b: b.area[0])
        return filtered
 