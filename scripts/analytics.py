# import modules
from .sql_kit import SQL_Kit

# libraries
import mysql.connector
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import getpass

# this pulls data from the SQL database, then displays a dashboard of interactive plots, widgets and animations!

class Dashboard:
    
    def __init__(self, userID=None, password=None, database='easytranspose'):
        
        # if no credentials are  passed, prompt user
        if userID==None and password==None:
            # MySQL info
            self.userID = input('User ID: ')
            self.password = getpass.getpass('Password: ')
            self.database = database
        
        # credentials passed
        else:
            # MySQL info
            self.userID = userID
            self.password = password
            self.database = database
            
        
    """ SELECT * FROM table """
    def select_table(self, table):
        
        s = SQL_Kit(self.userID, self.password, self.database)
        data = s.select_table(table)
        
        return data
    
    
    def display(self):
        
        # import data from MySQL table
        df = self.select_table('transpose')
        data = df['StartPosition'].value_counts()
        
        # set matplotlib style
        plt.style.use('dark_background')
        
        """ Daily Transpositions by Hour """

        all_date_times = df['EventDateTime']

        all_days = []
        all_hours = []
        for item in all_date_times:
            all_days.append((item.timetuple().tm_yday))
            all_hours.append(item.hour)

        x = all_days
        y = all_hours
        x_labels = pd.Series(all_days).unique()
        
        fig1, ax1 = plt.subplots()
        ax1.set_title('Daily Transpositions by Hour')
        ax1.scatter(x,y,color='mediumspringgreen',linewidths=1)
        ax1.set_xlabel('day of year')
        ax1.set_ylabel('hour')
        ax1.xaxis.grid(True)
        
        if len(x_labels) > 5:
            ax1.xaxis.set_ticks([min(all_days), max(all_days)])
        else:
            ax1.xaxis.set_ticks(x_labels)
        
        ax1.yaxis.grid(False) 
        plt.show()
        
        
        """ MOVING AVERAGE """

        def day_of_year(datetime_entry):
            return datetime_entry.timetuple().tm_yday

        df['day_of_year'] = list(df.apply(lambda x: day_of_year(x['EventDateTime']),axis=1))
        daily_count = df['day_of_year'].value_counts().sort_index()

        averages = []
        i=1
        for dab_count in daily_count:
            values = daily_count[:i]
            average = round(sum(values)/len(values),2)
            averages.append(average)
            i+=1

        day_list = list(df['day_of_year'].unique())

        avg_move_df = pd.DataFrame([day_list,averages]).T
        avg_move_df.rename(columns={0: 'day_id', 1: 'moving_avg'},inplace=True)
        avg_move_df.set_index('day_id',inplace=True)
        
        fig1, ax1 = plt.subplots()
        ax1.plot(avg_move_df.index.astype(int),avg_move_df['moving_avg'], color='mediumspringgreen')
        ax1.set_title('Moving AVG')
        ax1.set_xlabel('day_of_year')
        ax1.xaxis.set_ticks([min(all_days), max(all_days)])
        ax1.set_ylabel('avg transpositions per day')
        plt.show()
        
        """ Total Transpositions per day """

        dates = []
        for item in list(df['EventDateTime']):
            day = item.day
            month = item.month
            year = item.year

            date_st = str(month)+'/'+str(day)+'/'+str(year)
            dates.append(date_st) 

        data = pd.DataFrame(pd.Series(dates).value_counts()).sort_index()

        dates = list(data.index)
        counts = list(data[0])

        objects = dates
        y_pos = np.arange(len(objects))

        # get class info from class_absence_stats dataframe
        performance = counts
        #fig3 = plt.figure(3) 
        plt.bar(y_pos, performance, color='mediumspringgreen', align='center', alpha=0.8)
        plt.xticks(y_pos, objects)
        plt.title('Total Transpositions per Day')
        plt.ylabel('Total Transpositions ')
        plt.xlabel('Day')

        plt.show()
        
        
        """ Top 3 Instruments """

        objects = df['Instrument'].value_counts().index[:3]
        y_pos = np.arange(len(objects))

        # get class info from class_absence_stats dataframe
        performance = list(df['Instrument'].value_counts())[:3]
        #fig3 = plt.figure(3) 
        plt.bar(y_pos, performance, color='mediumspringgreen', align='center', alpha=0.8)
        plt.xticks(y_pos, objects)
        plt.title('Top 3 Instruments')
        plt.ylabel('Total Usage')
        plt.xlabel('Instrument')

        plt.show()
        
        
        """ Top 5 Start Notes """

        objects = df['StartNote'].value_counts().index[:5]
        y_pos = np.arange(len(objects))

        # get class info from class_absence_stats dataframe
        performance = list(df['StartNote'].value_counts())[:5]
        #fig3 = plt.figure(3) 
        plt.bar(y_pos, performance, color='mediumspringgreen',align='center', alpha=0.8)
        plt.xticks(y_pos, objects)
        plt.title('Top 5 Start Notes')
        plt.ylabel('Total Usage')
        plt.xlabel('Note Label')

        plt.show()

             
        """ Start Position Breakdown """

        objects = self.select_table('transpose')['StartPosition'].value_counts().index[:5]
        y_pos = np.arange(len(objects))

        # get class info from class_absence_stats dataframe
        performance = list(df['StartPosition'].value_counts())[:5]
        #fig3 = plt.figure(3) 
        plt.bar(y_pos, performance, color='mediumspringgreen', align='center', alpha=0.8)
        plt.xticks(y_pos, objects)
        plt.title('Start Position')
        plt.ylabel('Total Usage')
        plt.xlabel('Start Position')

        plt.show()