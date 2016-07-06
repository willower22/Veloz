# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 17:19:10 2016

@author: Y
"""
from common import *
    
# create a table which includes data with all 588 factors
def create_all_factor_table():
    workdr = 'C:/Users/Y/UCLA/Internship/Veloz/code/kyle/'
    file_nm = workdr + 'Data' + str(1) + '.csv'
    k_data = import_csv(file_nm,0)

    for i in range(2,38): #
        file_nm = workdr + 'Data' + str(i) + '.csv'
        next_code_num = max(k_data[:,1])
        k_data_1 = import_csv(file_nm,next_code_num)
        k_data = add_data(k_data, k_data_1)    

    k_data_df = pd.DataFrame(data=k_data,columns=['zipcode','code','year','value'])

    all_df = pivot_2(k_data_df.as_matrix(),1)

    file_nm = workdr + 'Zip_MedianValuePerSqft_AllHomes.csv'
    value2_year = read_price_per_sq(file_nm)
    value2_year_df = pd.DataFrame(data = value2_year, columns=['zipcode', 'year', 'Median Price Per Sqr Ft.'])

    k_data_m = value2_year_df.merge(all_df, on=['zipcode','year']) #

    code_df = pd.DataFrame(columns=['column_nm','column_cd'])
     
    for i in range(1,38):
        file_nm = workdr + 'Data' + str(i) + '.csv'
        code_df = get_factor_names(code_df,file_nm,6)
    
    col_names = ['zipcode', 'year', 'Median Price Per Sqr Ft.']
    for i in range(0,588):
        col_names.append(code_df.column_nm[i])        
    k_data_m.columns = col_names
    
    file_nm = workdr + "all_factor_data.csv"
    k_data_m.to_csv(file_nm, index=False)

# execute create_all_factor_table()
create_all_factor_table()