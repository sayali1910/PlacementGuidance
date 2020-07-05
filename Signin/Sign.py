# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 14:43:16 2019

@author: Sayali
"""


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
from kivy.lang import Builder
from kivy.lang import BoxLayout

Builder.load_file('Signin/my.kv')
class Login(Screen):
    username=ObjectProperty(None)
    password=ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        client=MongoClient()
        db=client.stud
        self.users=db.users
    def login(self):
        
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
            
            com=self.users.find_one({'UserName':user,'Password':passw})
            print(com)
            if com==None:
                info.text = '[color=#FF0000]Invalid username and/ or password'
                
            else:
                info.text = '[color=#00FF00]username and/ or password is correct'
                if user == 'admin' or passw == 'admin':
                    self.parent.parent.current='scrn_admin'
                else:
                    if year=='BE':
                        self.parent.parent.current='scrn_bestart'
                    else:
                        self.parent.parent.current='scrn_studstart'
                        
            
                


    def signup(self):
        
        self.parent.parent.current='scrn_siup'

'''def show_popup():
    show=P()
    popupwindow =Popup(title="Popup Window",content=show, size_hint=(None,None),size=(400,400))
    popupwindow.open()
'''


class MyApp(App):
    def build(self):
        manager = ScreenManager()

        manager.add_widget(Login(name='loginwindow'))
       
        return manager


if __name__=="__main__":
    MyApp().run()
