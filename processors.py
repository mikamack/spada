import yaml
import shutil

import sys,os
sys.path.append(os.getcwd())
from widgets import TimeStamp, TableView, ImageGallery

import tkinter as tk
from tkinter import ttk
class UIDataAdd:
   
   item_list=[]
   var=0
  
   
   def create_notebook(self,pos_x,pos_y,width,height,parwn):
      '''Create tabs control (Notebook) and place it to dialog/tab'''
      new_tabc = ttk.Notebook(parwn)
      new_tabc.place(x=pos_x, y=pos_y, height=height, width=width)
      
      return new_tabc
   
   def add_tab(self,parwn,label):
      '''Add tab to dedicated Notebook and fill the heading label for the tab'''
      new_tab=ttk.Frame(parwn)
      parwn.add(new_tab, text=label)
      
      return new_tab
       

   def create_item(self,item,tabc):
      '''Create/tune item @ dedicated tab '''
      match (item['type']):
         case('TimeStamp'):
            val=tk.StringVar(master=None, value='1970-01-01 00:00', name=item['id'])
            ts=TimeStamp(tabc, item['label'], item['pos_x'], item['pos_y'], datetime_value=val)
            return {ts:val}
         case ('Entry'): 
            val=tk.StringVar(master=None,value='',name=item['id'])
            
            entry= ttk.Entry(tabc, textvariable=val)
            entry.place(x=item['pos_x'],y=item['pos_y'])
            return {entry:val}
         case('TableView'):
            val=tk.StringVar(value=str([]), name=item['id'])
            tv=TableView(tabc,parameter=item['label'],textvariable=val,width=item['width'], height=item['height'],pos_x=item['pos_x'],pos_y=item['pos_y'])
            return {tv:val}
         case ('ImageGallery'):
            val = tk.StringVar(value=str([]), name=item['id'])
            ig=ImageGallery(tabc,parameter=item['id'],textvariable=val,width=item['width'],height=item['height'],pos_x=item['pos_x'],pos_y=item['pos_y'])
            return {ig:val}
         case ('Button'):
            btn = ttk.Button(tabc, text=item['label'])
            btn.place(x=item['pos_x'],y=item['pos_y'])
            return {btn:0} #'0' - only render
         case ('Tab'):
            tab=self.add_tab(tabc, item['label'])
            return tab
         case ('Checkbutton'):
            val=tk.BooleanVar(master=None,value=False,name=item['id'])
            chkbtn=tk.Checkbutton(tabc, variable=val)
            chkbtn.place(x=item['pos_x'],y=item['pos_y'])
            return {chkbtn:val}
         case ('Label'):
            lbl=ttk.Label(tabc,text=item['label'])
            lbl.place(x=item['pos_x'],y=item['pos_y'])
            return {lbl:0} # '0' - render only
         case ('LabelFrame'):

            lfr=ttk.LabelFrame(tabc, text=item['label'], height=item['height'], width=item['width'])
            lfr.place(x=item['pos_x'],y=item['pos_y'])
            return {lfr:0}
         case ('Listbox'):
            val=tk.StringVar(master=None,value=item['values'],name=item['id'])
            lbx=tk.Listbox(tabc, listvariable=val, selectmode=tk.SINGLE, height=item['height'], width=item['width'])
            lbx.place(x=item['pos_x'],y=item['pos_y'])
            return {lbx:val}
         case ('Scale'):
            val=tk.DoubleVar(master=None,value=0.0,name=item['id'])
            scl=tk.Scale(tabc,length=item['length'],orient=item['orient'],from_=item['from'], to=item['to'], resolution=item['resolution'],variable=item['id'])
            scl.place(x=item['pos_x'],y=item['pos_y'])
            return {scl:val}
         case ('Radiobutton'):
            val=tk.StringVar(master=None,name=item['id'])
            rdb=tk.Radiobutton(tabc,text=item['label'],value=item['value'],variable=val)
            rdb.place(x=item['pos_x'], y=item['pos_y'])
            
            return {rdb:val}
            
         case ('Spinbox'):
            val=tk.DoubleVar(master=None,value=item['from'],name=item['id'])
            spn=tk.Spinbox(tabc,from_=item['from'],to=item['to'],width=item['width'],increment=item['increment'],textvariable=val)
            spn.place(x=item['pos_x'],y=item['pos_y'])
            
            return {spn:val}
         case('Progressbar'):
            
            progb=ttk.Progressbar(tabc,orient=item['orient'], maximum=item['maximum'],mode=item['mode'],variable=item['id'])
            progb.place(x=item['pos_x'], y=item['pos_y'])
            return {progb:0}
         case('Text'):
            
            txt=tk.Text(tabc,height=item['height'],width=item['width'],wrap='word',name=item['id'])
            txt.place(x=item['pos_x'],y=item['pos_y'])
            return {txt:item['id']}
         case('Treeview'):
            tbl=ttk.Treeview(tabc,columns=item['columns'])
            i=0
            for head_title in item['columns']:
               tbl.heading('#'+str(i), text=head_title)
               i=i+1
            tbl.place(x=item['pos_x'],y=item['pos_y'])
         
            return {tbl:0}
         case ('Combobox'):
            val=tk.StringVar(master=None,value='',name=item['id'])
            lbx=ttk.Combobox(tabc, textvariable=item['id'], values=item['values'], exportselection=0, height=item['height'], width=item['width'])
            lbx.place(x=item['pos_x'],y=item['pos_y'])
            return {lbx:val}
         case _:
            return {0:0}
 
 
   def render_gui(self,src,target):
      '''Renders content of src list to tabs'''
      for items in range(0, len(src)):
      
        if (src[items]['type'] == 'Tab'):
           if (src[items-1]['type'] != 'Tab' or items == 0):
              target=self.create_notebook(src[items]['pos_x'],src[items]['pos_y'],src[items]['width'],src[items]['height'],target)
           tmp=self.add_tab(target,src[items]['label'])
           self.render_gui(src[items]['content'],tmp)
        else:
           creat_item = self.create_item(src[items],target)
           if (list(creat_item.keys())[0] != 0): # omit zeroed elements in item list
            self.item_list.append(creat_item)
      return self.item_list