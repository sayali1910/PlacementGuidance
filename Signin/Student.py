from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.popup import Popup
from pymongo import MongoClient
from kivy.uix.boxlayout import BoxLayout
Builder.load_file('Signin/student.kv')

class SigninWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        client=MongoClient()
        db=client.stud
        self.users=db.users
    def validate_user(self):
        user = self.ids.username_field
        pwd = self.ids.pwd_field
        info = self.ids.info
        year=self.ids.year_field
        user = user.text
        passw = pwd.text
        year=year.text

        if user == '' or passw == '':
            info.text = '[color=#FF0000]username and/ or password required'
        else:
            
            com=self.users.find_one({'UserName':user,'Password':passw,'Year':year})
            print(com)
            if com==None:
                info.text = '[color=#FF0000]Invalid username and/ or password'
                
            else:
                info.text = '[color=#00FF00]username and/ or password is correct'
                if user=='admin' and passw=='admin' and year=='No':
                    self.parent.parent.current='scrn_admin'
                elif year=='BE':
                    self.parent.parent.current='scrn_bestart'
                else:
                    self.parent.parent.current='scrn_studstart'

    def signup(self):
        
        self.parent.parent.current='scrn_siup'



class StudentApp(App):
    # signin class inherit from App class
    def build(self):
        # build is inbuilt function n App class use for Layout
        return SigninWindow()


if __name__ == "__main__":
    # here we are creating a object sa of SigninApp class
    sa = StudentApp()
    sa.run()
    # run is inbuilt function in App class
