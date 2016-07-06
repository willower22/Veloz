from pandas import DataFrame, read_csv
import pandas as pd
import csv
import numpy as np
import statsmodels.formula.api as sm
from scipy import stats
from sklearn import linear_model
import datetime
from dateutil.relativedelta import relativedelta
import calendar

def add_months(sourcedate,months):
     month = sourcedate.month - 1 + months
     year = int(sourcedate.year + month / 12 )
     month = month % 12 + 1
     day = min(sourcedate.day,calendar.monthrange(year,month)[1])
     return datetime.date(year,month,day)
     
## add data into an original dataset
def add_data(data, data_2):
    n_row1 = len(data[:,0])
    n_row2 = len(data_2[:,0])
    n_col = len(data[0,:])
    
    new_data = np.zeros((n_row1+n_row2, n_col)) #initializing
    new_data[0:n_row1,:] = data[:,:]
    new_data[n_row1:,:] = data_2[:,:]              

    return new_data

# import census2 related data
def import_csv(file_nm,code_num_start):
        
    k=0
    with open(file_nm) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(readCSV)
        for row in readCSV:
            for j in range(1,len(row)):
                k += 1
        
    data = np.zeros((k, 4)) #initializing

    df = pd.read_csv(file_nm)
    df_col_arr = df.columns[1:]

    date_arr = np.zeros(len(df_col_arr)) #initializing

    for i in range(0,len(date_arr)):
        if('2010' in df_col_arr[i]):
            date_arr[i] = 2010
        elif('2011' in df_col_arr[i]):
            date_arr[i] = 2011
        elif('2012' in df_col_arr[i]):
            date_arr[i] = 2012
        elif('2013' in df_col_arr[i]):
            date_arr[i] = 2013
        elif('2014' in df_col_arr[i]):
            date_arr[i] = 2014            
        elif('2015' in df_col_arr[i]):
            date_arr[i] = 2015

    k=0
    with open(file_nm) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(readCSV)
        c1 = []
        c2 = []
        for row in readCSV:

            for j in range(1,len(row)):
                data[k,0] = row[0]
                data[k,1] = str(int((j-1)/6)+1+code_num_start) #
                data[k,2] = date_arr[j-1]               
                if(row[j]=='N/A' or row[j]==''):
                    data[k,3] = 0
                else:                
                    data[k,3] = row[j]

                k += 1
    return data

## change column names
def chg_column_names(df,num_keys):
    col_arr = df.columns
    num_col = len(col_arr)
    k=1
    
    for i in range(num_keys,num_col):
        col_b = col_arr[i]
        col_a = 'x' + str(k)      
        df = df.rename(columns={col_b:col_a})
        k += 1

    return df

def pivot_2(data,col):
    uniq = np.unique(data[:,col])
    df = pd.DataFrame(data = data, columns=['zipcode', 'code', 'year', 'value'])

    df_m = df[df['code'] == uniq[0]]
    for i in uniq[1:]:
        df_temp = df[df['code'] == i]
        df_m = pd.merge(df_m, df_temp, left_on=['zipcode','year'], right_on=['zipcode','year'])

    df_m = df_m.drop(['code_x','code_y','code'], axis=1)

    col_names = ['zipcode', 'year']
    for i in range(0,len(uniq)):
        col = 'x' + str(i+1)
        col_names.append(col)

    df_m.columns = col_names
    return df_m

## regression function for all factors
def regression_all(df,y_col,num_keys):
    col_arr = df.columns
    num_col = len(col_arr)
    col_all = col_arr[num_keys]
    for i in range(num_keys,num_col-1):
        col_all += '+' + col_arr[i+1]

    formula = col_arr[y_col] + '~' + col_all
    result = sm.ols(formula = formula, data=df).fit()

    return result

def regression_ex(df,y_col,num_keys,excluding_cols):
    col_arr = df.columns
    num_col = len(col_arr)
    col_all = ''
    for i in range(num_keys,num_col-1):
        if(col_arr[i+1] not in excluding_cols):
            if(i == num_keys):
                col_all = col_arr[num_keys]

            col_all += '+' + col_arr[i+1]

    formula = col_arr[y_col] + '~' + col_all
    result = sm.ols(formula = formula, data=df).fit()

    return result

# get 588 factor names from 37 csv files
def get_factor_names(code_df,file_nm,num_year):

    df = pd.read_csv(file_nm)
    df_col_arr = df.columns[1:]
    date_arr = np.zeros(len(df_col_arr)) #initializing
    temp_list = []
    code_list = []

    next_code = code_df['column_cd'].max() +1
    if(pd.isnull(code_df['column_cd'].max())):
        next_code = 1

    for i in range(0,int(len(date_arr)/6)):

        col_name = df_col_arr[int(i*num_year)][:-6]
        temp_list.append(col_name)
        code_list.append(int(i+next_code))

    temp_df = pd.DataFrame(data = temp_list, columns=['column_nm'])
    temp_df = temp_df.assign(column_cd = code_list)
    code_df = code_df.append(temp_df, ignore_index=True)

    return code_df

# import median house value per square data
def read_price_per_sq(file_nm):
    k=0    
    with open(file_nm) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',', quotechar='|')   
        next(readCSV)
        for row in readCSV:
            for j in range(1,len(row)):
                k += 1
        
    value2 = np.zeros((k, 4)) #initializing
    
    k=0
    with open(file_nm) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(readCSV)    
        c1 = []
        c2 = []
        for row in readCSV:
            start_date = datetime.datetime.strptime('Apr 1 1996  1:33PM', '%b %d %Y %I:%M%p')
    
            for j in range(1,len(row)):
                value2[k,0] = row[0]
                value2[k,1] = start_date.year
                value2[k,2] = start_date.month            
                value2[k,3] = int(row[j] or 0)
                k += 1
                start_date = add_months(start_date,1)
    value2_year = value2[value2[:,2]==12,:]
    value2_year = np.append(value2_year,np.zeros([len(value2_year),1]),1)
    # delete month column
    value2_year = value2_year[:,[0,1,3]]
    return value2_year
    
    
    
    
    
    
    
    
    
    
    
    