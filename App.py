from Libs import *
from TableScreen import *
from ItemScreen import *

Window.size = 1024,768

class MainApp(MDApp):
    
    def build(self):
        
        from SM import SM
        self.SM = SM()
        self.TableScreen = TablePage()
        self.SM.ItemScreen = ItemPage()
        self.SM.add_widget(self.TableScreen)
        self.SM.add_widget(self.SM.ItemScreen)

        return self.SM

MainApp().run()
