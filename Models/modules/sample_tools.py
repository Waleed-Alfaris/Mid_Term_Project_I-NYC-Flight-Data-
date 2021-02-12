def clean_and_split_model_train(df):
    '''For model training only. This function will accept a full flights dataset, with fl_date, crs_arr_time, and crs_dep_time in datetime format.
    Function will return two datasets, X and y. X will have the same columns as flights_test, y is the target column.
    
    Parameters:
    df: input dataframe with time columns in dt format.
    
    Returns:
    X: datatset with matching columns of flights_test.
    y: target vector of same number of rows as X.
    '''
    
    
    import numpy as np, pandas as pd
    flights = df.copy(deep=True)
    
    test_cols = pd.read_csv('../Datasets/flights_test.txt', sep=';', low_memory=False).columns.values
    flights_stripped = flights.loc[:, test_cols] #select only columns that appear in flights_test
    flights_stripped['arr_delay'] = flights['arr_delay'] #join target column for dropping of rows in unison
    flights_stripped.dropna(axis=0, inplace=True) #arr_delay only column with NaNs. As this is the target variable, will drop rows
    
    flights_X = flights_stripped.drop(columns='arr_delay')
    flights_y = flights_stripped.loc[:, 'arr_delay']
    
    return flights_X, flights_y
    
    


def append_hourly_indecies(df, med_tod_delay_df):
    import pandas as pd, numpy as np
    
    flights = df.copy(deep=True).reset_index(drop=True)
    med_delays = med_tod_delay_df.copy(deep=True).reset_index(drop=True)
#     mode_delays = mode_tod_delay_df.copy(deep=True).reset_index(drop=True)
    
    med_delay_list, mode_delay_list = [], []
    for i in range(len(flights)):
        match_found = False
        
        if i in np.arange(1000, len(flights), 1000):
            print(f'Current iteration: {i} of {len(flights)} total...') #status update every 5000 iteration
            

        for j in range(len(med_delays)):
            if all([flights['crs_dep_time'][i].hour == med_delays['Scheduled Departure (Hour)'][j],
                    flights['crs_arr_time'][i].hour == med_delays['Scheduled Arrival (Hour)'][j],
                    flights['origin'][i] == med_delays['Departing Airport'][j],
                   ]):
                
                match_found = True
                med_delay_list.append(med_delays['Hourly Arrival Delay (Median)'][j])
#                 mode_delay_list.append(mode_delays['Hourly Arrival Delay (Mode)'][j])
                break
            
            
        if match_found == False:
            print(f'No match found for flights row {i}. Filling with 0')
            med_delay_list.append(0)
#             mode_delay_list.append(0)
            
    flights['Median TOD Delay IDX'] = med_delay_list
#     flights['Mode TOD Delay IDX'] = mode_delay_list
    
    print('Complete. Dataframe returned with columns appended.')
    return flights 






def append_monthly_indecies(df, med_toy_delay_df):
    import pandas as pd, numpy as np
    
    flights = df.copy(deep=True).reset_index(drop=True)
    med_delays = med_toy_delay_df.copy(deep=True).reset_index(drop=True)
#     mode_delays = mode_toy_delay_df.copy(deep=True).reset_index(drop=True)
    
    med_delay_list, mode_delay_list = [], []
    for i in range(len(flights)):
        match_found = False
        
        if i in np.arange(2500, len(flights), 2500):
            print(f'Current iteration: {i} of {len(flights)} total...') #status update every 5000 iteration

        for j in range(len(med_delays)):
            if all([flights['fl_date'][i].month == med_delays['Month'][j],
                    flights['origin'][i] == med_delays['Departing Airport'][j],
                   ]):
                
                match_found = True
                med_delay_list.append(med_delays['Monthly Arrival Delay (Median)'][j])
#                 mode_delay_list.append(mode_delays['Monthly Arrival Delay (Mode)'][j])
                break
                
        if match_found == False:
            print(f'No match found for flights row {i}. Filling with 0')
            med_delay_list.append(0)
#             mode_delay_list.append(0)
            
    flights['Median TOY Delay IDX'] = med_delay_list
#     flights['Mode TOY Delay IDX'] = mode_delay_list
    
    print('Complete. Dataframe returned with columns appended.')
    return flights





def append_taxi_indecies(df, med_tod_taxi_df, mode_tod_taxi_df):
    import pandas as pd, numpy as np
    
    flights = df.copy(deep=True).reset_index(drop=True)
    med_delays = med_tod_taxi_df.copy(deep=True).reset_index(drop=True)
    mode_delays = mode_tod_taxi_df.copy(deep=True).reset_index(drop=True)
    
    med_delay_list_in, med_delay_list_out, mode_delay_list_in, mode_delay_list_out = [], [], [], []
    for i in range(len(flights)):
        match_found = False
        
        if i in np.arange(2500, len(flights), 2500):
            print(f'Current iteration: {i} of {len(flights)} total...') #status update every 5000 iteration

        for j in range(len(med_delays)):
            if all([flights['crs_dep_time'][i].hour == med_delays['Scheduled Departure (Hour)'][j],
                    flights['crs_arr_time'][i].hour == med_delays['Scheduled Arrival (Hour)'][j],
                   ]):
                
                match_found = True
                med_delay_list_in.append(med_delays['Hourly Taxi-In Duration (Median)'][j])
                med_delay_list_out.append(med_delays['Hourly Taxi-Out Duration (Median)'][j])
                mode_delay_list_in.append(mode_delays['Hourly Taxi-In Duration (Mode)'][j])
                mode_delay_list_out.append(mode_delays['Hourly Taxi-Out Duration (Mode)'][j])
                break
                
        if match_found == False:
            print(f'No match found for flights row {i}. Filling with 0')
            med_delay_list_in.append(0)
            med_delay_list_out.append(0)
            mode_delay_list_in.append(0)
            mode_delay_list_out.append(0)
            
            
            
    flights['Mode TOD Taxi-In IDX'] = mode_delay_list_in
    flights['Mode TOD Taxi-Out IDX'] = mode_delay_list_out
    flights['Median TOD Taxi-In IDX'] = med_delay_list_in
    flights['Median TOD Taxi-Out IDX'] = med_delay_list_out
    
    print('Complete. Dataframe returned with columns appended.')
    return flights



def append_traffic_index(df, tod_traffic_df):
    import pandas as pd, numpy as np
    
    flights = df.copy(deep=True).reset_index(drop=True)
    delays = tod_traffic_df.copy(deep=True).reset_index(drop=True)
    
    
    delay_list_arr, delay_list_dep = [], []
    for i in range(len(flights)):
        dep_match_found, arr_match_found = False, False
        
        if i in np.arange(2500, len(flights), 2500):
            print(f'Current iteration: {i} of {len(flights)} total...') #status update every 5000 iteration

        for j in range(len(delays)):
            if all([flights['crs_dep_time'][i].hour == delays['Hour'][j],
                    flights['origin'][i] == delays['Airport'][j],
                   ]):
                
                dep_match_found = True
                delay_list_dep.append(delays['Flights'][j])

                
            if all([flights['crs_arr_time'][i].hour == delays['Hour'][j],
                    flights['dest'][i] == delays['Airport'][j],
                   ]):
                
                arr_match_found = True
                delay_list_arr.append(delays['Flights'][j])    
                
                
                
        if dep_match_found == False:
            print(f'No match found for dep flights row {i}. Filling with 0')
            delay_list_dep.append(0)
            
        if arr_match_found == False:
            print(f'No match found for arr flights row {i}. Filling with 0')
            delay_list_arr.append(0)

                      
    flights['TOD Dep Traffic IDX'] = delay_list_dep
    flights['TOD Arr Traffic IDX'] = delay_list_arr
    
    print('Complete. Dataframe returned with columns appended.')
    return flights























    
# def append_median_tod_delay(df, tod_delay_df):
#     '''WARNING! For large datasets, this function takes a long time to run.
    
#     Function that accepts flights and tod_delay_idx tables. Returns df with appended row for time of day delay index
    
#     Parameters:
#     df: dataset with features matching flights_test features
#     tod_delay_df: time of day delay index table
    
#     Returns:
#     df: input df with tod delay index column appended
#     '''
    
    
#     import pandas as pd, numpy as np
    
#     flights = df.copy(deep=True).reset_index(drop=True)
#     delays = tod_delay_df.copy(deep=True).reset_index(drop=True)
    
    
#     delay_list = []
#     for i in range(len(flights)):
#         match_found = False

#         for j in range(len(delays)):
#             if all([flights['crs_dep_time'][i].hour == delays['Scheduled Departure (Hour)'][j],
#                     flights['crs_arr_time'][i].hour == delays['Scheduled Arrival (Hour)'][j],
#                     flights['mkt_unique_carrier'][i] == delays['Airline'][j],
#                     flights['origin'][i] == delays['Departing Airport'][j],
#                     flights['dest'][i] == delays['Arriving Airport'][j]
#                    ]):
                
#                 match_found = True
#                 delay_list.append(delays['Hourly Arrival Delay(Median)'][j])
#                 break
                
#         if match_found == False:
#             print(f'No match found for flights row {i}. Filling with NaN')
#             delay_list.append(np.nan)
            
#     flights['Median TOD Delay IDX'] = delay_list
#     return flights    
    
    

# def append_mode_tod_delay(df, tod_delay_df):
#     import pandas as pd, numpy as np
    
#     flights = df.copy(deep=True).reset_index(drop=True)
#     delays = tod_delay_df.copy(deep=True).reset_index(drop=True)
    
    
#     delay_list = []
#     for i in range(len(flights)):
#         match_found = False

#         for j in range(len(delays)):
#             if all([flights['crs_dep_time'][i].hour == delays['Scheduled Departure (Hour)'][j],
#                     flights['crs_arr_time'][i].hour == delays['Scheduled Arrival (Hour)'][j],
#                     flights['mkt_unique_carrier'][i] == delays['Airline'][j],
#                     flights['origin'][i] == delays['Departing Airport'][j],
#                     flights['dest'][i] == delays['Arriving Airport'][j]
#                    ]):
                
#                 match_found = True
#                 delay_list.append(delays['Hourly Arrival Delay(Mode)'][j])
#                 break
                
#         if match_found == False:
#             print(f'No match found for flights row {i}. Filling with NaN')
#             delay_list.append(np.nan)
            
#     flights['Mode TOD Delay IDX'] = delay_list
#     return flights




# def append_median_toy_delay(df, toy_delay_df):
#     import pandas as pd, numpy as np
    
#     flights = df.copy(deep=True).reset_index(drop=True)
#     delays = toy_delay_df.copy(deep=True).reset_index(drop=True)
    
    
#     delay_list = []
#     for i in range(len(flights)):
#         match_found = False

#         for j in range(len(delays)):
#             if all([flights['fl_date'][i].month == delays['Month'][j],
#                     flights['mkt_unique_carrier'][i] == delays['Airline'][j],
#                     flights['origin'][i] == delays['Departing Airport'][j],
#                     flights['dest'][i] == delays['Arriving Airport'][j]
#                    ]):
                
#                 match_found = True
#                 delay_list.append(delays['Monthly Arrival Delay(Median)'][j])
#                 break
                
#         if match_found == False:
#             print(f'No match found for flights row {i}. Filling with NaN')
#             delay_list.append(np.nan)
            
#     flights['Median TOY Delay IDX'] = delay_list
#     return flights




# def append_mode_toy_delay(df, toy_delay_df):
#     import pandas as pd, numpy as np
    
#     flights = df.copy(deep=True).reset_index(drop=True)
#     delays = toy_delay_df.copy(deep=True).reset_index(drop=True)
    
    
#     delay_list = []
#     for i in range(len(flights)):
#         match_found = False

#         for j in range(len(delays)):
#             if all([flights['fl_date'][i].month == delays['Month'][j],
#                     flights['mkt_unique_carrier'][i] == delays['Airline'][j],
#                     flights['origin'][i] == delays['Departing Airport'][j],
#                     flights['dest'][i] == delays['Arriving Airport'][j]
#                    ]):
                
#                 match_found = True
#                 delay_list.append(delays['Monthly Arrival Delay(Mode)'][j])
#                 break
                
#         if match_found == False:
#             print(f'No match found for flights row {i}. Filling with NaN')
#             delay_list.append(np.nan)
            
#     flights['Mode TOY Delay IDX'] = delay_list
#     return flights



# def append_mode_tod_taxi(df, tod_taxi_df):
#     import pandas as pd, numpy as np
    
#     flights = df.copy(deep=True).reset_index(drop=True)
#     delays = tod_taxi_df.copy(deep=True).reset_index(drop=True)
    
    
#     delay_list_in, delay_list_out = [], []
#     for i in range(len(flights)):
#         match_found = False

#         for j in range(len(delays)):
#             if all([flights['crs_dep_time'][i].hour == delays['Scheduled Departure (Hour)'][j],
#                     flights['crs_arr_time'][i].hour == delays['Scheduled Arrival (Hour)'][j],
#                     flights['origin'][i] == delays['Departing Airport'][j],
#                     flights['dest'][i] == delays['Arriving Airport'][j]
#                    ]):
                
#                 match_found = True
#                 delay_list_in.append(delays['Hourly Taxi-In Duration (Mode)'][j])
#                 delay_list_out.append(delays['Hourly Taxi-Out Duration (Mode)'][j])
#                 break
                
#         if match_found == False:
#             print(f'No match found for flights row {i}. Filling with NaN')
#             delay_list_in.append(np.nan)
#             delay_list_out.append(np.nan)
            
#     flights['Mode TOD Taxi-In IDX'] = delay_list_in
#     flights['Mode TOD Taxi-Out IDX'] = delay_list_out
#     return flights


# def append_median_tod_taxi(df, tod_taxi_df):
#     import pandas as pd, numpy as np
    
#     flights = df.copy(deep=True).reset_index(drop=True)
#     delays = tod_taxi_df.copy(deep=True).reset_index(drop=True)
    
    
#     delay_list_in, delay_list_out = [], []
#     for i in range(len(flights)):
#         match_found = False

#         for j in range(len(delays)):
#             if all([flights['crs_dep_time'][i].hour == delays['Scheduled Departure (Hour)'][j],
#                     flights['crs_arr_time'][i].hour == delays['Scheduled Arrival (Hour)'][j],
#                     flights['origin'][i] == delays['Departing Airport'][j],
#                     flights['dest'][i] == delays['Arriving Airport'][j]
#                    ]):
                
#                 match_found = True
#                 delay_list_in.append(delays['Hourly Taxi-In Duration (Median)'][j])
#                 delay_list_out.append(delays['Hourly Taxi-Out Duration (Median)'][j])
#                 break
                
#         if match_found == False:
#             print(f'No match found for flights row {i}. Filling with NaN')
#             delay_list_in.append(np.nan)
#             delay_list_out.append(np.nan)
            
#     flights['Median TOD Taxi-In IDX'] = delay_list_in
#     flights['Median TOD Taxi-Out IDX'] = delay_list_out
#     return flights


# def append_tod_traffic(df, tod_traffic_df):
#     import pandas as pd, numpy as np
    
#     flights = df.copy(deep=True).reset_index(drop=True)
#     delays = tod_traffic_df.copy(deep=True).reset_index(drop=True)
    
    
#     delay_list_arr, delay_list_dep = [], []
#     for i in range(len(flights)):
#         dep_match_found, arr_match_found = False, False

#         for j in range(len(delays)):
#             if all([flights['crs_dep_time'][i].hour == delays['Hour'][j],
#                     flights['origin'][i] == delays['Airport'][j],
#                    ]):
                
#                 dep_match_found = True
#                 delay_list_dep.append(delays['Flights'][j])

                
#             if all([flights['crs_arr_time'][i].hour == delays['Hour'][j],
#                     flights['dest'][i] == delays['Airport'][j],
#                    ]):
                
#                 arr_match_found = True
#                 delay_list_arr.append(delays['Flights'][j])    
                
                
                
#         if dep_match_found == False:
#             print(f'No match found for dep flights row {i}. Filling with NaN')
#             delay_list_dep.append(np.nan)
            
#         if arr_match_found == False:
#             print(f'No match found for arr flights row {i}. Filling with NaN')
#             delay_list_arr.append(np.nan)

                      
#     flights['TOD Dep Traffic IDX'] = delay_list_dep
#     flights['TOD Arr Traffic IDX'] = delay_list_arr
#     return flights