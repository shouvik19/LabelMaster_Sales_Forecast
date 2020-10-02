# intermodal
import numpy as np
import pandas as pd
import copy
import datetime
import matplotlib.pyplot as plt
import seaborn as sns


def read_intermodal_summary_m(file_path,file_names):
    print('Reading file. This may take time.')
    file_1=pd.read_excel(open(str(file_path)+str(file_names[0]), 'rb'),sheet_name='summary-m')
    file_1=file_1.T
    
    # change JAN-january, FEB-febuary
    file_1.loc[:,1].unique()
    month_dict= {'JAN': '01', 'FEB' :'02', 'MAR':'03', 'APR':'04', 'MAY':'05', 'JUN':'06', 'JUL':'07', 'AUG':'08', 
                 'SEP':'09', 'OCT':'10', 'NOV':'11', 'DEC':'12'}
    
    file_1.loc[:,1]=file_1.loc[:,1].map(month_dict)
    
    file_1.loc[:,0]=file_1.loc[:,0].astype(str) + "-" + file_1.iloc[:,1].astype(str)
    
    # deleting month column
    file_1=file_1.drop([1],axis=1)
    file_1.reset_index(drop=True,inplace=True)
    
    ##Merge headers with their sub-variables
    holder=np.nan
    for i in range(2,(file_1.shape[1]+1)):
        if (pd.isnull(file_1.loc[2,i])==False):
            file_1.loc[2,i]= str(holder)+str('-')+str(file_1.loc[2,i])
        elif (pd.isnull(file_1.loc[1,i])==False):
            holder = file_1.loc[1,i]
            file_1.loc[2,i] = file_1.loc[1,i]
    
    # changing column names to entry in row 2
    file_1.columns=file_1.loc[2,:]
    
    # deleting 0,1,2 rows
    file_1.drop([0,1,2],axis=0,inplace=True)
    
    # deleting empty columns
    # Find the columns where each value is null
    empty_cols =[]
    for i in range(len(file_1.columns)):
        if (file_1.iloc[:,i].isnull().all()==True):
            empty_cols.append(i)
    
    # Drop these columns from the dataframe
    file_1.drop(file_1.columns[empty_cols],axis=1,inplace=True)
    
    # rename Date column
    file_1.rename(columns={"nan-nan": "Date"}, inplace=True)
    
    # change Date's column datatype
    file_1['Date']=pd.to_datetime((file_1['Date'].astype(str)),format='%Y-%m')
    
    #-----------------------------------------------------------------------------
    # confirm the column names 
    # removing (') from column name 
    special_char='\''
    col_special=[]
    col_special_orig=[]
    
    for i in file_1.columns:
        if special_char in i:
            col_special.append(i)
            col_special_orig.append(i)
    
    for i in range(len(col_special)):
        col_special[i]=col_special[i].replace('\'','')
        
    # rename column with special char
    for i in range(len(col_special)):
        file_1.rename(columns={col_special_orig[i]: col_special[i]}, inplace=True)
    
    
    col_names=['Date', 'Intermodal Revenue Movements (IANA-ETSO)-Total',
           'Intermodal Revenue Movements (IANA-ETSO)-International',
           'Intermodal Revenue Movements (IANA-ETSO)-Domestic',
           'Intermodal Revenue Movements (IANA-ETSO)-Domestic Trailers',
           'Intermodal Revenue Movements (IANA-ETSO)-Domestic Containers',
           'Memo: Domestic Containers & 53+ Trailers',
           'S.A. Total Revenue Movements Index (Jan 2001 = 100)',
           'S.A. Total Revenue Movements Index (Jan 2001 = 100)-International Movements Index (Jan 2001 = 100)',
           'S.A. Total Revenue Movements Index (Jan 2001 = 100)-Domestic Movements Index (Jan 2001 = 100)',
           'Container Share %, Total Intermodal',
           'Container Share %, Total Intermodal-Total Domestic % (Dom. Container+Trailers)',
           'Container Share %, Total Intermodal-Truckload Only % (Dom. Container+53 Trailers)',
           'FTR Intermodal Competitive Index-Intermodal Competitive Index (0=Neutral)',
           'U.S. Origin Intermodal Volumes-International',
           'U.S. Origin Intermodal Volumes-Domestic',
           'U.S. Origin Intermodal Volumes-Total',
           'Canada Origin Intermodal Volumes-International',
           'Canada Origin Intermodal Volumes-Domestic',
           'Canada Origin Intermodal Volumes-Total',
           'Mexico Origin Intermodal Volumes-International',
           'Mexico Origin Intermodal Volumes-Domestic',
           'Mexico Origin Intermodal Volumes-Total',
           'N.A. Port Activity, Total TEUs',
           'N.A. Port Activity, Total TEUs-Imports',
           'N.A. Port Activity, Total TEUs-Exports',
           'N.A. Port Activity, Total TEUs-SA Imports',
           'West Coast Port Activity, Total TEUs',
           'West Coast Port Activity, Total TEUs-Imports',
           'West Coast Port Activity, Total TEUs-Exports',
           'West Coast Port Activity, Total TEUs-SA Imports',
           'East Coast Port Activity, Total TEUs',
           'East Coast Port Activity, Total TEUs-Imports',
           'East Coast Port Activity, Total TEUs-Exports',
           'East Coast Port Activity, Total TEUs-SA Imports',
           'Gulf Coast Port Activity, Total TEUs',
           'Gulf Coast Port Activity, Total TEUs-Imports',
           'Gulf Coast Port Activity, Total TEUs-Exports',
           'Gulf Coast Port Activity, Total TEUs-SA Imports',
           'Western Canadian Port Activity, Total TEUs',
           'Western Canadian Port Activity, Total TEUs-Imports',
           'Western Canadian Port Activity, Total TEUs-Exports',
           'Western Canadian Port Activity, Total TEUs-SA Imports']
    
    for i in range(len(col_names)):
        if (col_names[i] != file_1.columns[i]):
            print('Column name mismatch : Expected {e} but received {r}'.format(e=col_names[i],r=file_1.columns[i]))
    
    file_1.reset_index(drop=True,inplace=True)
    print('Reading Completed')
    
    return file_1
    

#file_names=['Intermodal Database.xlsx']

#file_path='/Users/amanprasad/Documents/Courses_IIT_Fall_2019/Practicum/LabelMaster/IIT-UIC_Forecasting_Project_Work/'

#df=read_intermodal_summary_m(file_path,file_names)

# exporting intermodal_summary-m into csv
#df.to_csv(r'/Users/amanprasad/Documents/Courses_IIT_Fall_2019/Practicum/LabelMaster/IIT-UIC_Forecasting_Project_Work/Exported_file_Aman/formated_intermodal_summary-m.csv', index = False)

#------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------
# rates-m

#file_names=['Intermodal Database.xlsx']

#file_path='/Users/amanprasad/Documents/Courses_IIT_Fall_2019/Practicum/LabelMaster/IIT-UIC_Forecasting_Project_Work/'

def read_intermodal_rate_m(file_path,file_names):
    print('Reading file. This may take time.')
    file_rate=pd.read_excel(open(str(file_path)+str(file_names[0]), 'rb'),sheet_name='rates-m')
    file_rate=file_rate.T

    # change JAN-january, FEB-febuary
    file_rate.loc[:,1].unique()
    month_dict= {'JAN': '01', 'FEB' :'02', 'MAR':'03', 'APR':'04', 'MAY':'05', 'JUN':'06', 'JUL':'07', 'AUG':'08', 
                 'SEP':'09', 'OCT':'10', 'NOV':'11', 'DEC':'12'}
    
    file_rate.loc[:,1]=file_rate.loc[:,1].map(month_dict)
    
    file_rate.loc[:,0]=file_rate.loc[:,0].astype(str) + "-" + file_rate.iloc[:,1].astype(str)
    
    # deleting month column
    file_rate=file_rate.drop([1],axis=1)
    file_rate.reset_index(drop=True,inplace=True)
    
    ##Merge headers with their sub-variables
    holder=np.nan
    for i in range(2,(file_rate.shape[1]+1)):
        if (pd.isnull(file_rate.loc[1,i])==False):
            file_rate.loc[1,i]= str(holder)+str('-')+str(file_rate.loc[1,i])
        elif (pd.isnull(file_rate.loc[0,i])==False):
            holder = file_rate.loc[0,i]
            file_rate.loc[1,i] = file_rate.loc[0,i]
    
    # changing column names to entry in row 1
    file_rate.columns=file_rate.loc[1,:]
    
    # deleting 0,1,2 rows
    file_rate.drop([0,1,2],axis=0,inplace=True)
    
    # deleting empty columns
    # Find the columns where each value is null
    empty_cols =[]
    for i in range(len(file_rate.columns)):
        if (file_rate.iloc[:,i].isnull().all()==True):
            empty_cols.append(i)
    
    # Drop these columns from the dataframe
    file_rate.drop(file_rate.columns[empty_cols],axis=1,inplace=True)
    
    # rename Date column
    file_rate.rename(columns={"nan-nan": "Date"}, inplace=True)
    
    # change Date's column datatype
    file_rate['Date']=pd.to_datetime((file_rate['Date'].astype(str)),format='%Y-%m')
    
    col_names=['Date',
           'Intermodal (Rail+Drayage) Rates (Rev/Load)-Total Intermodal (w/o FSC)',
           'Intermodal (Rail+Drayage) Rates (Rev/Load)-Total Intermodal (w/ FSC)']
        
    for i in range(len(col_names)):
        if (col_names[i] != file_rate.columns[i]):
            print('Column name mismatch : Expected {e} but received {r}'.format(e=col_names[i],r=file_1.columns[i]))
    
    file_rate.reset_index(drop=True,inplace=True)
    
    print('Reading Completed')
    return file_rate

#df=read_intermodal_rate_m(file_path,file_names)
    
# exporting intermodal_rate-m into csv
#df.to_csv(r'/Users/amanprasad/Documents/Courses_IIT_Fall_2019/Practicum/LabelMaster/IIT-UIC_Forecasting_Project_Work/Exported_file_Aman/formated_intermodal_rates-m.csv', index = False)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    










