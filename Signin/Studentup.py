from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.popup import Popup
from pymongo import MongoClient
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

Builder.load_file('Signin/studentup.kv')

class SignupWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        client=MongoClient()
        db=client.stud
        self.users=db.users
    def validate_user(self):
        user = self.ids.username_field
        pwd = self.ids.pwd_field
        year= self.ids.year_field
        info = self.ids.info

        user = user.text
        passw = pwd.text
        year=year.text

        if user == '' or passw == '' or year=='':
            info.text = '[color=#FF0000]username and/ or password required'
        else:
            
            com=self.users.find_one({'UserName':user})
            print(com)
            if com==None:
                self.users.insert_one({'UserName':user,'Password':passw,'Year':year})
                info.text = '[color=#FF0000]Registred Successfully'
            else:
                info.text = '[color=#00FF00]user already present'
        
        self.parent.parent.current = 'scrn_si'
    def back(self):
        self.parent.parent.current='scrn_si' 



class StudentUpApp(App):
    # signin class inherit from App class
    def build(self):
        # build is inbuilt function n App class use for Layout
        return SignupWindow()


if __name__ == "__main__":
    # here we are creating a object sa of SigninApp class
    sa = StudentUpApp()
    sa.run()
    # run is inbuilt function in App class
