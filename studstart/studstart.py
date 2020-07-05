# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 16:25:47 2019

@author: Sayali
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from pymongo import MongoClient
from utils.datatabel import DataTabel
from collections import OrderedDict
from kivy.uix.textinput import TextInput
from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
from kivy.uix.label import Label
import pandas as pd
import matplotlib.pyplot as plt
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg as FCK
from kivy.clock import Clock
from kivy.lang import Builder

Builder.load_file('studstart/studstart.kv')
class Notify(ModalView):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.size_hint=(.7,.7)
        
class StudStartWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        client=MongoClient()
        db=client.stud
        self.posts=db.posts
        self.ques=db.ques
        self.company=db.company
        self.comp_analysis = db.comp_analysis
        self.notify=Notify()
        
        
        
        #display_post
        scrn_post_content=self.ids.scrn_post_contents
        posts=self.get_Posts()
        prod_tabel=DataTabel(tabel=posts)
        scrn_post_content.add_widget(prod_tabel)
        
        #display ques
        scrn_que_content=self.ids.scrn_que_contents
        ques=self.get_question()
        ques_tabel=DataTabel(tabel=ques)
        scrn_que_content.add_widget(ques_tabel)
        

        company_name=[]
        package=[]
        year=[]
        
        spinvals=[]
        
        for comp in self.company.find():
            company_name.append(comp['CompanyName'])
            package.append(comp['Package'])
            year.append(comp['Year'])
            
        for x in range(len(company_name)):
            line='|'.join([company_name[x],package[x],year[x]])
            if line not in spinvals:
                spinvals.append(line)
        self.ids.target_company.values=spinvals
    
    def write_post(self):
        
        scrn_que_contents=self.ids.scrn_que_contents
        scrn_que_contents.clear_widgets()
        
        user_name=self.ids.name_field
        year=self.ids.year_field
        post=self.ids.post_field
        
        user_name=user_name.text
        post=post.text
        year=year.text
        
        
        if user_name.strip()== '' or post.strip()=='' or year.strip()=='' :
            self.notify.add_widget(Label(text='[color=#FFF00][b]Provide Complete Information[/b][/color]',markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch,1)
        else:
            self.ques.insert_one({'UserName':user_name,'Posts':post})
            
            
        ques=self.get_question()
        questabel=DataTabel(tabel=ques)
        scrn_que_contents.add_widget(questabel)
    def get_Posts(self):
        
        client = MongoClient()
        db = client.stud
        posts = db.posts
        _posts = OrderedDict(
                    user_name={},
                    post_data={}
                )
        user_name=[]
        post_data=[]
        
        for post in posts.find():
            user_name.append(post['UserName'])
            post_data.append(post['Posts'])
            
        
        #print(passwords)
        posts_length=len(user_name)
        idx=0
        while idx<posts_length:
            _posts['user_name'][idx]=user_name[idx]
            _posts['post_data'][idx]=post_data[idx]
            idx +=1
        return _posts
    
    def get_question(self):
       
        client = MongoClient()
        db = client.stud
        ques = db.ques
        _ques = OrderedDict(
                    user_name={},
                    ques_data={}
                )
        user_name=[]
        ques_data=[]
        
        for que in ques.find():
            user_name.append(que['UserName'])
            ques_data.append(que['Posts'])
            
        
        #print(passwords)
        ques_length=len(user_name)
        idx=0
        while idx<ques_length:
            _ques['user_name'][idx]=user_name[idx]
            _ques['ques_data'][idx]=ques_data[idx]
            idx +=1
        return _ques
    
    def get_company(self):
        client = MongoClient()
        db = client.stud
        company = db.company
        _company = OrderedDict(
                    user_name={},
                    company_name={},
                    pckg={},
                    stat={},
                    year={}
                )
        user_name=[]
        company_name=[]
        pckg=[]
        stat=[]
        year=[]
        for com in company.find():
            user_name.append(com['UserName'])
            company_name.append(com['CompanyName'])
            pckg.append(com['Package'])
            stat.append(com['Status'])
            year.append(com['Year'])
        
            
        
        #print(passwords)
        com_length=len(user_name)
        idx=0
        while idx<com_length:
            _company['user_name'][idx]=user_name[idx]
            _company['company_name'][idx]=company_name[idx]
            _company['pckg'][idx]=pckg[idx]
            _company['stat'][idx]=stat[idx]
            _company['year'][idx]=year[idx]
            idx +=1
        return _company
    
    
    def killswitch(self,dtx):
        self.notify.dismiss()
        self.notify.clear_widgets()
    def view_stats(self):
        plt.cla()
        self.ids.analysis_res.clear_widgets()
        target_company = self.ids.target_company.text
        print(target_company)
        target=target_company.split('|')
        print(target)
        com=self.company.find_one({'CompanyName':target[0],'Package':target[1],'Year':target[2]})
        if com==None:
            print("Data Not Found")
        else:
            com1=self.company.count_documents({'CompanyName':target[0],'Package':target[1],'Year':target[2]})
            com2=self.company.count_documents({'CompanyName':target[0],'Package':target[1],'Year':target[2],'Status':"Yes"})
            
            
        with open('CompanyAnalysis.csv','w') as f:
            f.write('CompanyName,Package,Year,Total_stud,Selected_stud\n')
            line=','.join([str(target[0]),str(target[1]),str(target[2]),str(com1),str(com2)])
            f.write(line+'\n')
            
        
        df = pd.read_csv('CompanyAnalysis.csv')
        df.plot.bar(x='Year',y=['Total_stud','Selected_stud'])
        self.ids.analysis_res.add_widget(FCK(plt.gcf()))
        
    def change_screen(self,instance):
        if instance.text=='Post Your Question':
            self.ids.scrn_mngr.current='write_post_content'
        elif instance.text=='Company Analysis':
            self.ids.scrn_mngr.current='scrn_analysis'
        elif instance.text=='Recent posts':
            self.ids.scrn_mngr.current='scrn_post_content'
        elif instance.text=='Recent Questions':
            self.ids.scrn_mngr.current='scrn_que_content'
    def back(self):
        self.parent.parent.current='scrn_si'        

class StudStartApp(App):
    # signin class inherit from App class
    def build(self):
        # build is inbuilt function n App class use for Layout
        return StudStartWindow()


if __name__ == "__main__":
    # here we are creating a object sa of SigninApp class
    sa = StudStartApp()
    sa.run()
    # run is inbuilt function in App class
