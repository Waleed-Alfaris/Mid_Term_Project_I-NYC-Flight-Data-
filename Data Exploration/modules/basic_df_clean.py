import pandas as pd
flights = pd.read_csv('modules/samples/flights_sample.csv',sep=';')
import numpy as np
from sklearn.model_selection import train_test_split

flights.columns

flights.isnull().sum().sort_values(ascending=False)[:10].index

flights['cancelled'].value_counts()

y = flights['arr_delay']
X = flights[['Unnamed: 0', 'Unnamed: 0.1', 'fl_date', 'mkt_unique_carrier',
       'branded_code_share', 'mkt_carrier', 'mkt_carrier_fl_num',
       'op_unique_carrier', 'tail_num', 'op_carrier_fl_num',
       'origin_airport_id', 'origin', 'origin_city_name', 'dest_airport_id',
       'dest', 'dest_city_name', 'crs_dep_time', 'dep_time', 'dep_delay',
       'taxi_out', 'wheels_off', 'wheels_on', 'taxi_in', 'crs_arr_time',
       'arr_time', 'cancelled', 'cancellation_code', 'diverted',
       'dup', 'crs_elapsed_time', 'actual_elapsed_time', 'air_time', 'flights',
       'distance', 'carrier_delay', 'weather_delay', 'nas_delay',
       'security_delay', 'late_aircraft_delay', 'first_dep_time',
       'total_add_gtime', 'longest_add_gtime', 'no_name']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2)

##### to many missing vals, to be dropped
null = ['no_name', 'total_add_gtime', 'first_dep_time', 'longest_add_gtime',
       'cancellation_code', 'late_aircraft_delay', 'security_delay',
       'nas_delay', 'weather_delay', 'carrier_delay']

#### repeats, to be dropped
repeat_cols = ['origin_airport_id','origin_city_name', 'dest_airport_id','dest_city_name','op_carrier_fl_num',
              'mkt_unique_carrier','branded_code_share','op_unique_carrier','tail_num']

### non informative columns, from inspection, to be droped
logical_drop = ['Unnamed: 0', 'Unnamed: 0.1','wheels_off', 'wheels_on','cancelled','diverted','dup',
               'flights',
               'origin','dest','mkt_carrier_fl_num','diverted','cancelled'
]

###### info that can't be known in real time, so we'll aggregate
col_to_agg = ['dep_time','arr_time','actual_elapsed_time', 'crs_dep_time','taxi_out','taxi_in',
             'air_time']


####### dropping all bad columns
X_train.drop(labels=null, axis=1, inplace=True)
X_train.drop(labels=repeat_cols, axis=1, inplace=True)
X_train.drop(labels=logical_drop, axis=1, inplace=True)


X_test.drop(labels=null, axis=1, inplace=True)
X_test.drop(labels=repeat_cols, axis=1, inplace=True)
X_test.drop(labels=logical_drop, axis=1, inplace=True)


for col in X_train.columns:
    if X_train[col].isnull().sum() > 70000:
        X_train.drop(labels=col, axis=1, inplace=True)
        
for col in X_train.columns:
    if X_train[col].isnull().sum() < 70000:
        if X_train[col].dtype == 'float64':
            X_train[col].fillna(X_train[col].mean(), inplace=True)
        else:
            X_train[col].fillna(X_train[col].mode(), inplace=True)        


###### filling na vals for cols with not so many
for col in X_test.columns:
    if X_test[col].isnull().sum() > 70000:
        X_test.drop(labels=col, axis=1, inplace=True)
        
for col in X_test.columns:
    if X_test[col].isnull().sum() < 70000:
        if X_test[col].dtype == 'float64':
            X_test[col].fillna(X_test[col].mean(), inplace=True)
        else:
            X_test[col].fillna(X_test[col].mode(), inplace=True)     

            
            
##### converting date strings to dateitme, isolate for month, and turn into int
X_train.loc[:,'fl_date']= pd.to_datetime(X_train['fl_date']).dt.strftime('%m').astype('int64')

X_test.loc[:,'fl_date']= pd.to_datetime(X_test['fl_date']).dt.strftime('%m').astype('int64')



# get dummies for airlines
X_train = pd.get_dummies(X_train)

X_test = pd.get_dummies(X_test)


###### remember the col_to_agg?, here we take their mean for every month
for col in col_to_agg:
    for i in range(1,13):
        X_train.loc[X_train['fl_date']==i, col]= X_train.groupby(by='fl_date').mean()[col][i]

for col in col_to_agg:
    for i in range(1,13):
        X_test.loc[X_test['fl_date']==i, col]= X_test.groupby(by='fl_date').mean()[col][i]

        
###### Fill na values for y values with mean
y_train = y_train.fillna(y_train.mean())

y_test = y_test.fillna(y_test.mean())