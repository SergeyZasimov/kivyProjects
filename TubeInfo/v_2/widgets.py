
import root
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.accordion import Accordion, AccordionItem

from config import UNITS, DISTRICTS

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
            board.add_widget(ToggleButton(text=el, size_hint_x=0.2, group='type', font_size='20sp', on_press=root.Root.select_unit))

            lbl = Label(text_size=(500, None), font_size='20sp')
            lbl.id = el
            board.add_widget(lbl)
            self.labels.append(lbl)

            scr = Label(text='0', color=(1, 0, 0, 1), size_hint_x=0.2, font_size='25sp')
            scr.id = el
            board.add_widget(scr)
            self.scores.append(scr)

        item.add_widget(board)
        return item


class PlacesBoard(Accordion):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = 0.4
        
        for district in DISTRICTS:
            parking_places_item = self.createParkingPlacesItem(district, DISTRICTS[district])
            self.add_widget(parking_places_item)

    def createParkingPlacesItem(self, name, list_):
        item = AccordionItem(title=name)
        board = GridLayout(cols=5, rows=4)

        for place in list_:
            board.add_widget(Button(text=str(place), font_size='18sp',  on_press=root.Root.press_place))

        item.add_widget(board)
        return item


class Selector(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
#        self.orientation = 'vertical'
        self.size_hint_y = 0.1

        add = Selector.add = ToggleButton(text='Добавить', group='add_del', state='down', on_press=root.Root.select_status)
        del_ = Selector.del_ = ToggleButton(text='Удалить', group='add_del', on_press=root.Root.select_status)
        fetch = Button(text='Данные', on_press=root.Root.fetch)
        clear = Button(text='Очистить', on_press=root.Root.clear)

        self.add_widget(add)
        self.add_widget(del_)
        self.add_widget(fetch)
        self.add_widget(clear)
