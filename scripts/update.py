""" load music-code program data into MySQL database """

import mysql.connector
from datetime import datetime

class DatabaseUpdate(object):
    
    def __init__(self, userID='wesley', password='2433zap', database="easytranspose"):
        
        self.userID = userID
        self.password = password
        self.database = database
        
    def update_db(self, sql, val):   
        """ update_db  

        Required Parameters
        sql: a string of the SQL code you want executed.
        
        val: a tuple of all values being loaded into SQL table
     
        """   
      
        try: 
            #
            mydb=mysql.connector.connect(
            host="localhost",
            port=3306,
            user=self.userID,
            passwd=self.password,
            database=self.database
            )

            mycursor = mydb.cursor()
            mycursor.execute(sql, val)
            mydb.commit()
            mycursor.close()
            mydb.close()

        except Error as e:
            mycursor.close()
            mydb.close()
            print(e)
            
            
    # MusiCode class updates
    
    def transpose_table(self, start_note, transpose_note, start_position, instrument):         
            sql = "INSERT INTO transpose (StartNote, TransposeNote, StartPosition, Instrument, EventDateTime) VALUES (%s, %s, %s, %s, %s)" 
            val = (start_note, transpose_note, start_position, instrument, datetime.now())     
            self.update_db(sql,val)
