from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from collections import OrderedDict
from pymongo import MongoClient
from utils.datatabel import DataTabel
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.modalview import ModalView
from datetime  import datetime
import hashlib
from kivy.clock import Clock
import pandas as pd
import matplotlib.pyplot as plt
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg as FCK
from kivy.lang import Builder

Builder.load_file('admin/admin.kv')


class Notify(ModalView):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.size_hint=(.7,.7)
        
class AdminWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        client=MongoClient()
        db=client.stud
        self.users=db.users
        self.posts=db.posts
        self.ques=db.ques
        self.company=db.company
        self.comp_analysis = db.comp_analysis
        self.notify=Notify()
        
        content=self.ids.scrn_contents
        users=self.get_user()
        usertabel=DataTabel(tabel=users)
        content.add_widget(usertabel)
        
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
        
        #display company
        scrn_company_content=self.ids.scrn_company_contents
        company=self.get_company()
        company_tabel=DataTabel(tabel=company)
        scrn_company_content.add_widget(company_tabel)
        
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
                
        

    def add_user_feilds(self):
        target = self.ids.ops_feilds
        target.clear_widgets()
        crud_user = TextInput(hint_text="User Name")
        crud_pwd = TextInput(hint_text="Password")
        crud_year = TextInput(hint_text="FE/SE/TE/BE")
        crud_submit=Button(text='ADD',size_hint_x=None,width=100,on_release=lambda x:self.add_user(crud_user.text,crud_pwd.text,crud_year.text))
        
        target.add_widget(crud_user)
        target.add_widget(crud_pwd)
        target.add_widget(crud_year)
        target.add_widget(crud_submit)
    
    def add_user(self, user,pwd,year):
        content=self.ids.scrn_contents
        content.clear_widgets()
        
        if user.strip()== '' or pwd.strip()=='' or year.strip()=='':
            self.notify.add_widget(Label(text='[color=#FFF00][b]Provide Complete Information[/b][/color]',markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch,1)
        else:
            com=self.users.find_one({'UserName':user})
            if com==None:
                self.users.insert_one({'UserName':user,'Password':pwd,'Year':year})
                
            else:
                self.notify.add_widget(Label(text='[color=#FF000][b]UserName Is Present Try Another[/b][/color]',markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch,1)
            
        
        users=self.get_user()
        usertabel=DataTabel(tabel=users)
        content.add_widget(usertabel)
    def update_user_feilds(self):
        target=self.ids.ops_feilds
        target.clear_widgets()
        crud_user = TextInput(hint_text="User Name",multiline=False)
        crud_pwd = TextInput(hint_text="Password",multiline=False)
        crud_year = TextInput(hint_text="FE/SE/TE/BE",multiline=False)
        crud_submit=Button(text='Update',size_hint_x=None,width=100,on_release=lambda x:self.update_user(crud_user.text,crud_pwd.text,crud_year.text))
        
        target.add_widget(crud_user)
        target.add_widget(crud_pwd)
        target.add_widget(crud_year)
        target.add_widget(crud_submit)
    def update_user(self,user,pwd,year):
        content=self.ids.scrn_contents
        content.clear_widgets()
        
        if user.strip()== '' or pwd.strip()=='' or year.strip()=='' :
            self.notify.add_widget(Label(text='[color=#FFF00][b]Provide Complete Information[/b][/color]',markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch,1)
        else:
            com=self.users.find_one({'UserName':user})
            if com==None:
                self.notify.add_widget(Label(text='[color=#FF000][b]Data Not Present[/b][/color]',markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch,1)
            
            else:
                
                self.users.update_one({'UserName':user},{'$set':{'UserName':user,'Password':pwd,'Year':year}})
        
        users=self.get_user()
        usertabel=DataTabel(tabel=users)
        content.add_widget(usertabel)
    
    def remove_user_feilds(self):
        target=self.ids.ops_feilds
        target.clear_widgets()
        crud_user = TextInput(hint_text="User Name")
        crud_submit=Button(text='Remove',size_hint_x=None,width=100,on_release=lambda x:self.remove_user(crud_user.text))
        
        target.add_widget(crud_user)
        target.add_widget(crud_submit)
    def remove_user(self,user):
        content=self.ids.scrn_contents
        content.clear_widgets()
        
        if user.strip()== '':
            self.notify.add_widget(Label(text='[color=#FFF00][b]Provide Complete Information[/b][/color]',markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch,1)
        else:
            com=self.users.find_one({'UserName':user})
            if com==None:
                self.notify.add_widget(Label(text='[color=#FF000][b]Data Not Present[/b][/color]',markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch,1)
            else:
                self.users.remove({'UserName':user})
        
        users=self.get_user()
        usertabel=DataTabel(tabel=users)
        content.add_widget(usertabel)
        
    def add_post_feilds(self):
        target = self.ids.ops_feilds_p
        target.clear_widgets()
        crud_user = TextInput(hint_text="User Name")
        crud_post = TextInput(hint_text="Post")
        crud_submit=Button(text='ADD',size_hint_x=None,width=100,on_release=lambda x:self.add_post(crud_user.text,crud_post.text))
        
        target.add_widget(crud_user)
        target.add_widget(crud_post)
        target.add_widget(crud_submit)
   
    
    
    def add_post(self, user,post):
        content=self.ids.scrn_post_contents
        content.clear_widgets()
        
        if user.strip()== '' or post.strip()=='' :
            self.notify.add_widget(Label(text='[color=#FFF00][b]Provide Complete Information[/b][/color]',markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch,1)
        else:
            self.posts.insert_one({'UserName':user,'Posts':post})
        
        posts=self.get_Posts()
        posttabel=DataTabel(tabel=posts)
        content.add_widget(posttabel)
        
    def update_post_feilds(self):
        target=self.ids.ops_feilds_p
        target.clear_widgets()
        crud_user = TextInput(hint_text="User Name")
        crud_post = TextInput(hint_text="Post")
        crud_submit=Button(text='Update',size_hint_x=None,width=100,on_release=lambda x:self.update_post(crud_user.text,crud_post.text))
        
        target.add_widget(crud_user)
        target.add_widget(crud_post)
        target.add_widget(crud_submit)
    def update_post(self,user,post):
        content=self.ids.scrn_post_contents
        content.clear_widgets()
        
        if user.strip()== '' or post.strip()=='' :
            self.notify.add_widget(Label(text='[color=#FFF00][b]Provide Complete Information[/b][/color]',markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch,1)
        else:
            com=self.posts.find_one({'UserName':user})
            if com==None:
                self.notify.add_widget(Label(text='[color=#FF000][b]Data Not present[/b][/color]',markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch,1)
            else:
                self.posts.update_one({'UserName':user},{'$set':{'UserName':user,'Posts':post}})
        
        posts=self.get_Posts()
        posttabel=DataTabel(tabel=posts)
        content.add_widget(posttabel)   
    
    def remove_post_feilds(self):
        target=self.ids.ops_feilds_p
        target.clear_widgets()
        crud_user = TextInput(hint_text="User Name")
        crud_submit=Button(text='Remove',size_hint_x=None,width=100,on_release=lambda x:self.remove_post(crud_user.text))
        
        target.add_widget(crud_user)
        target.add_widget(crud_submit)
    
    def remove_post(self,user):
        content=self.ids.scrn_post_contents
        content.clear_widgets()
        
        if user.strip()== '':
            self.notify.add_widget(Label(text='[color=#FFF00][b]Provide Complete Information[/b][/color]',markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch,1)
        else:
            com=self.posts.find_one({'UserName':user})
            if com==None:
                self.notify.add_widget(Label(text='[color=#FF000][b]Data Not Present[/b][/color]',markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch,1)
            else:
                self.posts.remove({'UserName':user})
        
        posts=self.get_Posts()
        posttabel=DataTabel(tabel=posts)
        content.add_widget(posttabel) 
        
        
        
        
    def add_que_feilds(self):
        target = self.ids.ops_feilds_q
        target.clear_widgets()
        crud_user = TextInput(hint_text="User Name")
        crud_ques = TextInput(hint_text="question")
        crud_submit=Button(text='ADD',size_hint_x=None,width=100,on_release=lambda x:self.add_que(crud_user.text,crud_ques.text))
        
        target.add_widget(crud_user)
        target.add_widget(crud_ques)
        target.add_widget(crud_submit)
   
    
    
    def add_que(self, user,que):
        content=self.ids.scrn_que_contents
        content.clear_widgets()
        
        self.ques.insert_one({'UserName':user,'Posts':que})
        
        ques=self.get_question()
        ques_tabel=DataTabel(tabel=ques)
        content.add_widget(ques_tabel)
        
    def update_que_feilds(self):
        target=self.ids.ops_feilds_q
        target.clear_widgets()
        crud_user = TextInput(hint_text="User Name")
        crud_ques = TextInput(hint_text="Question")
        crud_submit=Button(text='Update',size_hint_x=None,width=100,on_release=lambda x:self.update_que(crud_user.text,crud_ques.text))
        
        target.add_widget(crud_user)
        target.add_widget(crud_ques)
        target.add_widget(crud_submit)
    def update_que(self,user,ques):
        content=self.ids.scrn_que_contents
        content.clear_widgets()
        
        if user.strip()== '' or ques.strip()=='' :
            self.notify.add_widget(Label(text='[color=#FFF00][b]Provide Complete Information[/b][/color]',markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch,1)
        else:
            com=self.ques.find_one({'UserName':user})
            if com==None:
                self.notify.add_widget(Label(text='[color=#FF000][b]Data Not Present[/b][/color]',markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch,1)
            else:
                self.ques.update_one({'UserName':user},{'$set':{'UserName':user,'Posts':ques}})
        
        ques=self.get_question()
        ques_tabel=DataTabel(tabel=ques)
        content.add_widget(ques_tabel)  
    
    def remove_que_feilds(self):
        target=self.ids.ops_feilds_q
        target.clear_widgets()
        crud_user = TextInput(hint_text="User Name")
        crud_submit=Button(text='Remove',size_hint_x=None,width=100,on_release=lambda x:self.remove_que(crud_user.text))
        
        target.add_widget(crud_user)
        target.add_widget(crud_submit)
    
    def remove_que(self,user):
        content=self.ids.scrn_que_contents
        content.clear_widgets()
        
        if user.strip()== '' :
            self.notify.add_widget(Label(text='[color=#FFF00][b]Provide Complete Information[/b][/color]',markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch,1)
        else:
            com=self.ques.find_one({'UserName':user})
            if com==None:
                self.notify.add_widget(Label(text='[color=#FF000][b]Data Not Present[/b][/color]',markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch,1)
            else:
                self.ques.remove({'UserName':user})
        
        ques=self.get_question()
        ques_tabel=DataTabel(tabel=ques)
        content.add_widget(ques_tabel)
        
        
        
        
        
    def add_company_feilds(self):
        target = self.ids.ops_feilds_c
        target.clear_widgets()
        crud_user = TextInput(hint_text="User Name")
        crud_company = TextInput(hint_text="Company Name")
        crud_pckg = TextInput(hint_text="Package (3.5,7,5)")
        crud_status = TextInput(hint_text="Yes/No")
        crud_year = TextInput(hint_text="2019,2020")
        
        
        crud_submit=Button(text='ADD',size_hint_x=None,width=100,on_release=lambda x:self.add_company(crud_user.text,crud_company.text,crud_pckg.text,crud_status.text,crud_year.text))
        
        target.add_widget(crud_user)
        target.add_widget(crud_company)
        target.add_widget(crud_pckg)
        target.add_widget(crud_status)
        target.add_widget(crud_year)
        target.add_widget(crud_submit)
   
    
    
    def add_company(self, user,company,pckg,status,year):
        content=self.ids.scrn_company_contents
        content.clear_widgets()
        
        if user.strip()== '' or company.strip()=='' or pckg.strip()=='' or status.strip()=='' or year.strip()=='' :
            self.notify.add_widget(Label(text='[color=#FFF00][b]Provide Complete Information[/b][/color]',markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch,1)
        else:
            self.company.insert_one({'UserName':user,'CompanyName':company,'Package':pckg,'Status':status,'Year':year})
        
        company=self.get_company()
        company_tabel=DataTabel(tabel=company)
        content.add_widget(company_tabel)
        
    def update_company_feilds(self):
        
        target=self.ids.ops_feilds_c
        target.clear_widgets()
        crud_user = TextInput(hint_text="User Name")
        crud_company = TextInput(hint_text="Company Name")
        crud_pckg = TextInput(hint_text="Package (3.5,7,5)")
        crud_status = TextInput(hint_text="Yes/No")
        crud_year = TextInput(hint_text="2019,2020")
        
        
        crud_submit=Button(text='ADD',size_hint_x=None,width=100,on_release=lambda x:self.update_company(crud_user.text,crud_company.text,crud_pckg.text,crud_status.text,crud_year.text))
        
        target.add_widget(crud_user)
        target.add_widget(crud_company)
        target.add_widget(crud_pckg)
        target.add_widget(crud_status)
        target.add_widget(crud_year)
        target.add_widget(crud_submit)
    def update_company(self,user,company,pckg,status,year):
        content=self.ids.scrn_company_contents
        content.clear_widgets()
        
        if user.strip()== '' or company.strip()=='' or pckg.strip()=='' or status.strip()=='' or year.strip()=='' :
            self.notify.add_widget(Label(text='[color=#FFF00][b]Provide Complete Information[/b][/color]',markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch,1)
        else:
            com=self.company.find_one({'UserName':user,'CompanyName':company})
            if com==None:
                self.notify.add_widget(Label(text='[color=#FF000][b]Data Not Present[/b][/color]',markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch,1)
            else:
                self.company.update_one({'UserName':user},{'$set':{'UserName':user,'CompanyName':company,'Package':pckg,'Status':status,'Year':year}})

        
        company=self.get_company()
        company_tabel=DataTabel(tabel=company)
        content.add_widget(company_tabel)  
    
    def remove_company_feilds(self):
        target=self.ids.ops_feilds_c
        target.clear_widgets()
        crud_user = TextInput(hint_text="User Name")
        crud_submit=Button(text='Remove',size_hint_x=None,width=100,on_release=lambda x:self.remove_company(crud_user.text))
        
        target.add_widget(crud_user)
        target.add_widget(crud_submit)
    
    def remove_company(self,user):
        content=self.ids.scrn_company_contents
        content.clear_widgets()
        
        if user.strip()== '':
            self.notify.add_widget(Label(text='[color=#FFF00][b]Provide Complete Information[/b][/color]',markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch,1)
        else:
            com=self.company.find_one({'UserName':user})
            if com==None:
                self.notify.add_widget(Label(text='[color=#FF000][b]Data Not Present[/b][/color]',markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch,1)
            else:
                self.company.remove({'UserName':user})

        
        
        company=self.get_company()
        company_tabel=DataTabel(tabel=company)
        content.add_widget(company_tabel)
        
    def get_user(self):
        client = MongoClient()
        db = client.stud
        users = db.users
        _users = OrderedDict(
                    user_name={},
                    passwords={}
                )
        user_name=[]
        passwords=[]
        
        for user in users.find():
            user_name.append(user['UserName'])
            passwords.append(user['Password'])
        
        #print(passwords)
        users_length=len(user_name)
        idx=0
        while idx<users_length:
            _users['user_name'][idx]=user_name[idx]
            _users['passwords'][idx]=passwords[idx]
            idx +=1
        return _users
    
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
        
    def back(self):
        self.parent.parent.current='scrn_si'
        
    def change_screen(self,instance):
        if instance.text=='Manage posts':
            self.ids.scrn_mngr.current='scrn_post_content'
        elif instance.text=='Manage users':
            self.ids.scrn_mngr.current='scrn_content'
        elif instance.text=='Analysis':
            self.ids.scrn_mngr.current='scrn_analysis'
        elif instance.text=='Manage questions':
            self.ids.scrn_mngr.current='scrn_que_content'
        elif instance.text=='Manage company':
            self.ids.scrn_mngr.current='scrn_company_content'
    
class AdminApp(App):
    def build(self):
        return AdminWindow()




if __name__ == "__main__":
    w = AdminApp()
    w.run()
