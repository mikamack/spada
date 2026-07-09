import tkinter as tk
from tkinter import dialog
from tkinter import ttk
import sys,os
sys.path.append(os.getcwd())
import linters
import renders
from tkinter import messagebox
def main():
   if getattr(sys, 'frozen', False):
      os.environ['YAMLLINT_CONFIG_DIR'] = os.path.join(sys._MEIPASS, 'yamllint', 'conf')
   ui = renders.UIRender()
   #Check the yamls's syntax
   yl=linters.YamlLinter()
   res_l=yl.lint_files()
   res_s=yl.analyze_syntax()
   if (res_l>0 or res_s>0):
      messagebox.showerror('Error', 'Fix yamls!')
      exit()
   path_db='db.json'
   # Makes all windows objects
   root = tk.Tk()
   root.withdraw()
   
   if not os.path.exists(path_db):
      ui.register_ui("Register, please")
   else:
      ui.login_ui("Log in, please")
   root.mainloop()
if __name__ == "__main__":
   main()