# coding: utf-8
import shelve
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.accordion import Accordion, AccordionItem

# screen:s3,portrait,scale=.75

AIRCRAFTS1 = ['SSJ', '737', '320', '330', '777', '747']
AIRCRAFTS2 = ['757', '204', '76', '7', '9', '11']
INFO = {key: [] for key in (AIRCRAFTS1 + AIRCRAFTS2)}
PARKING_PLACES = [86, 90, 93, 94, 95, 96, 97, 100, 102, 107, 109, 111] + list(range(113, 132))
CURRENT_CONFIG = {
    'current_aircraft': None,
    'current_status': 'add'
}

DB_FILE = 'tube_db'

def make_db(path=DB_FILE):
    with shelve.open(path, flag='n') as db:
        for key in INFO:
            db[key] = INFO[key]

class TubeApp(App):

    def set_status(self, *args):
        if self.add.state == 'down':
            CURRENT_CONFIG['current_status'] = 'add'
        if self.delete.state == 'down':
            CURRENT_CONFIG['current_status'] = 'del'

    def set_type(self, obj):
        if obj.state == 'down':
            CURRENT_CONFIG['current_aircraft'] = obj.text

    def press_parking_place(self, obj):
        try:
            if CURRENT_CONFIG['current_status'] == 'add':
                INFO[CURRENT_CONFIG['current_aircraft']].append((obj.text))
            else:
                INFO[CURRENT_CONFIG['current_aircraft']].remove(obj.text)
        except: pass

        print(INFO[CURRENT_CONFIG['current_aircraft']])

        for label in [child for child in self.labels if child.id == CURRENT_CONFIG['current_aircraft']]:
            label.text = ', '.join(sorted(INFO[CURRENT_CONFIG['current_aircraft']]))

        make_db()

    def fetch_db(self):
        with shelve.open(DB_FILE) as db:
            for key in db:
                INFO[key] = db[key]

                for label in [child for child in self.labels if child.id == key]:
                    label.text = ', '.join(sorted(INFO[key]))
                    

    def build(self):
        # корень
        root = BoxLayout(orientation='vertical')

        # селектор добавить-удалить
        self.selector = BoxLayout(size_hint=(1, 0.1))
        self.add = ToggleButton(text='Добавить', group='add_del', state='down', on_press=self.set_status)
        self.delete = ToggleButton(text='Удалить', group = 'add_del', on_press = self.set_status)

        self.fetch = Button(text='Данные')
        self.fetch.on_press = self.fetch_db

        self.selector.add_widget(self.add)
        self.selector.add_widget(self.delete)
        self.selector.add_widget(self.fetch)

        # инфо панель
        self.accordion = Accordion(orientation='horizontal')
        self.item1 = AccordionItem(title='737 320 SSJ 330 777 747')
        self.item2 = AccordionItem(title='757 204 76 7 9 11')
        self.accordion.add_widget(self.item2)
        self.accordion.add_widget(self.item1)

        self.labels = []

        self.info_board1 = GridLayout(cols=2)
        for aircraft in AIRCRAFTS1:
            self.tgl = ToggleButton(text=aircraft)
            self.tgl.size_hint = (0.2, 1)
            self.tgl.group = 'type'
            self.tgl.on_press = lambda obj=self.tgl: self.set_type(obj)

            self.lbl = Label(halign='left', text_size=(300, None), shorten=False, shorten_from='left')
            self.lbl.id = aircraft
            self.labels.append(self.lbl)

            self.info_board1.add_widget(self.tgl)
            self.info_board1.add_widget(self.lbl)

        self.item1.add_widget(self.info_board1)

        self.info_board2 = GridLayout(cols=2)
        for aircraft in AIRCRAFTS2:
            self.tgl = ToggleButton(text=aircraft)
            self.tgl.size_hint = (0.2, 1)
            self.tgl.group = 'type'
            self.tgl.on_press = lambda obj=self.tgl: self.set_type(obj)

            self.lbl = Label(halign='left', text_size=(400, None), shorten=False, shorten_from='left')
            self.lbl.id = aircraft
            self.labels.append(self.lbl)

            self.info_board2.add_widget(self.tgl)
            self.info_board2.add_widget(self.lbl)

        self.item2.add_widget(self.info_board2)

        # стоянки
        self.parking_places = GridLayout(cols=4, rows=8)
        for place in PARKING_PLACES:
            self.btn = Button(text=str(place))
            self.btn.on_press = lambda obj=self.btn: self.press_parking_place(obj)
            self.parking_places.add_widget(self.btn)

        root.add_widget(self.accordion)
        root.add_widget(self.parking_places)
        root.add_widget(self.selector)

        return root

       
if __name__ == '__main__':
    app = TubeApp()
    app.run()

