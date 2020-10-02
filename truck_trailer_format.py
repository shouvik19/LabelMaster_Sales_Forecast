# freight-m
import numpy as np
import pandas as pd
import copy
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

def read_truck_trailer_freight_m(file_path,file_names):
    print('Reading file. This may take some time.')
    file_1=pd.read_excel(open(str(file_path)+str(file_names[0]), 'rb'),sheet_name='freight-m')
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
    file_1=file_1.dropna(how='all',axis=1)
    
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
    
    
    col_names=['Date', 'FTR Truck Loadings (000s, SA)',
           'FTR Truck Loadings Index (1992=100)',
           'FTR Truck Loadings Index (1992=100)-M/M % Change',
           'FTR Truck Loadings Index (1992=100)-Y/Y % Change',
           'FTR Rail Intermodal Loadings (000, SA)',
           'FTR Rail Intermodal Loadings Index (1992=100)',
           'FTR Rail Intermodal Loadings Index (1992=100)-M/M % Change',
           'FTR Rail Intermodal Loadings Index (1992=100)-Y/Y % Change',
           'FTR Rail Carloadings (carload + intermodal) (000s, SA)',
           'FTR Rail Carloadings Index (1992=100)',
           'FTR Rail Carloadings Index (1992=100)-M/M % Change',
           'FTR Rail Carloadings Index (1992=100)-Y/Y % Change',
           'FTR Cl. 8 Truck Tonnage (000s, SA)',
           'FTR Cl. 8 Truck Tonnage Index (1992=100)',
           'FTR Cl. 8 Truck Tonnage Index (1992=100)-M/M % Change',
           'FTR Cl. 8 Truck Tonnage Index (1992=100)-Y/Y % Change',
           'FTR Cl. 8 Truck Tonmiles (000000s, SA)',
           'FTR Cl. 8 Truck Tonmiles Index (1992=100)',
           'FTR Cl. 8 Truck Tonmiles Index (1992=100)-M/M % Change',
           'FTR Cl. 8 Truck Tonmiles Index (1992=100)-Y/Y % Change',
           'FTR Class 8 Truck Utilization (%, SA)',
           'Dry Van Trailer Loadings (000s, SA)',
           'Reefer Trailer Loadings (000s, SA)',
           'Platform Trailer Loadings (000s, SA)',
           'Straight Truck Loadings (000s, SA)',
           'Bulk Trailer Loadings (000s, SA)',
           'Food & Kindred Products (000s, SA)',
           'Stone, Clay, Glass & Concrete (000s, SA)',
           'Nonmetallic Minerals, Except Fuels (000s, SA)',
           'Chemicals & Allied Products (000s, SA)',
           'Transportation Equipment (000s, SA)', 'All Other Freight (000s, SA)',
           'FTR MD Truck Tonnage (000s, SA)',
           'FTR MD Truck Tonnage Index (1992=100)',
           'FTR MD Truck Tonnage Index (1992=100)-M/M % Change',
           'FTR MD Truck Tonnage Index (1992=100)-Y/Y % Change',
           'FTR MD Truck Tonmiles (000000s, SA)',
           'FTR MD Truck Tonmiles Index (1992=100)',
           'FTR MD Truck Tonmiles Index (1992=100)-M/M % Change',
           'FTR MD Truck Tonmiles Index (1992=100)-Y/Y % Change']
    
    for i in range(len(col_names)):
        if (col_names[i] != file_1.columns[i]):
            print('Column name mismatch : Expected {e} but received {r}'.format(e=col_names[i],r=file_1.columns[i]))
    
    file_1.reset_index(drop=True,inplace=True)
    print('Reading Completed')
    return file_1


#file_names=['Truck & Trailer Database.xlsx']

#file_path='/Users/amanprasad/Documents/Courses_IIT_Fall_2019/Practicum/LabelMaster/IIT-UIC_Forecasting_Project_Work/'

#df=read_truck_trailer_freight_m(file_path,file_names)

# exporting truck_trailer_freight-m into csv
#df.to_csv(r'/Users/amanprasad/Documents/Courses_IIT_Fall_2019/Practicum/LabelMaster/IIT-UIC_Forecasting_Project_Work/Exported_file_Aman/formated_truck_trailer_freight-m.csv', index = False)


#------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------
# economics-m

def read_truck_trailer_economics_m(file_path,file_names):
    print('Reading file. This may take some time.')
    file_1=pd.read_excel(open(str(file_path)+str(file_names[0]), 'rb'),sheet_name='economics-m')
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
    
    
    # changing column names to entry in row 2
    file_1.columns=file_1.loc[2,:]
    
    # deleting 0,1,2 rows
    file_1.drop([0,1,2],axis=0,inplace=True)
    
    # deleting empty columns
    file_1=file_1.dropna(how='all',axis=1)
    
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
    
    
    col_names=['Date', 'Total IP Index', 'Durable Manufacturing Index',
           'Non-Durable Manufacturing Index', 'Total Manufacturing Index',
           'Food Index', 'Chemicals Index', 'Fabricated Metal Product Index',
           'Automobile and Light-Duty Vehicles Index', 'Payroll Employment (000s)',
           'ISM Manufacturing Index', 'West Coast Port Container Activity (TEUs)',
           'Cass Freight Shipments Index (1992=100)',
           'Construction Employment (000s)', 'Manufacturing Employment (000s)',
           'Retail Trade Employment (000s)',
           'Total Transp. and Warehouse Emp. (000s)',
           'Truck Transportation Employment (000s)',
           'Other Transportation Employment (000s)', 'Unemployment Rate (%)',
           'Leading Economic Indicators (%)', 'Interest Rate Spread (%)',
           'Total Bus. Inventories/Retail Sales Ratio',
           'Business Inventories (Mil $)', 'Durable Goods Orders (Mil $)',
           'Nondefense Capital Goods Orders (Mil $)',
           'Chicago Fed National Activity Index 3MMA', 'S&P 500',
           'Total Construction Spending (Mil $)',
           'Public Construction Spending (Mil $)',
           'Private Residential Construction (Mil $)',
           'Private Non-Residential Construction (Mil $)', 'Housing Starts (000s)',
           'Retail Sales (Mil $)', 'Consumer Price Index',
           'Consumer Confidence (Conference Board)', 'Building Permits (000s)',
           'New Home Sales (000s)', 'Existing Home Sales (000s)',
           'National Avg. Diesel/Gal.',
           'Distillate Fuel Inventories (Mil Barrels/Day)',
           'W. Texas Int. Crude Oil ($Bbl.)', 'Truck-General Freight, TL',
           'Truck-General Freight, LTL', 'Rail-Line Haul, Carload',
           'Rail- Line Haul, Intermodal']
    
    for i in range(len(col_names)):
        if (col_names[i] != file_1.columns[i]):
            print('Column name mismatch : Expected {e} but received {r}'.format(e=col_names[i],r=file_1.columns[i]))
    
    file_1.reset_index(drop=True,inplace=True)
    print('Reading Completed')
    return file_1

#file_names=['Truck & Trailer Database.xlsx']
#file_path='/Users/amanprasad/Documents/Courses_IIT_Fall_2019/Practicum/LabelMaster/IIT-UIC_Forecasting_Project_Work/'

#df= read_truck_trailer_economics_m(file_path,file_names)

# exporting truck_trailer_economics-m into csv
#df.to_csv(r'/Users/amanprasad/Documents/Courses_IIT_Fall_2019/Practicum/LabelMaster/IIT-UIC_Forecasting_Project_Work/Exported_file_Aman/formated_truck_trailer_economics-m.csv', index = False)


#------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------
# indicators-m

def read_truck_trailer_indicators_m(file_path,file_names):
    print('Reading file. This may take some time.')
    file_1=pd.read_excel(open(str(file_path)+str(file_names[0]), 'rb'),sheet_name='indicators-m')
    file_1=file_1.T
    
    # considering columns upto 80
    file_1=file_1.iloc[:,0:80]
    
    # change JAN-january, FEB-febuary
    file_1.loc[:,1].unique()
    month_dict= {'JAN': '01', 'FEB' :'02', 'MAR':'03', 'APR':'04', 'MAY':'05', 'JUN':'06', 'JUL':'07', 'AUG':'08', 
                 'SEP':'09', 'OCT':'10', 'NOV':'11', 'DEC':'12'}
    
    file_1.loc[:,1]=file_1.loc[:,1].map(month_dict)
    
    file_1.loc[:,0]=file_1.loc[:,0].astype(str) + "-" + file_1.iloc[:,1].astype(str)
    
    # deleting month column
    file_1=file_1.drop([1],axis=1)
    file_1.reset_index(drop=True,inplace=True)
    
    
    holder1=np.nan
    holder2=np.nan
    
    for i in range(2,(file_1.iloc[2,:][file_1.iloc[2,:]=='Class 4, North America'].index[0])):
        if (pd.isnull(file_1.loc[2,i])==False):
            if (pd.isnull(file_1.loc[2,i-1])):
                holder2=file_1.loc[2,i]
                file_1.loc[2,i]= str(holder1)+str('-')+str(file_1.loc[2,i])
            else:
                file_1.loc[2,i]=str(holder1) + str('-') + str(holder2) + str(' ') + str(file_1.loc[2,i])
        elif (pd.isnull(file_1.loc[1,i])==False):
            holder1 = file_1.loc[1,i]
    
    
    for i in range((file_1.iloc[2,:][file_1.iloc[2,:]=='Class 4, North America'].index[0]),file_1.shape[1]):
        if (pd.isnull(file_1.loc[2,i-1])):
            if (pd.isnull(file_1.loc[2,i+1])==False):
                holder1=file_1.loc[2,i]
        if (pd.isnull(file_1.loc[2,i])==False):
            file_1.loc[2,i]= str(holder1)+str('-')+str(file_1.loc[2,i])
        

    # changing column names to entry in row 2
    file_1.columns=file_1.loc[2,:]
    
    # deleting 0,1,2 rows
    file_1.drop([0,1,2],axis=0,inplace=True)
    
    # deleting empty columns
    file_1=file_1.dropna(how='all',axis=1)
    
    # rename Date column
    file_1.rename(columns={"nan-nan": "Date"}, inplace=True)
    
    # change Date's column datatype
    file_1['Date']=pd.to_datetime((file_1['Date'].astype(str)),format='%Y-%m')
    
    # sort by date and reset index then
    file_1.sort_values(by='Date', ascending=True,inplace=True)
    file_1.reset_index(drop=True,inplace=True)
    
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
    
    
    col_names=['Date', 'Total Class 8, North America-OEM Net Orders',
           'Total Class 8, North America-OEM Net Orders M/M % Change',
           'Total Class 8, North America-OEM Net Orders Y/Y % Change',
           'Total Class 8, North America-Factory Shipments (Wards)',
           'Total Class 8, North America-Factory Shipments (Wards) M/M % Change',
           'Total Class 8, North America-Factory Shipments (Wards) Y/Y % Change',
           'Total Class 8, North America-Retail Sales (Wards)',
           'Total Class 8, North America-Retail Sales (Wards) M/M % Change',
           'Total Class 8, North America-Retail Sales (Wards) Y/Y % Change',
           'Total Class 8, North America-Inventories (Wards)',
           'Total Class 8, North America-Inventories (Wards) M/M % Change',
           'Total Class 8, North America-Inventories (Wards) Y/Y % Change',
           'Total Trailers, U.S.-Production',
           'Total Trailers, U.S.-Production M/M % Change',
           'Total Trailers, U.S.-Production Y/Y % Change',
           'Total Classes 4-7, North America-Factory Shipments (Wards)',
           'Total Classes 4-7, North America-Factory Shipments (Wards) M/M % Change',
           'Total Classes 4-7, North America-Factory Shipments (Wards) Y/Y % Change',
           'Total Classes 4-7, North America-Retail Sales (Wards)',
           'Total Classes 4-7, North America-Retail Sales (Wards) M/M % Change',
           'Total Classes 4-7, North America-Retail Sales (Wards) Y/Y % Change',
           'Total Classes 4-7, North America-Inventories (Wards)',
           'Total Classes 4-7, North America-Inventories (Wards) M/M % Change',
           'Total Classes 4-7, North America-Inventories (Wards) Y/Y % Change',
           'Class 4, North America-Factory Shipments (Wards)',
           'Class 4, North America-Retail Sales (Wards)',
           'Class 4, North America-Inventories (Wards)',
           'Class 6-7 Bus, North America-Factory Shipments (Wards)',
           'Class 4-7, US-Retail Sales (Wards)']
    
    for i in range(len(col_names)):
        if (col_names[i] != file_1.columns[i]):
            print('Column name mismatch : Expected {e} but received {r}'.format(e=col_names[i],r=file_1.columns[i]))
        
    file_1.reset_index(drop=True,inplace=True)
    
    print('Reading Complate')
    return file_1
    
    
#df=read_truck_trailer_indicators_m(file_path,file_names)

# exporting truck_trailer_indicators-m into csv
#df.to_csv(r'/Users/amanprasad/Documents/Courses_IIT_Fall_2019/Practicum/LabelMaster/IIT-UIC_Forecasting_Project_Work/Exported_file_Aman/formated_truck_trailer_indicators-m.csv', index = False)
    
















