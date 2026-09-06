import ast
import json
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from tksheet import Sheet
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
        self.dd=ttk.Entry(parwn,width=16,textvariable=datetime_value,validate="key", validatecommand=(self.reg, "%d", "%i", "%S", "%P"))
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
       if idx ==12:
           if future_text[11] == '2' and inserted_text in "0123":
               return True
           if (future_text[11] == '1' or future_text[11] == '0') and inserted_text.isdigit():
               return True
           return False
       if idx ==13:
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
       elif idx ==14:
           if inserted_text in "012345":
              return True
           return False
       else:
           if inserted_text.isdigit():
               return True
           return False
class TableView(tk.Frame):
    def __init__(self,parwn,parameter,width,height,pos_x,pos_y,textvariable, **kwargs):
       tk.Frame.__init__(self,parwn)
    #   if textvariable is not None:
    #       if not isinstance(textvariable, tk.StringVar):
    #          raise TypeError("textvariable must be a ListVar object")
    #       self.textvariable=textvariable
    #   else:
    #        self.textvariable = tk.StringVar(self)

       self.textvariable=textvariable
       self.param_var=tk.StringVar(value='')
       self._updating = False

       self.lg = ttk.LabelFrame(parwn,text=parameter,height=height+50,width=width+50)
       self.lg.place(x=pos_x-25,y=pos_y-15)

       self.tv = ttk.Treeview(parwn,columns=["DateTime",str(parameter)],show="headings",height=int(height/22))
       self.tv.heading("DateTime", text="Datetime")
       self.tv.heading(str(parameter), text=parameter)
       self.tv.column("DateTime",width=int(width*0.55),anchor="w")
       self.tv.column(str(parameter), width=int(width*0.35),anchor="w")
       self.tv.place(x=pos_x+10,y=pos_y+1)
       self.scrollbar = ttk.Scrollbar(parwn, orient="vertical", command=self.tv.yview)
       self.scrollbar.place(x=pos_x+width-20,y=pos_y+1,height=height)
       self.tv.configure(yscrollcommand=self.scrollbar.set)

       self.btn_add = ttk.Button(parwn, text="+", width=3, command = lambda: self._add_button())
       self.btn_add.place(x=pos_x+155,y=pos_y+height+5)
       self.btn_del = ttk.Button(parwn, text="-", width=3, command = lambda: self._del_button())
       self.btn_del.place(x=pos_x+50,y=pos_y+height+5)
       self.param = ttk.Entry(parwn,width=12,textvariable=self.param_var)
       self.param.place(x=pos_x+195,y=pos_y+height+5)

       self.textvariable.trace_add("write", lambda *args: self._update_widget(self.textvariable.get()))
       self._update_widget(self.textvariable.get())

    def _add_button(self):
       '''Handler for + button'''
       if self.param_var.get() == '':
           messagebox.showerror('Error', "Add parameter to include to TimeSeries")
           return
       self.tv.insert("",index="end",values=[str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),self.param_var.get()])
       self.param_var.set('')
       self._update_data()

    def _del_button(self):
        '''Handler for - button'''
        row_index_list=self.tv.get_children()
        self.tv.delete(row_index_list[-1])
        self._update_data()

    def _update_data(self):
        '''for control var update'''
        self._updating = True

        
        row_index_list=self.tv.get_children()
        result_data=[]
        for row_index in row_index_list:
            row_values =self.tv.item(row_index, "values")
            result_data.append(list(row_values))

        self.textvariable.set(str(result_data))
        self._updating = False

        return result_data

    def _update_widget(self,table_data):
        '''for widget update'''
        if self._updating:
            return
        for row_id in self.tv.get_children():
            self.tv.delete(row_id)
       
        for row in ast.literal_eval(table_data):
            self.tv.insert("",index="end",values=row)

