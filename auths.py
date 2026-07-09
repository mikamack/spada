from tkinter import dialog
import yaml

import tinydb
import os.path
import hashlib
import uuid
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tinydb import TinyDB, Query

class UIAuth:

   def auth_user(self,user,passwd):
      '''Authenticates or registers a user with passwd in the DB.
         Gives a user id or -1 if login failed '''
      path_db='db.json'
      user_id=''
      if not os.path.exists(path_db):
         conn_db=TinyDB(path_db)    
         tbl=conn_db.table('_users')
         tmp=passwd.encode('utf-8')
         hash_pwd=hashlib.sha512(tmp)
         tbl.insert({'login': user, 'hash_passwd': hash_pwd.hexdigest() })
         messagebox.showinfo('Info','You have been registered')
         user_id = uuid.uuid1()
         conn_db.close()

      else:
         conn_db=TinyDB(path_db)
         tbl=conn_db.table('_users')
         query = Query()
         tmp=passwd.encode('utf-8')
         hash_value=hashlib.sha512(tmp)
         res=tbl.search((query.login == user) & (query.hash_passwd == hash_value.hexdigest()))
         if len(res) > 0:
            user_id = uuid.uuid1()
         else:
            user_id = -1
         conn_db.close()
      return user_id
