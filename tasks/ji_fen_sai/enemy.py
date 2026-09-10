from module.base.button import ButtonWrapper, ClickButton
from module.ocr.ocr import Digit, Ocr
from tasks.ji_fen_sai.assets.assets_ji_fen_sai import JI_FEN_SAI_FIGHT_START_BUTTON


class Enemy:
    power: int = 0
    organization: str = ''
    score: int = 0
    button:tuple[int,int,int,int]
    def __init__(self,area):
        if isinstance(area, ButtonWrapper):
            self.area = area.area
        elif isinstance(area, tuple):
            self.area = area
        self.button=None
    def __str__(self):
        return f" 组织: {self.organization},积分:{self.score},小队战力: {self.power}"    
    def  recognition(self,image,power,organization,score):
        #button
        JI_FEN_SAI_FIGHT_START_BUTTON.load_search(self.area)
        if JI_FEN_SAI_FIGHT_START_BUTTON.match_template(image):
            self.button=JI_FEN_SAI_FIGHT_START_BUTTON.button
        #power
        ocr=Digit(power)
        self.power=ocr.ocr_single_line(image)
        #organization
        ocr=Ocr(organization)
        self.organization=ocr.ocr_single_line(image)
        #score
        ocr=Digit(score)
        self.score=ocr.ocr_single_line(image)
        



