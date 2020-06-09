from Libs import *
from SM import _session
from BaseScreen import *

Config_kv = """
<ConfigPage>:
    name : "ConfigPage"

    MDGridLayout:
        cols:1
        id : MainGrid
        
        MDToolbar:
            id : ItemToolbar
            pos_hint : {"top" : 1}
            left_action_items : [['arrow-left', lambda x : root.go_back()]]

"""

class ConfigPage(BasePage):

    Builder.load_string(Config_kv)
    
    def go_back(self):
        self.parent.current = "TablePage"