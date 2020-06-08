from Libs import *
from TableScreen import *

Window.size = 1024,768

class MainApp(MDApp):
    
    def build(self):
        
        from SM import SM
        self.SM = SM()
        self.TableScreen = TablePage()
        self.SM.add_widget(self.TableScreen)

        return self.SM

MainApp().run()
