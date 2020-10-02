# merge sales and external factors
import numpy as np
import pandas as pd
import copy
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

merged_external=pd.read_csv('/Users/amanprasad/Documents/Courses_IIT_Fall_2019/Practicum/LabelMaster/IIT-UIC_Forecasting_Project_Work/Exported_file_Aman/external_merged.csv')

merged_sales=pd.read_csv('/Users/amanprasad/Documents/Courses_IIT_Fall_2019/Practicum/LabelMaster/IIT-UIC_Forecasting_Project_Work/Exported_file_Aman/formated_combined_monthly_sales.csv')

# merge sales and external factors
merged_sales_external = pd.merge(merged_sales, merged_external, how='outer', on='Date')

merged_sales_external.sort_values(by='Date',ascending=True,inplace=True)
merged_sales_external.reset_index(drop=True,inplace=True)
# export merged_sales_external
merged_sales_external.to_csv(r'/Users/amanprasad/Documents/Courses_IIT_Fall_2019/Practicum/LabelMaster/IIT-UIC_Forecasting_Project_Work/Exported_file_Aman/merged_sales_external.csv', index = False)















