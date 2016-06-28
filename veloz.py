from pandas import DataFrame, read_csv
import pandas as pd
import csv
import numpy as np

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

def pivot_2(data,col):
    uniq = np.unique(data[:,col])
    df = pd.DataFrame(data = data, columns=['zipcode', 'code', 'year', 'value'])

    df_m = df[df['code'] == 1]
    for i in uniq[1:]:
        df_temp = df[df['code'] == i]
        
        df_m = pd.merge(df_m, df_temp, left_on=['zipcode','year'], right_on=['zipcode','year'])

    df_m = df_m.drop(['code_x', 'code_y'], axis=1)
    
    return df_m


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

## import from Data1.csv to Data10.csv files

file_nm = 'C:/Users/Y/UCLA/Internship/Veloz/code/kyle/Data' + str(1) + '.csv'
k_data = import_csv(file_nm,0)

for i in range(2,10):
    file_nm = 'C:/Users/Y/UCLA/Internship/Veloz/code/kyle/Data' + str(i) + '.csv'
    next_code_num = max(k_data[:,1])
    k_data_1 = import_csv(file_nm,next_code_num)
    k_data = add_data(k_data, k_data_1)    
