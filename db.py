from tkinter import dialog
from tkinter import messagebox
import random
import tinydb
from tinydb import TinyDB, Query
import tinydb.table

class DBHandler:

   DB_PATH='db.json' 
   def guess_value(self,value):
         '''Aux function to define the type of data has been entered: String, Float or Integer'''
         #bool value excluded
         if isinstance(value,bool) or (('-' in str(value)) and (':' in str(value))):
            return value
         digits=0
         points=0
         char=0
         try:
            while char < len(value):
               
               if value[char].isdigit() == True:
                  digits+=1
               elif value[char] == '.' or value[char] == ',':
                  value=value.replace(',','.')
                  points+=1
               else:
                  return str(value)
               char+=1
            if points <=1 and points > 0:
               return float(value)
            elif digits>0:
               return int(value)
            else:
               return str(value)
            
         except (TypeError, ValueError):
            messagebox.showerror('Error data conversion','Check your data in the Search form')

   def add_record(self,db_table,db_data):
      '''Inserting info from {{db_data}} into db - add record to {{db_connection}}/{{db_table}}'''
      path_db=self.DB_PATH
      db_connection=TinyDB(path_db)
      for value1 in db_data:
         tmp_value=self.guess_value(str(db_data[value1]))
         db_data[value1]=tmp_value
      try:
         tbl=db_connection.table(db_table)
         result=tbl.insert(db_data)
         db_connection.close()
      except ValueError:
         messagebox.showinfo('Info','Error data writing. Try one more time.')
         return -1
      return result
   
   def search_record(self,db_table,db_data):
      '''Looking up {{db_data}} in {{db_table}} through {{db_connection}} to db'''
   
      path_db=self.DB_PATH
      db_connection=TinyDB(path_db)
      table=db_connection.table(db_table)

      base_query=Query()
      start_query=Query().noop()
      i=0
      try:
         while i < len(db_data)/4:
            if (db_data[i][3]=='AND') or (db_data[i][3]==''):
                if db_data[i][1] == '<':
                   start_query=start_query & (base_query[db_data[i][0]]<self.guess_value(db_data[i][2]))
                elif db_data[i][1] == '=':
                   start_query=start_query & (base_query[db_data[i][0]] == self.guess_value((db_data[i][2])))
                elif db_data[i][1] == '!=':
                   start_query=start_query & ~(base_query[db_data[i][0]]==self.guess_value(db_data[i][2]))
                elif db_data[i][1] == '>':
                   start_query=start_query & (base_query[db_data[i][0]]>self.guess_value(db_data[i][2])) 
                else:
                   messagebox.showerror('Error','Wrong sign in field 1')
            elif db_data[i][3] == 'OR':
                if db_data[i][1] == '<':
                    start_query=start_query | (base_query[db_data[i][0]]<self.guess_value(db_data[i][2]))
                elif db_data[i][1] == '=':
                    start_query=start_query | (base_query[db_data[i][0]]==self.guess_value(db_data[i][2]))
                elif db_data[i][1] == '!=':
                    start_query=start_query | ~(base_query[db_data[i][0]]==self.guess_value(db_data[i][2]))
                elif db_data[i][1] == '>':
                    start_query=start_query | (base_query[db_data[i][0]]>self.guess_value(db_data[i][2]))
                else:
                   messagebox.showerror('Error','Wrong sign in field 1')
            i+=1
         result_set2=table.search(start_query)
         
      except ValueError:
          messagebox.showinfo('Info','Error data writing. Try one more time.')
          return {-1:-1}
      
      return result_set2
   def search_record_by_id(self, db_table, db_data):
      '''Searching record by doc_id field '''
      path_db=self.DB_PATH
      db_connection=TinyDB(path_db)
      table=db_connection.table(db_table)
      result_set2=table.get(doc_id=db_data)
      return result_set2

   def upsert_record_by_id(self, db_table, db_data, doc_id):
      '''Function to update record (update button)'''
      path_db=self.DB_PATH
      db_connection=TinyDB(path_db)
      table=db_connection.table(db_table)
      result_set2=table.upsert(tinydb.table.Document((db_data), doc_id))
      return result_set2

   def remove_record(self, db_table, doc_id):
      '''Removing data by user's request'''
      path_db=self.DB_PATH
      db_connection=TinyDB(path_db)
      table=db_connection.table(db_table)
      table.remove(doc_ids=[doc_id])