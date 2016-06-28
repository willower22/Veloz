# import census2 related data  =>  need to be revised
def import_csv(file_nm,code_num_start):
        
    k=0
    with open(file_nm) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(readCSV)
        for row in readCSV:
            for j in range(1,len(row)):
                k += 1
        
    data = np.zeros((k, 4)) #initializing

    k=0
    with open(file_nm) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(readCSV)
        c1 = []
        c2 = []
        for row in readCSV:
            start_date = 2010

            for j in range(1,len(row)):
                data[k,0] = row[0]
                data[k,1] = str(int((j-1)/6)+1+code_num_start) #
                data[k,2] = start_date + (j-1)%6
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
