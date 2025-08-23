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
from tasks.ren_zhe_tiao_zhan.assets.assets_ren_zhe_tiao_zhan import MI_JING_SUCCESS
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import torch
from ultralytics import YOLO
MODEL_PATH_CONFIG = r"tasks/ren_zhe_tiao_zhan/best.pt"
class AutoBattle(GameControl):
    def __init__(self, config, device: Device=None, task=None):
        super().__init__(config, device, task)
        self.PATHFINDING_PATTERN = [("RIGHT", 5.0), ("STOP", 0.5), ("LEFT", 5.0), ("STOP", 0.5)]
        self.DIRECTION_ANGLES = {"RIGHT": 90, "UP": 0, "LEFT": -90, "DOWN": 180, "STOP": 0}
        self.ATTACK_SWEET_SPOT_Y = (-40, 40)
        self.ATTACK_SWEET_SPOT_X = (-300, 300)
        self.FACING_BLIND_SPOT_X = (-40, 40)
        self.device_torch = "cuda" if torch.cuda.is_available() else "cpu"
        if self.device_torch == "cuda":
            torch.zeros(1).cuda()
        self.model = YOLO(MODEL_PATH_CONFIG)
        self.model.to(self.device_torch)
        logger.info("--- YOLO model loaded. ---")
        self.client = None
        self.path_finding_period=5
        try:
            logger.info(f"--- Initializing scrcpy client for device {self.device.serial} ---")
            self.client = pyscrcpy.Client(device=adbutils.device(serial=self.device.serial),max_fps=60)
            self.joystick = JoystickContact(self)
            logger.info("--- Scrcpy client and Joystick initialized. ---")
        except Exception as e:
            logger.error(f"---Failed to initialize services: {e}")
            raise ConnectionError(f"Scrcpy client initialization failed: {e}")

    def _distance(self, p1, p2):
        return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

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
        INFERENCE_SIZE = (640,640)
        current_state = 'SEARCHING'
        pathfinding_step = 0
        pathfinding_timer = Timer(0)
        path_period = Timer(self.path_finding_period)
        while True:
            if self.appear(MI_JING_SUCCESS):
                logger.info("--- Battle finished (MI_JING_SUCCESS detected). ---")
                self.joystick.up()
                break
            if not self.client or not self.client.alive:
                logger.error("Scrcpy client is not running. Aborting fight.")
                break
            self.device.click_record_clear()
            self.device.stuck_record_clear()
            img_raw = self.client.last_frame
            if img_raw is None:
                time.sleep(0.01)
                continue
            bgr_frame = cv2.cvtColor(img_raw, cv2.COLOR_RGB2BGR)
            self.image = bgr_frame
            self.device.image = bgr_frame
            resized_img = cv2.resize(img_raw, INFERENCE_SIZE)
            results = self.model(resized_img, conf=0.7, verbose=False, device=self.device_torch)
            self_boxes, enemy_boxes = [], []
            original_shape = self.image.shape
            scale_x = original_shape[1] / INFERENCE_SIZE[0]
            scale_y = original_shape[0] / INFERENCE_SIZE[1]
            for r in results:
                for box in r.boxes:
                    b = box.xyxy[0].cpu().numpy()
                    c = ((b[0] * scale_x + b[2] * scale_x) / 2, (b[1] * scale_y + b[3] * scale_y) / 2)
                    if int(box.cls[0]) == 0: self_boxes.append({'center': c})
                    else: enemy_boxes.append({'center': c})
            if self_boxes and enemy_boxes:
                if current_state != 'COMBAT':
                    logger.info(f"State: {current_state} -> COMBAT. Target acquired.")
                    current_state = 'COMBAT'
                s_char = min(self_boxes, key=lambda s: self._distance(s['center'], (original_shape[1] / 2, original_shape[0] / 2)))
                self_center = s_char['center']
                target_enemy = min(enemy_boxes, key=lambda e: self._distance(self_center, e['center']))
                enemy_center = target_enemy['center']
                dist = self._distance(self_center, enemy_center)
                dx, dy = enemy_center[0] - self_center[0], enemy_center[1] - self_center[1]
                if dist > attack_range:
                    angle = np.degrees(np.arctan2(dx, -dy))
                    self.joystick.set(angle)
                else:
                    is_in_sweet_spot_y = self.ATTACK_SWEET_SPOT_Y[0] < dy < self.ATTACK_SWEET_SPOT_Y[1]
                    if not is_in_sweet_spot_y:
                        angle = 180 if dy > 0 else 0
                        self.joystick.set(angle)
                    else:
                        self.joystick.up()
                        if self.execute_skill2(): pass
                        elif self.execute_skill1(): pass
                        else: self.execute_attack()
            else:
                if path_period.reached():
                    path_period.reset()
                else:
                    continue
                if current_state != 'PATHFINDING':
                    logger.info("State: -> PATHFINDING. Target lost, starting search pattern.")
                    current_state = 'PATHFINDING'
                    pathfinding_step = 0
                    _, duration = self.PATHFINDING_PATTERN[pathfinding_step]
                    pathfinding_timer = Timer(duration)
                    pathfinding_timer.reset()
                if pathfinding_timer.reached():
                    pathfinding_step = (pathfinding_step + 1) % len(self.PATHFINDING_PATTERN)
                    _, duration = self.PATHFINDING_PATTERN[pathfinding_step]
                    pathfinding_timer = Timer(duration)
                    pathfinding_timer.reset()
                    logger.info(f"Pathfinding: switching to step {pathfinding_step + 1}.")
                direction, _ = self.PATHFINDING_PATTERN[pathfinding_step]
                if direction == "STOP":
                    self.joystick.up()
                else:
                    angle = self.DIRECTION_ANGLES.get(direction, 0)
                    self.joystick.set(angle)