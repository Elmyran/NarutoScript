




from module.logger.logger import logger 
from module.base.timer import Timer
from tasks.base.assets.assets_base_page import BATTLE_ORDER_CHECK
from tasks.base.page import page_battle_order
from tasks.base.ui import UI
from tasks.battle_order.assets.assets_battle_order_claim import *
import cv2
from tasks.battle_order.draglist import *
from tasks.base.character_keyword import ACharacterTab,  OcrCharacterTab, SCharacterTab
from tasks.battle_order.switch import BATTLE_ORDER_TAB
from module.base.button import ClickButton  
from datetime import datetime  

class BattleOrderClaim(UI):
    def handle_battle_order_claim(self):
        self.device.click_record_clear()
        self.ui_ensure(page_battle_order)
        BATTLE_ORDER_TAB.set('奖励',main=self)
        time=Timer(1,3).start()
        for _ in self.loop():
            if time.reached():
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
            if self.interval_is_reached('claimable_click', interval=0.5):
                res,_=self.detect_reward_boxes(image=self.device.image,button=BATTLE_ORDER_REWARD_CLAIM_AREA)
                if res and len(res)!=0:
                        logger.info(f"Detect {len(res)} Claimable Reward ")
                        self.device.click(res[0])
                        self.interval_reset('claimable_click', interval=0.5)
                        time.reset()
    def _character_fragments_select(self):
        ocr=OcrCharacterTab(BATTLE_ORDER_CHARACTER_LIST_AREA)
        name=self.config.BattleOrder_SCharacterFragments
        draglist=S_CHARACTER_TAB_LIST
        if ocr.matched_ocr(self.device.image,SCharacterTab):
            pass
        elif ocr.matched_ocr(self.device.image,ACharacterTab):
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
            if self.appear_then_click(BATTLE_ORDER_REWARD_CLAIM_SUCCESS,interval=0):
                continue
            if self.appear_then_click(BATTLE_ORDER_CHARACTER_SELECT_CONFIRM):
                continue

        # 通过中文名称查找对应的关键词对象
    def find_character_by_cn(self,chinese_name):
        for character in SCharacterTab.instances.values():
            if character.cn == chinese_name:
                return character
        for character in ACharacterTab.instances.values():
            if character.cn == chinese_name:
                return character
        for character in CCharacterTab.instances.values():
            if character.cn == chinese_name:
                return character
        return None
    def is_claimable_single_frame(self, image, roi, v_thresh=125, ratio_thresh=0.4, mean_v_thresh=125):
        """
        平均亮度 + 白色过滤
        """
        import cv2
        import numpy as np

        x1, y1, x2, y2 = roi
        image = image[y1:y2, x1:x2]
        if image.size == 0:
            return False
        
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        s = hsv[:, :, 1]
        v = hsv[:, :, 2]

        # 高亮像素比例（未排白）
        high_mask = v > v_thresh
        ratio = np.sum(high_mask) / high_mask.size if high_mask.size > 0 else 0.0

        # 平均亮度（排除白色区域）
        valid_mask = ~((s < 30) & (v > 220))
        mean_v = np.mean(v[valid_mask]) if np.any(valid_mask) else np.mean(v)

      
        print(f"高亮像素占比: {ratio:.2f}, 平均亮度: {mean_v:.2f}")

        #  双条件判定
        return (ratio > ratio_thresh) and (mean_v > mean_v_thresh)

        
    def detect_reward_boxes(self, image, button, low=100, high=300):

       
        
        x1, y1, x2, y2 = button.area
        roi = image[y1:y2, x1:x2]   
        
        # 转灰度 + 高斯模糊
        gray = cv2.cvtColor(roi, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        # 边缘检测
        edges = cv2.Canny(blur, low, high)

        # 闭运算，连通边缘
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
        closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

        # 找轮廓（在 ROI 内）
        contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        box_width=80
        box_upper=525
        box_lower=603
        boxes = []
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            area = w * h
            ratio = w / float(h)
            
            max_w, max_h = 90, 80  
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            print(f"检测到轮廓: 面积={area}, 宽高比={ratio:.2f}, 顶点数={len(approx)}")
            # 矩形度过滤
            extent = cv2.contourArea(cnt) / float(w * h)
            print(f"矩形度: {extent:.2f}")
            if extent < 0.7 or extent > 1.05:
               continue
            
            ratio = w / float(h)
            if ratio > 1.05:
                continue
            # 过滤条件
            if w > 95:
                continue
            if h < 70 or h > 90:
                continue
            # 调整略大的框
            if w > max_w:
                over = w - max_w
                x += over // 2
                w -= over
            if h > max_h:
                over = h - max_h
                y += over // 2
                h -= over
            detected_right = x + x1 + w
            predicted_right = x + x1+ box_width
            #  把 ROI 坐标平移回全图
            #box=(x + x1, box_upper,min(predicted_right, detected_right),box_lower)
            box = (x + x1, y + y1, x + x1 + w, y + y1 + h)
            print(f"检测到可领取按钮: {box}")
            if self.is_claimable_single_frame(image=image, roi=box):
                click_button = ClickButton(area=box) 
                boxes.append(click_button)
                #cv2.rectangle(image, (x + x1, box_upper), (x + x1 +box_width, box_lower), (0, 255, 0), 2)
                cv2.rectangle(image, (x + x1, y + y1), ( x + x1 + w, y + y1 + h), (0, 255, 0), 2)
            else:
                #cv2.rectangle(image, (x + x1, box_upper), (x + x1 +box_width, box_lower), (255, 0, 0), 2)
                cv2.rectangle(image, (x + x1, y + y1), ( x + x1 + w, y + y1 + h), (255, 0, 0), 2)
            
            
        # 按 x 坐标排序
        boxes.sort(key=lambda b: b.button[0])
        image=cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if not self.config.Error_SaveError:  
            return boxes,image
        self.device.screenshot_deque.append({  
        'time': datetime.now(),  
        'image': image
        }) 
        self.screenshot_tracking_add()
        return boxes,image
