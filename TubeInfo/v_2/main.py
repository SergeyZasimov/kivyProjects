from kivy.app import App
from root import Root

#screen:s3,portrait,scale=.75


class MainApp(App):
    def build(self):
        return Root()


if __name__ == '__main__':
    MainApp().run()

