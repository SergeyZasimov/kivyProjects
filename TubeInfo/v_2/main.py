
import os
import shelve
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.accordion import Accordion, AccordionItem

#screen:s3,portrait,scale=.75

DB = os.path.join('db', 'tube_db')

UNITS = {
            'Стремянки': ('5', '6', '7', '9', '11', '15'),
            'Водила': ('SSJ', '737', '320', '330', '777', '747', '757', '204', '76'),
        }

DISTRICTS = {
               # 'Запад': tuple(range(162, 221)),
               # 'C': tuple(range(132, 151)),
                'B': tuple(range(113, 132)),
                'Восток': tuple(range(86, 113)),
            }


class InfoBoard(Accordion):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.labels = InfoBoard.labels = []
        self.scores = InfoBoard.scores = []
        
        for unit in UNITS: 
            info_board_item = self.createInfoBoardItem(unit, UNITS[unit])
            self.add_widget(info_board_item)
    
    def createInfoBoardItem(self, name, list_):
        item = AccordionItem(title=name)
        board = GridLayout(cols=3)
        
        for el in list_:
            board.add_widget(ToggleButton(text=el, size_hint_x=0.2, group='type', on_press=Root.select_unit))

            lbl = Label(text_size=(550, None))
            lbl.id = el
            board.add_widget(lbl)
            self.labels.append(lbl)

            scr = Label(text='0', color=(1, 0, 0, 1), size_hint_x=0.2)
            scr.id = el
            board.add_widget(scr)
            self.scores.append(scr)

        item.add_widget(board)
        return item


class PlacesBoard(Accordion):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        
        for district in DISTRICTS:
            parking_places_item = self.createParkingPlacesItem(district, DISTRICTS[district])
            self.add_widget(parking_places_item)

    def createParkingPlacesItem(self, name, list_):
        item = AccordionItem(title=name)
        board = GridLayout(cols=8, rows=8)

        for place in list_:
            board.add_widget(Button(text=str(place), on_press=Root.press_place))

        item.add_widget(board)
        return item


class Selector(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_x = 0.2

        self.add = Selector.add = ToggleButton(text='Добавить', group='add_del', state='down', on_press=Root.select_status)
        self.del_ = Selector.del_ = ToggleButton(text='Удалить', group='add_del', on_press=Root.select_status)
        self.fetch = Button(text='Данные', on_press=Root.fetchDB)
        self.clear = Button(text='Очистить', on_press=Root.clear)

        self.add_widget(self.add)
        self.add_widget(self.del_)
        self.add_widget(self.fetch)
        self.add_widget(self.clear)


class Root(BoxLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        Root.status = 'Добавить'
        Root.current_unit = None
        Root.info = self.createInfoDict()
        self.createDB()

        self.info_board = InfoBoard()
        self.places_board = PlacesBoard()
        self.selector = Selector()
        
        self.lower = BoxLayout()
        self.lower.add_widget(self.selector)
        self.lower.add_widget(self.places_board)

        self.add_widget(self.info_board)
        self.add_widget(self.lower)

    def createInfoDict(self):
        keys = []
        
        for category in UNITS: 
            for el in UNITS[category]:
                keys.append(el)

        info_dict = {key: [] for key in keys}

        return info_dict

    def select_status(self):
        if self.state == 'down':
            Root.status = self.text
        else:
            Root.status = ''

    def press_place(self):
        try:
            if Root.status == 'Добавить':
                Root.info[Root.current_unit].append(self.text)
            elif Root.status == 'Удалить':
                Root.info[Root.current_unit].remove(self.text)
                Selector.del_.state = 'normal'
                Selector.add.state = 'down'
                Root.status = 'Добавить'

            for label in InfoBoard.labels:
                if label.id == Root.current_unit:
                    label.text = ', '.join(sorted(Root.info[Root.current_unit], key=int))

            for score in InfoBoard.scores:
                if score.id == Root.current_unit:
                    score.text = str(len(Root.info[Root.current_unit]))
                    score.color = (1, 1, 1, 1)
                    if score.text == '0':
                        score.color = (1, 0, 0, 1)

            Root.updateDB(Root.current_unit)
        except Exception as ex: print(ex)

    def select_unit(self):
        if self.state == 'down':
            Root.current_unit = self.text
        else:
            Root.current_unit = None

    def createDB(self):
        if not os.path.exists('db'):
            os.mkdir('db')

            with shelve.open(DB, flag='n') as db:
                for key in Root.info:
                    db[key] = Root.info[key]

    def updateDB(key):
        with shelve.open(DB, flag='w') as db:
            db[key] = Root.info[key]

    def fetchDB(self):
        with shelve.open(DB) as db:
            for key in db:
                Root.info[key] = db[key]

                for label in InfoBoard.labels:
                    if label.id == key:
                        label.text = ', '.join(sorted(Root.info[key], key=int))

                for score in InfoBoard.scores:
                    if score.id == key:
                        score.text = str(len(Root.info[key]))
                        score.color = (1, 1, 1, 1)
                        if score.text == '0':
                            score.color = (1, 0, 0, 1)
                        

    def clear():
        pass


class MainApp(App):
    def build(self):
        return Root()


if __name__ == '__main__':
    MainApp().run()

