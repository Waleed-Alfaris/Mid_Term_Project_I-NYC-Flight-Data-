def clean(df):

    # Importing modules
    import pandas as pd
    import numpy as np
    from sklearn.model_selection import train_test_split
    import math
    
    
    # A little data epxloration...
    df.columns

    df.isnull().sum().sort_values(ascending=False)[:10].index

    # identify x and y vals for regression...
    y = df['arr_delay']
    X = df[['Unnamed: 0', 'Unnamed: 0.1', 'fl_date', 'mkt_unique_carrier',
       'branded_code_share', 'mkt_carrier', 'mkt_carrier_fl_num',
       'op_unique_carrier', 'tail_num', 'op_carrier_fl_num',
       'origin_airport_id', 'origin', 'origin_city_name', 'dest_airport_id',
       'dest', 'dest_city_name', 'crs_dep_time', 'dep_time', 'dep_delay',
       'taxi_out', 'wheels_off', 'wheels_on', 'taxi_in', 'crs_arr_time',
       'arr_time', 'cancelled', 'cancellation_code', 'diverted',
       'dup', 'crs_elapsed_time', 'actual_elapsed_time', 'air_time', 'flights',
       'distance', 'carrier_delay', 'weather_delay', 'nas_delay',
       'security_delay', 'late_aircraft_delay', 'first_dep_time',
       'total_add_gtime', 'longest_add_gtime', 'no_name','arr_delay']]

    
    # split the data befor eany changes...
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2)

    
    # convert all dates into integers for the month
    X_train.loc[:,'fl_date']= pd.to_datetime(X_train['fl_date']).dt.strftime('%m').astype('int64')
    X_test.loc[:,'fl_date']= pd.to_datetime(X_test['fl_date']).dt.strftime('%m').astype('int64')
    
    
    
    # Identify important columns
    col_to_agg = ['air_time','actual_elapsed_time','taxi_in','taxi_out','wheels_on',
             'arr_time','wheels_off','taxi_out','dep_delay','dep_time']

    # to many nulls, will drop
    null = ['no_name', 'total_add_gtime', 'first_dep_time', 'longest_add_gtime',
       'cancellation_code']

    # repetitive cols, will drop
    repeat_cols = ['origin_airport_id','origin_city_name', 'dest_airport_id','dest_city_name','op_carrier_fl_num',
              'mkt_unique_carrier','branded_code_share','op_unique_carrier','tail_num']

    # other cols to drop bc, no info 
    logical_drop = ['Unnamed: 0', 'Unnamed: 0.1','wheels_off', 'wheels_on','cancelled','diverted','dup',
               'flights',
               'origin','dest','mkt_carrier_fl_num','diverted','cancelled','dep_delay',
               'carrier_delay', 'weather_delay', 'nas_delay', 'security_delay', 'late_aircraft_delay']
    
    
    
    # replacing na values in columns from col_to_agg, with their median with respect to month
    for col in col_to_agg:
        for i in range(1,13):
            X_train.loc[X_train['fl_date']==i, col] = X_train.loc[X_train['fl_date']==i, col].fillna(X_train.loc[X_train['fl_date']==i][col].median())
            
            
    for col in col_to_agg:
        for i in range(1,13):
            X_test.loc[X_test['fl_date']==i, col] = X_test.loc[X_test['fl_date']==i, col].fillna(X_test.loc[X_test['fl_date']==i][col].median())
            
            
            
    # replacing arr_delay values with their median with respect to month
    for i in range(1,13):
        X_train.loc[X_train['fl_date']==i, 'arr_delay'] = X_train.loc[X_train['fl_date']==i, 'arr_delay'].median()
        
    for i in range(1,13):
        X_test.loc[X_test['fl_date']==i, 'arr_delay'] = X_test.loc[X_test['fl_date']==i, 'arr_delay'].median()
            
    
    # drop labels designated to be droped...
    X_train.drop(labels=null, axis=1, inplace=True)
    X_train.drop(labels=repeat_cols, axis=1, inplace=True)
    X_train.drop(labels=logical_drop, axis=1, inplace=True)
     
    X_test.drop(labels=null, axis=1, inplace=True)
    X_test.drop(labels=repeat_cols, axis=1, inplace=True)
    X_test.drop(labels=logical_drop, axis=1, inplace=True)

    
    
    # get dummy vars for mkt carrier
    X_train = pd.get_dummies(X_train)

    X_test = pd.get_dummies(X_test)
    
    
    
    #fill na vals of y, with their respective medians
    y_train = y_train.fillna(y_train.median())
 
    y_test = y_test.fillna(y_test.median())
    
    
    
    
    
    
    return X_train, X_test, y_train, y_test