# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 05:52:54 2019

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

Builder.load_file('Signin/my.kv')
class SignUp(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)
    phone = ObjectProperty(None)
    uname = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        client=MongoClient()
        db=client.stud
        self.users=db.users

    def sign(self):
        user = self.ids.username_field
        pwd = self.ids.pwd_field
        
        info = self.ids.info

        user = user.text
        passw = pwd.text
        

        if user == '' or passw == '':
            info.text = '[color=#FF0000]username and/ or password required'
        else:
            
            com=self.users.find_one({'UserName':user})
            print(com)
            if com==None:
                self.users.insert_one({'UserName':user,'Password':passw})
                info.text = '[color=#FF0000]Registred Successfully'
            else:
                info.text = '[color=#00FF00]user already present'
        
        self.parent.parent.current = 'scrn_si'

class MyApp(App):
    def build(self):
        manager = ScreenManager()

        
        manager.add_widget(SignUp(name='signup'))
        return manager


if __name__=="__main__":
    MyApp().run()