# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 18:50:13 2019

@author: Sayali
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from admin.admin import AdminWindow
from Signin.Student import SigninWindow
from Signin.Studentup import SignupWindow
from bestart.bestart import BeStartWindow
from studstart.studstart import StudStartWindow
#from admin.utils.datatabel import DataTabel
class MainWindow(BoxLayout):
    admin_widget=AdminWindow()
    signin_widget=SigninWindow()
    signup_widget=SignupWindow()
    bestart_widget=BeStartWindow()
    studstart_widget=StudStartWindow()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.scrn_si.add_widget(self.signin_widget)
        
        self.ids.scrn_siup.add_widget(self.signup_widget)
        
        self.ids.scrn_admin.add_widget(self.admin_widget)
        
        self.ids.scrn_bestart.add_widget(self.bestart_widget)
        
        self.ids.scrn_studstart.add_widget(self.studstart_widget)
        
class MainApp(App):
    def build(self):
        return MainWindow()


if __name__ == '__main__':
    P = MainApp()
    P.run()
