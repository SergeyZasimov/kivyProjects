#pylint:disable=E0611
#pylint:disable=E0401
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

class Container(BoxLayout):
    status = ObjectProperty()
    def on_press(self):
        if self.status.add_status.state == 'down':
            print(self.status.add_status.text)
        elif self.status.delete_status.state == 'down':
            print(self.status.delete_status.text)            
    
class Selector():
    add_status = ObjectProperty()
    delete_status = ObjectProperty()
    
    
class MyApp(App):
    def build(self):
        return Container()
        
if __name__ ==  '__main__':
      app = MyApp()
      app.run()
