import numpy as np
import pandas as pd
import copy
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

import intermodal_format
import truck_trailer_format



file_path='/Users/amanprasad/Documents/Courses_IIT_Fall_2019/Practicum/LabelMaster/IIT-UIC_Forecasting_Project_Work/'

file_names=['Intermodal Database.xlsx']
formated_intermodal_summary=intermodal_format.read_intermodal_summary_m(file_path,file_names)
formated_intermodal_rates=intermodal_format.read_intermodal_rate_m(file_path,file_names)

file_names=['Truck & Trailer Database.xlsx']
formated_truck_trailer_indicators=truck_trailer_format.read_truck_trailer_indicators_m(file_path,file_names)
formated_truck_trailer_economics=truck_trailer_format.read_truck_trailer_economics_m(file_path,file_names)
formated_truck_trailer_freight=truck_trailer_format.read_truck_trailer_freight_m(file_path,file_names)

# merge
external_merged = pd.merge(formated_intermodal_summary, formated_intermodal_rates, how='outer', on='Date')

external_merged = pd.merge(external_merged, formated_truck_trailer_indicators, how='outer', on='Date')

external_merged = pd.merge(external_merged, formated_truck_trailer_economics, how='outer', on='Date')

external_merged = pd.merge(external_merged, formated_truck_trailer_freight, how='outer', on='Date')


# exporting external_merged into csv
external_merged.to_csv(r'/Users/amanprasad/Documents/Courses_IIT_Fall_2019/Practicum/LabelMaster/IIT-UIC_Forecasting_Project_Work/Exported_file_Aman/external_merged.csv', index = False)














