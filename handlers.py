import yaml
import time
from pathlib import Path

import tkinter as tk
from tkinter import messagebox, ttk
import sys,os
sys.path.append(os.getcwd())
from auths import UIAuth
from db import DBHandler


class UIHandler:
    '''Variables for storing returned values from handlers'''
    v_press_register=0
    v_press_login=0
    v_press_exit=0
    '''Resultset table's width in columns'''
    TABLE_WIDTH_LIMIT=10
    
    '''Event handlers for buttons'''
    def press_register(self,login,passwd,passwd_c):
           ERROR_HEADING='Error!'
           lgn=login.get()
           pwd=passwd.get()
           pwd_c=passwd_c.get()
           print (lgn,pwd,pwd_c)
           if pwd != pwd_c:
              messagebox.showerror("Error!", "Password differs")
           elif (len(pwd)<6):
              messagebox.showerror(ERROR_HEADING, "Password too short")
           elif (len(pwd) == 0 | len(lgn) == 0):
              messagebox.showerror(ERROR_HEADING, 'Username/Password cannot be empty')  
           auth = UIAuth()
           auth.auth_user(lgn,pwd)
           self.v_press_register=1
           return self.v_press_register

    def press_exit(self,d):
           d.destroy()
           
    
    def press_login(self,login,passwd):
           lgn=login.get()
           pwd=passwd.get()
           ERROR_HEADING='Error!'
           if (len(pwd) == 0 | len(lgn) == 0):
              messagebox.showerror(ERROR_HEADING, 'Username/Password cannot be empty')
           auth = UIAuth()
           if auth.auth_user(lgn,pwd) != -1:
              self.v_press_login=1     
           else:
              messagebox.showerror(ERROR_HEADING, 'Wrong login/password.')
              self.v_press_login=-1
           return self.v_press_login
    
    def add_button(self,dialog,elements_list):
        '''Adds record to db from constructed UI. Needs a list of widgets, which data should be saved'''
        i=0
        result_dictionary={}
        dbc = DBHandler()
        try:
            for item in elements_list: 
                tmp_widget=list(item.keys())
                widget=tmp_widget[0]
                tmp_variable=list(item.values())
                control_var=tmp_variable[0]
                if ('entry' in widget.widgetName):
                     result_dictionary.update({str(widget.cget("textvariable")):control_var.get()})
                elif ('timestamp' in widget._w):
                     control_var.get()
                     result_dictionary.update({control_var._name:str(widget.cget("date_value"))})
                elif ('tableview' in widget._w):
                     control_var.get()
                     result_dictionary.update({control_var._name:str(control_var.get())})

                elif ('scale' in widget.widgetName):
                     #result_dictionary.update({str(widget.cget("name")):str(widget.cget("variable"))}) 
                     result_dictionary.update({str(widget.cget("variable")):control_var.get()}) 
                elif ('checkbutton' in widget.widgetName):
                     result_dictionary.update({str(widget.cget("variable")):control_var.get()})            
                elif ('listbox' in widget.widgetName):
                    i=widget.curselection()
                    tmp_result=[]
                    for var in i:
                        tmp_result.append(widget.get(var,None))
                    result_dictionary.update({str(widget.cget("listvariable")):tmp_result})
                elif ('spinbox' in widget.widgetName):
                    result_dictionary.update({str(widget.cget("textvariable")):control_var.get()})

                elif ('combobox' in widget.widgetName):
                    result_dictionary.update({str(widget.cget("textvariable")):control_var.get()})
                elif ('radiobutton' in widget.widgetName):
                    result_dictionary.update({str(widget.cget("variable")):control_var.get()})
                elif ('text' in widget.widgetName):
                    result_dictionary.update({widget._name:widget.get("1.0", "end-1c")})
                elif ('conbobox' in widget.widgetName):
                    result_dictionary.update({str(widget.cget("textvariable")):control_var.get()})
                else:
                     continue
               
            dbc.add_record('_data',result_dictionary)
            dialog.destroy()
        except KeyError:
            print ("Elements list is empty")
   
    def search_button(self, query_dialog, query_param, query_condition , query_value , query_combination ,value_dictionary, query_cbx, query_cbx_condition, query_cbx_combination, query_entry_value, table_list):
        '''Handles the press Search'''
        def clear_up():
            '''Clearing up for next search before closing search dialog'''
            query_param.clear()
            query_condition.clear()
            query_combination.clear()
            query_value.clear()

            query_cbx.clear()
            query_cbx_combination.clear()
            query_cbx_condition.clear()
            query_entry_value.clear()       
            query_dialog.destroy()

        table_list.delete(*table_list.get_children())
        dbc=DBHandler()
        '''parts of overall quere'''
        query_parts=[]
        i=0
 
        while i < len(query_param):
            '''part of query_parts[], used as temporary list for collecting elements of query'''
            inner_list=[]
            try:
                param = query_param[i].get()
                cond = query_condition[i].get()
                value = query_value[i].get()
                comb = query_combination [i].get()
                if ((param!='') and (cond!='') and (value!='')):
                   inner_list.append(value_dictionary[param])
                   inner_list.append(cond)
                   inner_list.append(value)
                   inner_list.append(comb)
                else:
                   messagebox.showerror('Empty field!', 'Fill all required fields!')
                query_parts.append(inner_list)
                i+=1
            except IndexError:
                break
            res = dbc.search_record("_data",query_parts)
            #try 2, to search string with eol 
            if not res:
                query_parts[0][2]=query_parts[0][2]+"\n"
                res = dbc.search_record("_data",query_parts)
            if len(res) > 0:
                row_index=0
                heading_list = ['','id']
                while row_index < len(res):
            
                    for heading_element in res[row_index].keys():
                        if heading_element not in heading_list:
                            heading_list.append(heading_element)
                    row_index += 1    
            else:
                messagebox.showinfo('Info', 'Requested data not found')
                #clear_up()
                return -1
            
            content_list=[]
            for j in res:
                content_list.clear()
                content_list.append(str(j.doc_id))

                #for key_value in j.keys():
                for key_value in heading_list:
                    if key_value == '' or key_value == 'id':
                        continue
                    content_list.append(j.get(key_value, ''))

                table_list.insert("",tk.END, values=content_list, open = False)
              
            l=0
            for head_title in heading_list:
                table_list.heading('#'+str(l), text=head_title)
                table_list.column('#'+str(l), width=100, stretch=False)
                if (l>=self.TABLE_WIDTH_LIMIT):
                    break
                l=l+1
         

 
        clear_up()
        return 0
    
    def edit_button(self,table_list):
        '''Handler for press Edit'''
        dbc = DBHandler()
        selected_item = table_list.selection()
        
        result = table_list.item(selected_item)['values']
        if (result == ''):
            return 0
        else:
            result2=dbc.search_record_by_id("_data", result[0])
            return result2 
        
    def update_button(self,dialog,update_list,dict_data):
        '''Updates data in db after edititing/revisioning in UI'''    
        dbc = DBHandler()
        result_dictionary = {}
        for item in update_list:
            if (list(item.values())[0] != 0):
                widget = list(item.keys())[0]
                control_var = list(item.values())[0]
            else:
                continue
            if (widget.widgetName=='ttk::entry'):
                result_dictionary.update({str(widget.cget("textvariable")):control_var.get()})
            elif (widget.widgetName=='scale'):
                result_dictionary.update({str(widget.cget("variable")):control_var.get()}) 
            elif (widget._name=='!timestamp'):
                result_dictionary.update({control_var._name:control_var.get()})
            elif (widget._name=='!tableview'):
                result_dictionary.update({control_var._name:control_var.get()})     
            elif (widget.widgetName=='checkbutton'):
                result_dictionary.update({str(widget.cget("variable")):control_var.get()})            
            elif (widget.widgetName=='listbox'):
                i=widget.curselection()
                tmp_result=[]
                for var in i:
                    tmp_result.append(widget.get(var,None))
                    result_dictionary.update({str(widget.cget("listvariable")):tmp_result})
            elif (widget.widgetName=='spinbox'):
                result_dictionary.update({str(widget.cget("textvariable")):control_var.get()})

            elif (widget.widgetName=='ttk::combobox'):
                result_dictionary.update({str(widget.cget("textvariable")):control_var.get()})
            elif (widget.widgetName=='radiobutton'):
                result_dictionary.update({str(widget.cget("variable")):control_var.get()})
            elif (widget.widgetName=='text'):
                result_dictionary.update({widget._name:widget.get("1.0", "end-1c")})
            elif (widget.widgetName=='ttk::conbobox'):
                result_dictionary.update({str(widget.cget("textvariable")):control_var.get()})
            else:
                continue
        
        dbc.upsert_record_by_id("_data",result_dictionary,dict_data.doc_id)
        dialog.destroy()

    def delete_button(self,table_list):
        '''Deletes selected record'''
        
        try:
            selected_items=table_list.selection()[0]
        except IndexError:
            messagebox.showerror('Error', 'Make s search first.')
            return 0
        dbc = DBHandler()
        record=table_list.item(selected_items)
        table_list.delete(selected_items)
        return dbc.remove_record("_data",record['values'][0])
    
    def print_button(self,doc_id):
        '''Makes a html report with opening it in a browser'''
        
        ts = time.time()
        report_path = Path("report/"+str(ts)+".html")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        dbc = DBHandler()
        value_index=dbc.search_record_by_id('_data',doc_id)
        try:
           stream = open('./yaml/print.yaml', 'r')
           res = yaml.safe_load(stream)
        except OSError:
           messagebox.showerror('Error','Something wrong with file yaml')
        if(res['type'] == 'html'):
           with report_path.open("w+", encoding="utf-8") as f:
               for block in res['content']:
                   match (block['type']):
                       case ('head'):
                           f.write("<html>\n")
                           f.write("   <head>\n")
                           f.write("      <title>"+block['data']+"</title>\n")
                           f.write ("   </head>\n")
                       case ('body'):
                           f.write("    <body>\n")
                           f.write ("      <h1> Sample report </h1>\n")
                           for sub in block['content']:
                                f.write("<h2>"+str(sub['param'])+"</h1>\n")
                                f.write(str(value_index[str(sub['data'])])+"\n")
                           f.write("    </body>\n")
                       case ('footer'):
                           f.write("    <footer>\n")
                           f.write(block['data']+"\n")
                           f.write("    </footer>\n")
                           f.write("</html>\n")     
        else:
            print ('This is not yet developed')
