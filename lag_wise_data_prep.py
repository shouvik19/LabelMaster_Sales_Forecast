# feature selection for 503

import pandas as pd
import numpy as np
%matplotlib inline
import matplotlib.pyplot as plt
import copy
import seaborn as sns

from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

from sklearn.feature_selection import RFE
from sklearn.ensemble import RandomForestRegressor
from matplotlib import pyplot

from dateutil.relativedelta import relativedelta
from datetime import datetime

merged_sales_external=pd.read_csv('/Users/amanprasad/Documents/Courses_IIT_Fall_2019/Practicum/LabelMaster/IIT-UIC_Forecasting_Project_Work/Exported_file_Aman/merged_sales_external.csv')



#-------------------------------------------------------
# df_503_external with lag = 0

def merged_503_sales_external(merged_sales_external,external_shift_down):

    formated_combined_monthly_sales_columns= ['Date', '503', '504', '505', '506', '507', '510', '511', '512', '508',
           '516', '517', '514', '520']
    df_503_external = copy.deepcopy(merged_sales_external)
    df_503_external['Date'] = pd.to_datetime(df_503_external['Date'], format='%Y-%m-%d')
    
    df_503_external.drop(formated_combined_monthly_sales_columns[2:],axis=1,inplace=True)
    
    df_503_external.sort_values(by='Date', ascending=True,inplace=True)
    df_503_external.reset_index(drop=True,inplace=True)
    
    df_503_external.index=df_503_external['Date']
    df_503_external.drop('Date',axis=1,inplace=True)
    
    #------------------------------------
    #------------------------------------
    
    # increase date by month += external_shift_down
    last_date_503 = np.max(df_503_external[df_503_external['503'].notnull()].index)
    last_date_keep= last_date_503 + relativedelta(months=external_shift_down)
    
    df_503_external = df_503_external[(df_503_external.index >='2000-01-01') & (df_503_external.index <= last_date_keep)]
    #--------------------------------------
    #------------------------------------
    
    # deleting columns with more than 30 null values
    df_503_external_less_30_null=df_503_external.loc[:, df_503_external.isnull().sum() < 30]
    
    
    #----------------
    # separating 503 
    df_503_train=copy.deepcopy(df_503_external_less_30_null['503'])
    df_not_503_train=copy.deepcopy(df_503_external_less_30_null.iloc[:,1:])
    
    # shift by lag s = external_shift_down
    s=external_shift_down
    df_not_503_train = df_not_503_train.shift(s, axis = 0)
    
    #-----------------------------------
    # impute missing values for train
    # train
    print('imputing missing values. This may take time.')
    imp_mean = IterativeImputer(random_state=0)
    imp_mean.fit(df_not_503_train)
    IterativeImputer(random_state=0)
    
    df_not_503_train_imputed=pd.DataFrame(imp_mean.transform(df_not_503_train), index=df_not_503_train.index,
                                          columns=df_not_503_train.columns)
    
    print('imputation completed.')
    
    #-----------------------------
    # feature selection
    print('feature selection in-progress. This may take time.')
    # perform feature selection
    
    rfe = RFE(RandomForestRegressor(n_estimators=500, random_state=1), n_features_to_select=100)
    
    
    if s == 0:
        fit = rfe.fit(df_not_503_train_imputed.iloc[:,:], df_503_train.iloc[:])
    else:
        fit = rfe.fit(df_not_503_train_imputed.iloc[:-external_shift_down,:], df_503_train.iloc[:-external_shift_down])
    
    #fit = rfe.fit(df_not_503_train_imputed.iloc[:-external_shift_down,:], df_503_train.iloc[:-external_shift_down])
    
    # report selected features
    Selected_Features=[]
    names = df_not_503_train_imputed.columns
    for i in range(len(fit.support_)):
        if fit.support_[i]:
            Selected_Features.append(names[i])
    
    
    print('feature selection completed')
    
    # keeping features which are in Selected_Features
    df_not_503_train_imputed_feat=copy.deepcopy(df_not_503_train_imputed[Selected_Features])
    
    
    # adding 503
    df_not_503_train_imputed_feat['503'] = df_503_train
    
    # removing Date from index and putting it into a clumn
    df_not_503_train_imputed_feat.reset_index(drop=False,inplace=True)
    
    print('merged_503_sales_external dataframe ready with external variables down-shift = {ss}'.format(ss = s))
    
    return df_not_503_train_imputed_feat


#-----------------------------------------------------------------
df_lag_0 = merged_503_sales_external(merged_sales_external, external_shift_down = 0)

# export df_not_503_train_imputed_feat to csv
df_lag_0.to_csv(r'/Users/amanprasad/Documents/Courses_IIT_Fall_2019/Practicum/LabelMaster/IIT-UIC_Forecasting_Project_Work/Exported_file_Aman/df_503_imputed_feat_lag_0.csv', index = False)


#--------------------------------------------------------------------------------------
# df_503_external with lag = 1

df_lag_1 = merged_503_sales_external(merged_sales_external, external_shift_down = 1)

# export df_lag_1 to csv
df_lag_1.to_csv(r'/Users/amanprasad/Documents/Courses_IIT_Fall_2019/Practicum/LabelMaster/IIT-UIC_Forecasting_Project_Work/Exported_file_Aman/df_503_imputed_feat_lag_1.csv', index = False)


#--------------------------------------------------------------------------------------
# df_503_external with lag = 2

df_lag_2 = merged_503_sales_external(merged_sales_external, external_shift_down = 2)

# export df_lag_1 to csv
df_lag_2.to_csv(r'/Users/amanprasad/Documents/Courses_IIT_Fall_2019/Practicum/LabelMaster/IIT-UIC_Forecasting_Project_Work/Exported_file_Aman/df_503_imputed_feat_lag_2.csv', index = False)



#--------------------------------------------------------------------------------------
# df_503_external with lag = 3

df_lag_3 = merged_503_sales_external(merged_sales_external, external_shift_down = 3)

# export df_lag_1 to csv
df_lag_3.to_csv(r'/Users/amanprasad/Documents/Courses_IIT_Fall_2019/Practicum/LabelMaster/IIT-UIC_Forecasting_Project_Work/Exported_file_Aman/df_503_imputed_feat_lag_3.csv', index = False)






