import os
import shelve
from widgets import *
from config import DB

class Root(BoxLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.status = Root.status = 'Добавить'
        self.status = Root.current_unit = None
        self.info = Root.info = self.createInfoDict()
        self.createDB()

        self.info_board = InfoBoard()
        self.places_board = PlacesBoard()
        self.selector = Selector()
        
        self.lower = BoxLayout(size_hint_y=0.5)
        self.lower.add_widget(self.selector)
        self.lower.add_widget(self.places_board)

        self.add_widget(self.info_board)
        self.add_widget(self.lower)

    #методы класса Root

    def createInfoDict(self):
        keys = []
        
        for category in UNITS:
            for el in UNITS[category]:
                keys.append(el)

        info_dict = {key: [] for key in keys}

        return info_dict


    def showInfo(key):
        for label in InfoBoard.labels:
            if label.id == key:
                label.text = ', '.join(sorted(Root.info[key], key=int))

        for score in InfoBoard.scores:
            if score.id == key:
                score.text = str(len(Root.info[key]))
                score.color = (1, 1, 1, 1)
                if score.text == '0':
                    score.color = (1, 0, 0, 1)

    def createDB(self):
        if not os.path.exists('db'):
            os.mkdir('db')

            with shelve.open(DB, flag='n') as db:
                for key in Root.info:
                    db[key] = Root.info[key]

    def updateDB(key):
        with shelve.open(DB, flag='w') as db:
            db[key] = Root.info[key]



    # методы-обработчики событий

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

            Root.showInfo(Root.current_unit)
            Root.updateDB(Root.current_unit)
        except Exception as ex:
            # print(ex)
            pass
    

    def select_unit(self):
        if self.state == 'down':
            Root.current_unit = self.text
        else:
            Root.current_unit = None

    def fetch(self):
        with shelve.open(DB) as db:
            for key in db:
                Root.info[key] = db[key]

                Root.showInfo(key)

    def clear(self):
        Root.info[Root.current_unit] = []
        Root.updateDB(Root.current_unit)
        Root.showInfo(Root.current_unit)
