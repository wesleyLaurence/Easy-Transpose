import mysql.connector
from datetime import datetime
import pandas as pd

class SQL_Kit(object):
    
    """ This kit enables access to MySQL database """
    
    def __init__(self, userID=None, password=None, database=None):
        
        # parameters
        self.userID = userID
        self.password = password
        self.database = database
        self.host = "localhost"
        self.port = 3306
        
        
    # get data from SQL table
    def select_table(self, table): 

        # connect to database
        try: 
            mydb = mysql.connector.connect(
            host = self.host,
            port = self.port,
            user = self.userID,
            passwd = self.password,
            database = self.database
            )
        except:
            print("Could not connect to database")

        try: 
            # SQL SELECT TABLE
            mycursor = mydb.cursor()
            mycursor.execute("""SELECT * FROM `%s`""" % (table))
            myresult = mycursor.fetchall()
            mycursor.close()

            # get column names
            mycursor = mydb.cursor()
            #mycursor.execute("SHOW columns FROM %s;", (table) )
            mycursor.execute("""SHOW columns FROM `%s`""" % (table))
            column_names = list(pd.DataFrame(mycursor.fetchall())[0])
            
            # close db and cursor
            mycursor.close()
            mydb.close()

        except Error as e:
            mycursor.close()
            mydb.close()
            print(e)
        
        # convert data into pandas dataframe
        df = pd.DataFrame(myresult,columns=column_names)
        df.set_index(column_names[0],inplace=True)

        return df
    
    
    # INSERT row in MySQL table
    def insert_row(self, sql, val):   
        """ 
        Required Parameters
        sql: a string of the SQL code you want executed.
        
        val: a tuple of all values being loaded into SQL table
        """   
        
        # connect to database
        try: 
            mydb = mysql.connector.connect(
            host = self.host,
            port = self.port,
            user = self.userID,
            passwd = self.password,
            database = self.database
            )
        except:
            print("Could not connect to database")
        
        try: 
            mycursor = mydb.cursor()
            mycursor.execute(sql, val)
            mydb.commit()
            mycursor.close()
            mydb.close()

        except Error as e:
            mycursor.close()
            mydb.close()
            print(e)
             
                
    def transpose_table(self, start_note, transpose_note, start_position, instrument):         
            sql = "INSERT INTO transpose (StartNote, TransposeNote, StartPosition, Instrument, EventDateTime) VALUES (%s, %s, %s, %s, %s)" 
            val = (start_note, transpose_note, start_position, instrument, datetime.now())     
            self.insert_row(sql,val)