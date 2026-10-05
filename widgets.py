import ast
import json
import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path
from tkinter import messagebox
from datetime import datetime
from tksheet import Sheet
from tkinter import dialog, filedialog
from tkinter import ttk
import sys,os,shutil

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

       self.btn_add = ttk.Button(parwn, text="+", width=3, command = lambda: self._add_button(self.tv))
       self.btn_add.place(x=pos_x+155,y=pos_y+height+5)
       self.btn_del = ttk.Button(parwn, text="-", width=3, command = lambda: self._del_button(self.tv))
       self.btn_del.place(x=pos_x+50,y=pos_y+height+5)
       self.param = ttk.Entry(parwn,width=12,textvariable=self.param_var)
       self.param.place(x=pos_x+195,y=pos_y+height+5)

       
       self.trace_id=self.textvariable.trace_add("write", lambda *args: self._update_widget(self.tv,self.textvariable.get()))
       self.bind("<Destroy>", self.cleanup)
       self._update_widget(self.tv,self.textvariable.get())

    def _add_button(self,tv_widget):
       '''Handler for + button'''
       if self.param_var.get() == '':
           messagebox.showerror('Error', "Add parameter to include to TimeSeries")
           return
       tv_widget.insert("",index="end",values=[str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),self.param_var.get()])
       self.param_var.set('')
       self._update_data(tv_widget)

    def _del_button(self,tv_widget):
        '''Handler for - button'''
        row_index_list=self.tv.get_children()
        tv_widget.delete(row_index_list[-1])
        self._update_data(tv_widget)

    def _update_data(self,tv_widget):
        '''for control var update'''
        if not self.tv.winfo_exists():
            return
        self._updating = True

        
        row_index_list=tv_widget.get_children()
        result_data=[]
        for row_index in row_index_list:
            row_values =tv_widget.item(row_index, "values")
            result_data.append(list(row_values))
 
        self.textvariable.set(str(result_data))
        self._updating = False

        return result_data

    def _update_widget(self,tv_widget,table_data):
        '''for widget update'''
        if self._updating:
            return
        for row_id in tv_widget.get_children():
            tv_widget.delete(row_id)
       
        for row in ast.literal_eval(table_data):
            tv_widget.insert("",index="end",values=row)

    def cleanup(self, ev):
        if ev.widget == self:
            self.textvariable.trace_remove("write",self.trace_id)

class ImageGallery(tk.Frame):
    
    def __init__(self,parwn,parameter,width,height,pos_x,pos_y,textvariable, **kwargs):
       '''Image Gallery constructor'''
       tk.Frame.__init__(self,parwn)
       self._updating = False
       self.file_path = ""
       self.textvariable = textvariable
       self.paths = ast.literal_eval("".join(self.textvariable.get()))
       '''index for image'''
       self.index=0
       self.canv=tk.Canvas()
       self.anno=tk.StringVar()
       param_width=width
       param_height=height
       '''target path to copy image'''
       self.result_path=Path.cwd() / "images" / parameter
       lbf = ttk.LabelFrame(parwn, text=parameter, width=100,height=70)
       lbf.place(x=pos_x,y=pos_y)
       bb = ttk.Button(parwn,text=" >>>> ", command= lambda:self.showGal(param_width,param_height))
       bb.place(x=pos_x+17, y=pos_y+17)
       self.textvariable.trace_add("write", lambda *args: self._update_widget(self.textvariable.get()))
    def showGal(self,width,height):
       '''Image gallery renderer'''
       self.anno=tk.StringVar()
       self.wid=tk.Toplevel()
       
       self.wid.title("ImageGallery - ")
       # get image's dimensions to adjust the Toplevel dialog
       self.wid.geometry(str(width)+"x"+str(height))
       self.canv=tk.Canvas(self.wid,width=width-190,height=height-100,bg='gray')
       self.canv.place(x=50,y=0)
       vs_canvas_image= ttk.Scrollbar(self.canv, orient = 'vertical', command=self.canv.yview)
       hs_canvas_image= ttk.Scrollbar(self.canv, orient = 'horizontal', command=self.canv.xview)
       vs_canvas_image.place(x=width-202, y=0, height=height-98)
       hs_canvas_image.place(x=0, y=height-112, width=width-202)
       self.canv.configure(yscrollcommand=vs_canvas_image.set, xscrollcommand=hs_canvas_image.set)
       self.prev = ttk.Button(self.wid, text='<', width=2, command=self.on_button_prev)
       self.next = ttk.Button(self.wid, text='>', width=2, command = self.on_button_next)
       self.prev.place(x=10,y=height/2-100)
       self.next.place(x=width-120,y=height/2-100)
       self.browse = ttk.Button(self.wid,text='...',width=10, command=lambda: self.on_button_browse())
       self.browse.place(x=600,y=height-95)
       self.store = ttk.Button(self.wid,text='Save gallery',width=16, command=lambda: self.on_button_save())
       self.store.place(x=800,y=height-95)
       self.anno_label=ttk.Label(self.wid,text="Legend:")
       self.anno_label.place(x=75,y=height-90)
       self.anno_text = ttk.Entry(self.wid,width=50,textvariable=self.anno)
       self.anno_text.place(x=130,y=height-90)
       img_dir = os.scandir(self.result_path)
       try:
           self.showImage(self.result_path / self.paths[self.index][1],25,25)
       except IndexError:
           pass
      
    def showImage(self,path,pos_x,pos_y):
        '''Draws the image in IG widget'''
        if path != '':
           self.img = ImageTk.PhotoImage(Image.open(path))
           self.canv.create_image(pos_x,pos_y,anchor=tk.NW, image=self.img)
           self.anno.set(self.paths[self.index][0])
        else:
           # just leave this canvas blank
           pass

    def on_button_prev(self):
        if self.index != 0:
            self.index -=1
            self.showImage(self.result_path / self.paths[self.index][1],25,25)
            self.anno.set(self.paths[self.index][0])
            
    def on_button_next(self):
        if self.index < len(self.paths)-1:
            self.index +=1
            self.showImage(self.result_path / self.paths[self.index][1],25,25)
            self.anno.set(self.paths[self.index][0])

    def on_button_browse(self):
        self.file_path = filedialog.askopenfilename(
           title="Выберите файл",
           filetypes=[("Изображения JPEG/GIF/PNG/BMP", "*.jpg *.jpeg *.png *.bmp"), ("Все файлы", "*.*")]
        )

    def on_button_save(self):
        '''Handler for 'Save gallery' button '''
        self._updating = True
        if self.file_path != '':
                self.paths.append(list([self.anno_text.get(),Path(self.file_path).name]))
                shutil.copy(self.file_path,self.result_path)
                self.showImage(self.result_path / self.paths[self.index][1],25,25)
        else:
            for sub in self.paths:
                tmp_path = self.result_path / sub[1]
                #if tmp_path.is_file(): 
                self.paths[self.index][0]=self.anno_text.get()
                
        self.textvariable.set(json.dumps(self.paths).replace('\\', '').replace('"', "'"))
        self._updating = False

    def _update_widget(self,text_variable):
        '''for widget update'''
        if self._updating:
            return
        self.index = 0
        self.paths = ast.literal_eval("".join(text_variable))
