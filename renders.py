
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import dialog
import sys,os
import yaml
import processors

sys.path.append(os.getcwd())
import handlers

from handlers import UIHandler


class UIRender:
    
    #counter for search dialog's widgetsets
    index_factor=0
    #StringVars controls for searching critirias
    query_param = []
    query_condition = []
    query_value = []
    query_combination = []

    query_cbx = []
    query_cbx_combination = []
    query_cbx_condition = []
    query_entry_value = []

    table_list=''
    # dictionary for search parameters: 'label':'id'. after selecting label in search
    # dialog defines id and then passing to searching in db
    value_items={}

    def register_ui(self,header):
       '''Dialog for register the user. Call when no database found/created/first started'''
       h = UIHandler()
       dialog=self.render_ui(header)
       login=''
       pwd=''
       pwd_c=''
       login_label=ttk.Label(dialog,text='New Login:')
       login_label.place(x=15,y=50)
       login_text=ttk.Entry(dialog, textvariable=login)
       login_text.place(x=150,y=50)
       pwd_label=ttk.Label(dialog,text='New Password: ')
       pwd_label.place(x=15,y=90)
       pwd_text= ttk.Entry(dialog, textvariable=pwd)
       pwd_text.place(x=150,y=90)
       pwd_label=ttk.Label(dialog,text='Confirm Password: ')
       pwd_label.place(x=15,y=130)
       pwd_textc= ttk.Entry(dialog, textvariable=pwd_c)
       pwd_textc.place(x=150,y=130)
       param=dialog
       login_btn=ttk.Button(dialog, text='Regist4r', width=25, command=lambda: self.blur_register_ui(h,login_text,pwd_text,pwd_textc,param))
       login_btn.place(x=90,y=160)
       exit_btn=ttk.Button(dialog,text='Exit',width=25, command=lambda: h.press_exit(param))
       exit_btn.place(x=90,y=210)
       return dialog

    def login_ui(self,header):
       '''Dialog for log in. When user created.'''
       login=''
       pwd=''
       h = UIHandler()
       dialog=self.render_ui(header)
       param=dialog
       login_label=ttk.Label(dialog,text='Login:')
       login_label.place(x=15,y=50)
       login_text=ttk.Entry(dialog, textvariable=login)
       login_text.place(x=100,y=50)
       pwd_label=ttk.Label(dialog,text='Password: ')
       pwd_label.place(x=15,y=90)
       pwd_text= ttk.Entry(dialog, textvariable=pwd, show='*')
       pwd_text.place(x=100,y=90)
       
       
       param=dialog
       
       login_btn=ttk.Button(dialog, text='Login', width=25, command=lambda: self.blur_login_ui(h,login_text,pwd_text,param))
       login_btn.place(x=50,y=120)
       exit_btn=ttk.Button(dialog,text='Exit', width=25, command=lambda: h.press_exit(param))
       exit_btn.place(x=50,y=160) 
       login_text.get()
       pwd_text.get()
       return dialog
   
    def render_ui(self, header):
       '''Common caller for register/log on'''
       dialog = tk.Toplevel()
       dialog.title(header)
       dialog.geometry("350x260")
       return dialog
   
    def render_main_ui(self, header, dialog):
       '''Head windows dialog'''
       h = UIHandler()
       dialog.title(header)
       dialog.geometry("750x520")
       label=tk.Label(dialog, text="Main")
       label.place(x=100,y=160)
       button_add=tk.Button(dialog,text='Add',command = lambda: self.render_add_ui())
       button_add.place(x=150,y=480)
       button_search=tk.Button(dialog,text='Search', command = lambda: self.render_search_ui(dialog))
       button_search.place(x=210,y=480)
       button_edit=tk.Button(dialog,text='Edit', command = lambda: self.render_edit_ui())
       button_edit.place(x=300,y=480)
       button_delete=tk.Button(dialog, text='Delete', command = lambda: h.delete_button(self.table_list))
       button_delete.place(x=360,y=480)
       button_delete=tk.Button(dialog, text='Send to print', command = lambda: self.render_print_data())
       button_delete.place(x=440,y=480)

       table_list_columns=("Id","","Field","Field 2","Field3","Field4","Field5","Field6","Field7","Field8")
       self.table_list=ttk.Treeview(dialog, columns=table_list_columns, padding=(0,0,15,15), selectmode = 'browse', show="headings")
       j=0
       while j < len(table_list_columns):
          self.table_list.column("#"+str(j), width=60)
          j+=1
       self.table_list.place(x=30,y=50)
       vs_table_list = ttk.Scrollbar(self.table_list, orient = 'vertical', command=self.table_list.yview)
       hs_table_list = ttk.Scrollbar(self.table_list, orient = 'horizontal', command=self.table_list.xview)
       vs_table_list.place(x=743, y=0, height=220)
       hs_table_list.place(x=0, y=220, width=756)
       
       self.table_list.configure(yscrollcommand=vs_table_list.set)
       self.table_list.configure(xscrollcommand=hs_table_list.set)

    def blur_login_ui(self, handler, login, pwd, dialog):
       '''Login UI dialog hiding'''
       list_widgets = dialog.winfo_children()
       if handler.press_login(login, pwd) == 1:
          for item in list_widgets:
             item.destroy()
          self.render_main_ui('BILC', dialog)
 
    def blur_register_ui(self, handler, login, pwd, pwd_c, dialog):
       '''Register UI dialog hiding'''
       list_widgets = dialog.winfo_children()
       if handler.press_register(login, pwd, pwd_c) == 1:
          for item in list_widgets:
             item.destroy()
          self.render_main_ui('BILC', dialog)
   
    def render_add_ui(self):
       '''Dialog for addition data to BILC's db'''
       h = UIHandler()

       add_dialog=tk.Toplevel()
       add_dialog.title('Add data')
       
       try:
         stream = open('yaml/gui.yaml', 'r')
         res = yaml.safe_load(stream)
       except OSError:
         messagebox.showerror('Error','Something wrong with file yaml')
       da = processors.UIDataAdd()

       add_dialog.geometry(str(res['width'])+"x"+str(res['height']))
       elements_list=da.render_gui(res['content'],add_dialog)
       add_button=ttk.Button(add_dialog, text="Add",command = lambda: h.add_button(add_dialog,elements_list))
       add_button.place(x=res['width']/4,y=600)
    
    def render_search_ui(self, dialog):
       '''Renders a search dialog'''
       
       res=[]
       def search_closing():
         '''Callback for zeroing lists of widgets and control variables within search dialog'''
         self.query_param.clear()
         self.query_condition.clear()
         self.query_combination.clear()
         self.query_value.clear()

         self.query_cbx.clear()
         self.query_cbx_combination.clear()
         self.query_cbx_condition.clear()
         self.query_entry_value.clear()
         query_dialog.destroy()
         self.index_factor=0
       
      
       h = UIHandler()
       self.index_factor=0
       query_dialog = tk.Toplevel()
       query_dialog.title ("Search data")
       query_dialog.geometry("640x480")
       
 
       self.query_param.append(tk.StringVar())
       self.query_condition.append(tk.StringVar())
       self.query_value.append(tk.StringVar())
       self.query_combination.append(tk.StringVar())
       x_pos=30
       y_pos=40
       
       query_dialog.protocol("WM_DELETE_WINDOW", search_closing)

       query_cbx_label = tk.Label(query_dialog,text='Parameter:')
       query_cbx_label.place(x=35,y=20)
       try:
         stream = open('yaml/gui.yaml', 'r')
         res = yaml.safe_load(stream)
       except OSError:
         messagebox.showerror('Error','Something wrong with file yaml')
       
       self.prepare_list(res['content'])
       self.query_cbx.append(ttk.Combobox(query_dialog, textvariable = self.query_param[0], values=list(self.value_items.keys()), exportselection = 0, height=10, width=25))
       self.query_cbx[self.index_factor].place(x=30,y=40)

       query_condition_label=tk.Label(query_dialog,text='Condition:')
       query_condition_label.place(x=260,y=20)
       
       result=ttk.Combobox(query_dialog, textvariable = self.query_condition[0], values=['<','=','!=','>'], exportselection = 0, height=4, width=2)
       self.query_cbx_condition.append(result)
       self.query_cbx_condition[self.index_factor].place (x=280,y=40)
       
       query_value_label=tk.Label(query_dialog,text="Value:")
       query_value_label.place(x=340,y=20)
       
       self.query_entry_value.append(ttk.Entry(query_dialog,textvariable=self.query_value[0]))
       self.query_entry_value[self.index_factor].place(x=340,y=40)
       query_value_label=tk.Label(query_dialog,text="AND/OR:")
       query_value_label.place(x=512,y=20)
       self.query_cbx_combination.append(ttk.Combobox(query_dialog, textvariable = self.query_combination[0], values=['AND','OR'], exportselection = 0, height=2, width=4))
       self.query_cbx_combination[self.index_factor].place (x=512,y=40)
       self.index_factor=self.index_factor+1
       query_add=tk.Button(query_dialog,text='+',width=1,command=lambda: self.render_add_search(query_dialog, x_pos, y_pos))
       query_del=tk.Button(query_dialog,text='-',width=1,command=lambda: self.render_del_search(self.query_param,self.query_condition,self.query_value,self.query_combination))
       query_add.place(x=590,y=40)
       query_del.place(x=590,y=70)
       query_start=tk.Button(query_dialog, text='Search', width=6, command=lambda: h.search_button(query_dialog,self.query_param, self.query_condition , self.query_value , self.query_combination , self.value_items, self.query_cbx, self.query_cbx_condition, self.query_cbx_combination, self.query_entry_value, self.table_list))
       query_start.place(x=x_pos+320,y=y_pos+400)
       
    def prepare_list(self,param):
       '''parsing labels and ids from yaml for preparing param list'''
       for i in param:
         if (i['type'] == 'Tab'):
             tmp=i['content']
             self.prepare_list(tmp)
         elif (i['type'] == 'Checkbutton' or i['type'] == 'Text' or i['type'] == 'Entry' or i['type'] == 'Listbox' or i['type'] == 'Scale' or i['type'] == 'Spinbox' or i['type'] == 'Combobox' or i['type'] == 'Radiobutton'):   
             self.value_items.update({i['label'] : i['id']})    
       
    def render_add_search(self,dialog,x_pos,y_pos):
      '''This is for addition group of widgets for search data''' 
      self.query_param.append(tk.StringVar())
      self.query_condition.append(tk.StringVar())
      self.query_value.append(tk.StringVar())
      self.query_combination.append(tk.StringVar())
       
      self.query_cbx.append(ttk.Combobox(dialog, textvariable = self.query_param[self.index_factor], values=list(self.value_items.keys()), exportselection = 0, height=10, width=25))
      self.query_cbx[self.index_factor].place(x=x_pos,y=y_pos*(self.index_factor+1))
      self.query_cbx_condition.append(ttk.Combobox(dialog, textvariable = self.query_condition[self.index_factor], values=['<','=','!=','>'], exportselection = 0, height=4, width=2))
      self.query_cbx_condition[self.index_factor].place (x=x_pos+250,y=y_pos*(self.index_factor+1))
      self.query_entry_value.append(ttk.Entry(dialog,textvariable=self.query_value[self.index_factor]))
      self.query_entry_value[self.index_factor].place(x=x_pos+310,y=y_pos*(self.index_factor+1))
      self.query_cbx_combination.append(ttk.Combobox(dialog, textvariable = self.query_combination[self.index_factor], values=['AND','OR'], exportselection = 0, height=2, width=4))
      self.query_cbx_combination[self.index_factor].place (x=x_pos+482,y=y_pos*(self.index_factor+1))
      self.index_factor=self.index_factor+1

    def render_del_search (self,query_param,query_condition,query_value,query_combination):
      '''This is for hiding the group of widgets for search data'''
      try:
          tmp1=self.query_cbx.pop()
          tmp2=self.query_cbx_combination.pop()
          tmp3=self.query_cbx_condition.pop()
          tmp4=self.query_entry_value.pop()
          query_param.pop()
          query_combination.pop()
          query_condition.pop()
          query_value.pop()
      except IndexError:
          return None
      tmp1.destroy()
      tmp2.destroy()
      tmp3.destroy()
      tmp4.destroy()

      self.index_factor=self.index_factor-1
    
    def render_edit_ui(self):
      if (self.table_list.selection() == ()):
         messagebox.showerror('Error','None selected. Make a search first')
         return 0

      edit_dialog=tk.Toplevel()
      edit_dialog.title("Edit data")
      
      try:
         stream = open('yaml/gui.yaml', 'r')
         res = yaml.safe_load(stream)
      except OSError:
         messagebox.showerror('Error','Something wrong with file yaml')
      edit_dialog.geometry(str(res['width'])+"x"+str(res['height']))
      edit_button=ttk.Button(edit_dialog, text="Update",command = lambda: h.update_button(edit_dialog,item_list, dict_data))
      edit_button.place(x=res['width']/2,y=res['height']-650)
       
      h = UIHandler()
      dict_data=h.edit_button(self.table_list)

      #Data edit dialog
      de = processors.UIDataAdd()
      try:
         stream = open('yaml/gui.yaml', 'r')
         res = yaml.safe_load(stream)
      except OSError:
         messagebox.showerror('Error','Something wrong with file yaml')
      de.item_list.clear()
      item_list=de.render_gui(res['content'],edit_dialog)
     
      for item in item_list:
         name_var=str(list(item.values())[0])
         if ('text' in list(item.keys())[0].widgetName):
            list(item.keys())[0].insert('1.0',dict_data.get(name_var))
         elif ('listbox' in list(item.keys())[0].widgetName):
            item_tuple=list(item.keys())[0].get(0,"end")
            for current in dict_data[name_var]:
               try:
                  index_to_select=item_tuple.index(current)
               except ValueError:
                  index_to_select=0
                  continue
               list(item.keys())[0].selection_set(index_to_select)
         elif('tableview' in list(item.keys())[0]._name):
            
            list(item.values())[0].set(dict_data.get(name_var))

         elif (list(item.values())[0] != 0 and dict_data.get(name_var) != None):
            list(item.values())[0].set(dict_data.get(name_var))
         elif (list(item.values())[0] == 0 and dict_data.get(name_var) != None):
            '''this should be exposed to user if he/she modified UI but old data for old UI has left in DB'''
            print ('Found unbound data: '+str(dict_data))
         else:
            continue    

    def render_print_data(self):
      if (self.table_list.selection() == ()):
         messagebox.showerror('Error','None selected. Make a search first')
         return 0
      
            
      try:
         stream = open('yaml/gui.yaml', 'r')
         yaml.safe_load(stream)
      except OSError:
         messagebox.showerror('Error','Something wrong with file yaml')
      
      row_index=self.table_list.selection()
      
      doc_id = self.table_list.item(row_index)['values'][0]
      h = UIHandler()
      h.print_button(doc_id)        
