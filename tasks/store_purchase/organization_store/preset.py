from module.base.filter import MultiLangFilter  
import re
from module.ocr.ocr import OcrResultButton
from tasks.store_purchase.organization_store.keywords import MeritExchangeItem
from tasks.store_purchase.selector import StoreSelector  
def get_regex_from_keyword_name(keyword, attr_name):
    string = ""
    for instance in keyword.instances.values():
        if hasattr(instance, attr_name):
            for name in instance.__getattribute__(attr_name):
                string += f"{name}|"
    # some pattern contain each other, make sure each pattern end with "-" or the end of string
    return f"(?:({string[:-1]})(?:-|$))?"  

MERIT_EXCHANGE_FILTER_ATTR=tuple()
MERIT_EXCHANGE_ATTR='merit_exchange'
MERIT_EXCHANGE_FILTER_PRESET = ('reset')  
pattern = ''
merit_exchange_regex = get_regex_from_keyword_name(MeritExchangeItem, MERIT_EXCHANGE_ATTR)
pattern+= merit_exchange_regex

MERIT_EXCHANGE_REGEX = re.compile(pattern)  
MERIT_EXCHANGE_FILTER_ATTR+= (MERIT_EXCHANGE_FILTER_ATTR,)  
MERIT_EXCHANGE_FILTER = MultiLangFilter(  
    MERIT_EXCHANGE_REGEX,   
    MERIT_EXCHANGE_FILTER_ATTR,   
    MERIT_EXCHANGE_FILTER_PRESET  
)

MeritExchangePreset="""
组织饰品礼盒 > 铜币 > 轮回石 > 忍玉
""" 
class MeritExchangeSelector(StoreSelector):
    def recognition(self):
       pass
    def ui_select(self, target: OcrResultButton | None, skip_first_screenshot=True):
        def is_curio_selected():
            pass
            

        def is_select_complete():
            pass
         

    def try_select(self, option: OcrResultButton | str):
        pass

    def load_filter(self):
        filter_ = MERIT_EXCHANGE_FILTER
        string = ""
        match self.config.OrganizationStore_MeritExchangeFilter:
            case 'preset':
                string=MeritExchangePreset
            case 'custom':
                string = self.config.OrganizationStore_CustomMeritExchangeFilter
        filter_.load(string)
        self.filter_=filter_
