import math

from module.base.timer import Timer
from module.logger import logger
from module.ocr.ocr import Digit
from module.ocr.yolomodel import YOLO_MODEL
from tasks.activity.assets.assets_activity_qiu_ri_ji import *
from tasks.activity.draglist import ACTIVITY_TAB_LIST
from tasks.activity.keyword import QiuRiJiKeyword
from tasks.activity.qiu_ri_ji.ocr import OcrQuizTitle, OcrQuizOption
from tasks.activity.qiu_ri_ji.question import match_quiz_title, QUIZ_STRATEGIES
from tasks.activity.qiu_ri_ji.title import QuizTitle
from tasks.base.assets.assets_base_page import FULL_SCREEN
from tasks.base.page import page_activity, page_qiu_ri_ji
from tasks.ren_zhe_tiao_zhan.joystick import GameControl
CLASS_NAMES={
    0:'center',
    1:'arrow'
}
class QiuRiJi(GameControl):
    def run(self):
        self.handle_qiu_ri_ji()
        self.config.task_delay(server_update=True)
        self.config.task_stop()
    def handle_qiu_ri_ji(self):
        self.ui_ensure(page_activity)
        ACTIVITY_TAB_LIST.search_rows(main=self,keyword=QiuRiJiKeyword)
        self._activity_goto_qiu_ri_ji()
        ocr=Digit(ACTION_NUMBER)
        for _ in self.loop():
            if self.appear(ACTION_SHORTAGE):
                break
            if self.appear_then_click(QUICK_EXPLORE,interval=1):
                if self._check():
                    self._handle()
                else:
                    continue
            if self.appear(EXPLORING):
                self._explore()
            action=ocr.ocr_single_line(self.device.image)
            if action!=0:
                self.appear_then_click(EXPLORE_BUTTON,interval=1)
            else:
                break
        self.ui_goto_main()


    def _activity_goto_qiu_ri_ji(self):

        for _ in self.loop():
            if self.ui_page_appear(page_qiu_ri_ji):
                break
            if self.appear_then_click(ACTIVITY_GOTO_PAGE,interval=1):
                continue


    def _explore(self):

        self._search()
        if not self._check():
            return
        self._handle()


    def _search(self):
        self.device.screenshot()
        model=YOLO_MODEL.get_model('tasks/activity/qiu_ri_ji/best.onnx',classes=CLASS_NAMES)
        for _ in self.loop():
            if FIND_BUTTON.match_template(self.device.image,direct_match=True):
                print('find button pressed')
                break
            else:
                res=model.predict(self.device.image,conf=0.4)
                print(res)
                angle=self.get_arrow_angle(res)
                if angle is None:
                    continue
                self.move_to_direction(angle,0.2)

    def get_arrow_angle(self,res):
        """
        res: List[YoloResult]
        返回 arrow 相对于 center 的角度（0-360度）
        正上方为0度，顺时针为正
        """
        center_xy = None
        arrow_xy = None

        for r in res:
            x, y, w, h = r.box
            x_center = x + w / 2
            y_center = y + h / 2

            if r.class_id == 0:   # center
                center_xy = (x_center, y_center)
            elif r.class_id == 1: # arrow
                arrow_xy = (x_center, y_center)

        if center_xy is None or arrow_xy is None:
            return None  # 找不到必要目标

        dx = arrow_xy[0] - center_xy[0]
        dy = center_xy[1] - arrow_xy[1]  # Y轴向下，正上方为0，所以反向

        angle = math.degrees(math.atan2(dx, dy))
        angle = (angle + 360) % 360
        return angle

    def _check(self):
        time=Timer(3,5).start()
        for _ in self.loop():
            if time.reached():
                return  False
            if self.appear(QIU_RI_JI_EVENT):
                return True
            if self.appear(QIU_RI_JI_GET_REWARD):
                return True
            FIND_BUTTON.load_search(FULL_SCREEN.area)
            if self.appear_then_click(FIND_BUTTON):
                continue

    def _handle(self):
        self.device.screenshot()
        ocr = OcrQuizOption(ANSWER_AREA)
        for _ in self.loop():
            if QIU_RI_JI_EXPLORE_BUTTON.match_template_color(self.device.image):
                break
            if self.appear_then_click(QIU_RI_JI_GET_REWARD,interval=1):
                continue
            option=self._select_option()
            if option:
                button=ocr.matched_ocr(self.device.image,option)
                if button:
                    self.device.click(button[0])

    def _select_option(self):
        self.device.screenshot()
        title_ocr = OcrQuizTitle(QUESTION_AREA)
        results = title_ocr.detect_and_ocr(self.device.image)
        question_text = ''.join([r.ocr_text for r in results])
        print(question_text)
        all_quiz_titles = list(QuizTitle.instances.values())
        matched_title = match_quiz_title(question_text, all_quiz_titles)
        if matched_title in QUIZ_STRATEGIES:
            priority_options = QUIZ_STRATEGIES[matched_title]
            logger.info(f'匹配到题目: {matched_title}, 选择答案: {priority_options}')
            return priority_options
        logger.warning('No matching option found')
        return None



