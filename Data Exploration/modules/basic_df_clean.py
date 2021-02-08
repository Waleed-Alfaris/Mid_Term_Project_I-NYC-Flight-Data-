import pandas as pd
flights = pd.read_csv('modules/samples/flights_sample.csv',sep=';')
import numpy as np
from sklearn.model_selection import train_test_split


# check available columns
flights.columns

# Seperate into X,y and train test split 
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

# check shape
X_train.shape

y_train.shape

# columns to note...
# repeats, will drop
repeat_cols = ['origin_airport_id','origin_city_name', 'dest_airport_id','dest_city_name','op_carrier_fl_num',
              'mkt_unique_carrier','branded_code_share','op_unique_carrier','tail_num']


logical_drop = ['Unnamed: 0', 'Unnamed: 0.1','weather_delay','wheels_off', 'wheels_on','cancelled','diverted','dup',
               'flights',
               'origin','dest','mkt_carrier_fl_num','diverted','cancelled'
]

col_to_agg = ['dep_time','arr_time','actual_elapsed_time', 'crs_dep_time','taxi_out','taxi_in','carrier_delay','nas_delay','security_delay',
             'late_aircraft_delay','air_time']



# remove columns with to many nans, fillna for columns with some byt not to many
for col in X_train.columns:
    if X_train[col].isnull().sum() > 70000:
        X_train.drop(labels=col, axis=1, inplace=True)
        
for col in X_train.columns:
    if X_train[col].isnull().sum() < 70000:
        if X_train[col].dtype == 'float64':
            X_train[col].fillna(X_train[col].mean(), inplace=True)
        else:
            X_train[col].fillna(X_train[col].mode(), inplace=True)   
            

# Drop columns for repeat or logical reasons
X_train.drop(labels=repeat_cols, axis=1, inplace=True)
X_train.drop(labels=logical_drop, axis=1, inplace=True)

# group dates by month, turn into int
X_train['fl_date']= pd.to_datetime(X_train['fl_date']).dt.strftime('%m').astype('int64')


# get dummies for airline
X_train = pd.get_dummies(X_train)


# aggregating the agg columns
for col in col_to_agg:
    for i in range(1,13):
        X_train.loc[X_train['fl_date']==i, col]= X_train.groupby(by='fl_date').mean()[col][i]







##### run into error when trying to fit linreg form sklearn "Input contains NaN, infinity or a value too large for dtype('float64')."
from sklearn.linear_model import LinearRegression

reg = LinearRegression()


y = reg.fit(X_train, y_train)