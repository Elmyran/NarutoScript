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
    def __str__(self):
        return f" 组织: {self.organization},积分:{self.score},小队战力: {self.power}"    
    def  recognition(self,image):
        #button
        JI_FEN_SAI_FIGHT_START_BUTTON.load_search(self.area)
        if JI_FEN_SAI_FIGHT_START_BUTTON.match_template(image):
            self.button=JI_FEN_SAI_FIGHT_START_BUTTON.button
        #power
        power_area=(840,
                    self.area[1]+67,
                    940,
                    self.area[3]
                    )
        button=ClickButton(area=power_area,name='POWER')
        ocr=Digit(button)
        self.power=ocr.ocr_single_line(image)
        #organization
        organization_area=(555,
                           self.area[1]+34,
                           700,
                           self.area[3]-40

        )
        button=ClickButton(area=organization_area,name='ORGANIZATION')
        ocr=Ocr(button)
        self.organization=ocr.ocr_single_line(image)
        #score
        score_area=(630,
                    self.area[1]+66,
                    690,
                    self.area[3]
                    )
        button=ClickButton(area=score_area,name='SCORE')
        ocr=Digit(button)
        self.score=ocr.ocr_single_line(image)
        



