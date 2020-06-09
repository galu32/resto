from Libs import *
from TableScreen import TablePage
from ItemScreen import ItemPage
from ConfigScreen import ConfigPage

Window.size = 1024,768

class MainApp(MDApp):
    
    def build(self):
        
        from SM import SM
        self.SM = SM()
        self.SM.TableScreen = TablePage()
        self.SM.ItemScreen = ItemPage()
        self.SM.ConfigScreen = ConfigPage()
        self.SM.add_widget(self.SM.TableScreen)
        self.SM.add_widget(self.SM.ItemScreen)
        self.SM.add_widget(self.SM.ConfigScreen)

        return self.SM

MainApp().run()
