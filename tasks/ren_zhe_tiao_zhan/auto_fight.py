import numpy as np
import cv2
import time
import os
import pyscrcpy
import adbutils
from module.device.device import Device
from module.logger import logger
from module.base.timer import Timer
from tasks.ren_zhe_tiao_zhan.joystick import GameControl, JoystickContact
from tasks.ren_zhe_tiao_zhan.assets.assets_ren_zhe_tiao_zhan import MI_JING_SUCCESS, MI_JING_REWARD_EXIT, \
    MI_JING_REWARD_AREA

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import torch
from ultralytics import YOLO
MODEL_PATH_CONFIG = r"tasks/ren_zhe_tiao_zhan/best.pt"
class AutoBattle(GameControl):
    def __init__(self, config, device: Device = None, task=None):
        super().__init__(config, device, task)
        self.PATHFINDING_PATTERN = [("RIGHT", 5.0), ("STOP", 0.5), ("LEFT", 5.0), ("STOP", 0.5)]
        self.DIRECTION_ANGLES = {"RIGHT": 90, "UP": 0, "LEFT": -90, "DOWN": 180, "STOP": 0}
        self.ATTACK_SWEET_SPOT_Y = (-40, 40)
        self.ATTACK_SWEET_SPOT_X = (-300, 300)
        self.FACING_BLIND_SPOT_X = (-40, 40)
        self.TARGET_LOST_BUFFER_DURATION = 2.0
        self.device_torch = "cuda" if torch.cuda.is_available() else "cpu"
        print(self.device_torch)
        if self.device_torch == "cuda":
            torch.zeros(1).cuda()
        self.model = YOLO(MODEL_PATH_CONFIG)
        self.model.to(self.device_torch)
        logger.info("--- YOLO model loaded. ---")
        self.client = None
        try:
            logger.info(f"--- Initializing scrcpy client for device {self.device.serial} ---")
            self.client = pyscrcpy.Client(device=adbutils.device(serial=self.device.serial), max_fps=60,
                                          bitrate=16000000, block_frame=False)
            self.joystick = JoystickContact(self)
            logger.info("--- Scrcpy client and Joystick initialized. ---")
        except Exception as e:
            logger.error(f"---Failed to initialize services: {e}")
            raise ConnectionError(f"Scrcpy client initialization failed: {e}")
    def _distance(self, p1, p2):
        return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    def start_services(self):
        if not self.client.alive:
            self.client.start(threaded=True)
            while self.client.last_frame is None:
                time.sleep(0.1)
        logger.info("--- Services started, ready for battle. ---")
    def stop_services(self):
        logger.info("--- Stopping services. ---")
        if hasattr(self, 'joystick') and self.joystick.is_downed:
            self.joystick.up()
        if self.client and self.client.alive:
            self.client.stop()
    def run(self):
        attack_range = 300
        current_state = 'SEARCHING'
        pathfinding_step = 0
        pathfinding_timer = Timer(0)
        target_lost_timer = Timer(self.TARGET_LOST_BUFFER_DURATION)
        miss_count = 0
        MISS_THRESHOLD = 5
        while True:
            self.device.click_record_clear()
            self.device.stuck_record_clear()
            img_raw = self.client.last_frame
            if img_raw is None:
                continue
            img = cv2.cvtColor(img_raw, cv2.COLOR_BGR2RGB)
            self.device.image = img
            MI_JING_SUCCESS.load_search(MI_JING_REWARD_AREA.area)
            MI_JING_REWARD_EXIT.load_search(MI_JING_REWARD_AREA.area)
            if self.appear(MI_JING_SUCCESS) or self.appear(MI_JING_REWARD_EXIT):
                logger.info("--- Battle finished (MI_JING_SUCCESS detected). ---")
                self.joystick.up()
                break
            if not self.client or not self.client.alive:
                logger.error("Scrcpy client is not running. Aborting fight.")
                break
            results = self.model(img_raw, conf=0.7, verbose=False, device=self.device_torch)
            self_boxes, enemy_boxes = [], []
            for r in results:
                for box in r.boxes:
                    b = box.xyxy[0].cpu().numpy()
                    c = ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)
                    if int(box.cls[0]) == 0:
                        self_boxes.append({'center': c})
                    else:
                        enemy_boxes.append({'center': c})
            if self_boxes and enemy_boxes:
                miss_count = 0
                if current_state != 'COMBAT':
                    logger.info(f"State: {current_state} -> COMBAT. Target acquired.")
                    current_state = 'COMBAT'
                h, w = self.device.image.shape[:2]
                screen_center = (w / 2, h / 2)
                s_char = min(self_boxes, key=lambda s: self._distance(s['center'], screen_center))
                self_center = s_char['center']
                target_enemy = min(enemy_boxes, key=lambda e: self._distance(self_center, e['center']))
                enemy_center = target_enemy['center']
                dist = self._distance(self_center, enemy_center)
                dx, dy = enemy_center[0] - self_center[0], enemy_center[1] - self_center[1]
                if dist > attack_range:
                    angle = np.degrees(np.arctan2(dx, -dy))
                    self.joystick.set(angle)
                else:
                    is_in_sweet_spot_x = self.ATTACK_SWEET_SPOT_X[0] < dx < self.ATTACK_SWEET_SPOT_X[1]
                    is_in_sweet_spot_y = self.ATTACK_SWEET_SPOT_Y[0] < dy < self.ATTACK_SWEET_SPOT_Y[1]
                    is_in_blind_spot = self.FACING_BLIND_SPOT_X[0] < dx < self.FACING_BLIND_SPOT_X[1]
                    if is_in_blind_spot and is_in_sweet_spot_y:
                        self.joystick.up()
                        if self.execute_skill2():
                            pass
                        elif self.execute_skill1():
                            pass
                        else:
                            self.execute_attack()
                    elif not is_in_sweet_spot_y:
                        angle = 180 if dy > 0 else 0
                        self.joystick.set(angle)
                    elif is_in_sweet_spot_x and not is_in_blind_spot:
                        if np.random.rand() < 0.7:
                            self.joystick.up()
                            if self.execute_skill2():
                                pass
                            elif self.execute_skill1():
                                pass
                            else:
                                self.execute_attack()
                        else:
                            angle = 90 if dx > 0 else -90
                            self.joystick.set(angle)
                    else:
                        angle = 90 if dx > 0 else -90
                        self.joystick.set(angle)
            else:
                miss_count += 1
                if current_state == 'COMBAT' and miss_count >= MISS_THRESHOLD:
                    logger.info("State: COMBAT -> HOLDING. Target lost, waiting before search.")
                    current_state = 'HOLDING'
                    target_lost_timer.reset()
                    self.joystick.up()
                elif current_state == 'HOLDING':
                    if target_lost_timer.reached():
                        logger.info("State: HOLDING -> PATHFINDING. Buffer ended, starting search pattern.")
                        current_state = 'PATHFINDING'
                        pathfinding_step = 0
                        _, duration = self.PATHFINDING_PATTERN[pathfinding_step]
                        pathfinding_timer = Timer(duration)
                        pathfinding_timer.reset()
                elif current_state == 'PATHFINDING':
                    if pathfinding_timer.reached():
                        pathfinding_step = (pathfinding_step + 1) % len(self.PATHFINDING_PATTERN)
                        direction, duration = self.PATHFINDING_PATTERN[pathfinding_step]
                        pathfinding_timer = Timer(duration)
                        pathfinding_timer.reset()
                        logger.info(f"Pathfinding: switching to step {pathfinding_step + 1} ({direction}).")
                    direction, _ = self.PATHFINDING_PATTERN[pathfinding_step]
                    if direction == "STOP":
                        self.joystick.up()
                    else:
                        angle = self.DIRECTION_ANGLES.get(direction, 0)
                        self.joystick.set(angle)
