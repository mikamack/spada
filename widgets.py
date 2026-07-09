
import tkinter as tk
from datetime import datetime
from tkinter import dialog
from tkinter import ttk
import sys,os

class TimeStamp(ttk.Frame):
   def __init__(self, parwn, label_text, pos_x, pos_y, datetime_value, *args, **kwargs): 
        self.name = kwargs.pop("name", 'name')
        super().__init__(parwn, *args, **kwargs)
        self.lab=ttk.Label(parwn,text=label_text)
        self.lab.place(x=pos_x,y=pos_y)
        self.reg = self.winfo_toplevel().register(self.validate_date)        
        self.dd=ttk.Entry(parwn,width=15,textvariable=datetime_value,validate="key", validatecommand=(self.reg, "%d", "%i", "%S", "%P"))
        self.dd.place(x=pos_x,y=pos_y+20)
     
   def cget(self,param):
       '''Get option from widget'''
       if param == 'date_value':
            return super().cget(param)
   
   def configure(self,cnf=None,**kwargs):
       '''Set option for widget'''
       if "value" in kwargs:
            param = kwargs.pop("date_value")
            self.initial_date.set(param)
       super().configure(cnf, **kwargs)
   
   def validate_date(self, action, index, inserted_text, future_text):
       '''Validating the input field of datetime'''
       if action == '0':
           return True         
       idx = int(index)
       if len(future_text) > 16:
           return False
       if idx == 11:
           if inserted_text in "012":
               return True
           return False
       if idx == 13:
           if inserted_text == ':':
               return True
           return False
       elif idx ==4 or idx ==7:
           if inserted_text == '-':
               return True
           return False
       elif idx == 10:
           if inserted_text == ' ':
               return True
           return False
       elif idx ==5:
           if int(inserted_text) == 1 or int(inserted_text) == 0:
               return True
           return False
       elif idx ==8:
           if int(inserted_text) == 0 or int(inserted_text) == 1 or int(inserted_text) == 2 or int(inserted_text) == 3 :
               return True
           return False            
       else:
           if inserted_text.isdigit():
               return True
           return False
