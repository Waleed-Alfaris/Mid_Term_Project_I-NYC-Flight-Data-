def arr_delays(df, agg='monthly', agg_obj='median'):
    '''Function that accepts a dataframe with columns ['fl_date', 'mkt_unique_carrier', 'origin', 'dest', 'crs_dep_time', 'crs_arr_time', 'arr_delay']
    and returns an aggregated dataframe with the median or mode of arrival delays. Aggreagation is by airline->origin->destination.
    
        Parameters:
        df: (dataframe) to aggregate.
        agg: (str) options {'monthly', 'hourly'}. Type of aggregation to perform. Default='monthly'.
        agg_obj: (str) options {'median', 'mode'}. Objective of aggregation. Default='median'.
        
        Returns:
        dataframe with aggregated information on median arrival delays.'''   
    
    import numpy as np, pandas as pd
    import math
    from scipy.stats import mode
    flights = df.copy(deep=True)
    
   
    #drop columns we don't need
    print('Dropping columns...') 
    flights = flights.loc[:, ['fl_date', 'mkt_unique_carrier', 'origin', 'dest', 'crs_dep_time', 'crs_arr_time', 'arr_delay']]
    flights['fl_date'] = pd.to_datetime(flights['fl_date'].astype(str), format='%Y-%m-%d') #convert fl_date feature into datetime
    
    
    
    #monthly aggregation parameter
    if agg == 'monthly':
        
        #median parameter
        if agg_obj == 'median':
            print('Aggregating by monthly median...')
            flights = flights.groupby(by=[flights['fl_date'].dt.month, 'mkt_unique_carrier', 'origin', 'dest']).median()['arr_delay'].reset_index()

            print('Cleaning output...')
            #there are 465 routes in the table that do not exist for some airlines during specific months. Will drop
            flights = flights.dropna().reset_index(drop=True)
            flights.rename(columns={'fl_date': 'Month', 
                                    'mkt_unique_carrier': 'Airline', 
                                    'arr_delay': 'Monthly Arrival Delay(Median)',
                                    'origin': 'Departing Airport',
                                    'dest': 'Arriving Airport'}, inplace=True)

            print('Complete! Aggregated dataframe returned.\n')
            
        #mode parameter
        elif agg_obj == 'mode':
            print('Aggregating by monthly mode...')
            flights = flights.groupby(by=[flights['fl_date'].dt.month, 'mkt_unique_carrier', 'origin', 'dest'])['arr_delay'].agg(pd.Series.mode).reset_index()

            print('Cleaning output...')
            #there are 465 routes in the table that do not exist for some airlines during specific months. Will drop
            flights = flights.dropna().reset_index(drop=True)
            flights.rename(columns={'fl_date': 'Month', 
                                    'mkt_unique_carrier': 'Airline', 
                                    'arr_delay': 'Monthly Arrival Delay(Mode)',
                                    'origin': 'Departing Airport',
                                    'dest': 'Arriving Airport'}, inplace=True)
            
            mode_list = []
            for row in range(len(flights)):
                if 'ndarray' in str(type(flights['Monthly Arrival Delay(Mode)'][row])):
                    mode_list.append(flights['Monthly Arrival Delay(Mode)'][row].mean()) #if there are multiple modes, take the mean of them all
                    
                else:
                    mode_list.append(flights['Monthly Arrival Delay(Mode)'][row])
                    
            
            flights['Monthly Arrival Delay(Mode)'] = mode_list #replace column with a single number for each row
            flights.dropna(inplace=True) #drop the 400 or so rows that dont have routes

            print('Complete! Aggregated dataframe returned.\n')
            
        else:
            print('Please enter a valid agg_obj. Options are "median" and "mode"')   
            
        return flights
        
    
    
    #hourly aggregation paramter
    elif agg == 'hourly':
        
        #convert crs_dep_time and crs_arrival_time into datetime objects
        #first have to go through and fix the format of the original columns
        print('Grabbing time columns...')    
        time_of_day_df = flights[['crs_dep_time', 'crs_arr_time']].astype(str) #convert to string to be able to iterate through indecies
        col_position = 0 #position of column being changed in reformatting loop below
        cols = ['crs_dep_time', 'crs_arr_time']
        
        for col in cols: #run on both columns
        
            print(f'Formatting {col} for datetime object conversion...')        
            for row in range(len(time_of_day_df)): #iterate through every row
                if time_of_day_df[col][row] == '2400': 
                    time_of_day_df.iloc[row, col_position] = '00:00' #change 2400 to 0000 as this is the datetime module standard

                elif len(time_of_day_df[col][row]) == 1:
                    time_of_day_df.iloc[row, col_position] = '00:0' + time_of_day_df[col][row]

                elif len(time_of_day_df[col][row]) == 2:
                    time_of_day_df.iloc[row, col_position] = '00:' + time_of_day_df[col][row]

                elif len(time_of_day_df[col][row]) == 3:
                    time_of_day_df.iloc[row, col_position] = '0' + time_of_day_df[col][row][0] + ':' +time_of_day_df[col][row][1:]

                else:
                    time_of_day_df.iloc[row, col_position] = time_of_day_df[col][row][0:2] + ':' + time_of_day_df[col][row][2:]
                    
            
            print(f'Converting {col} into datetime object...')
            flights[col] = time_of_day_df[col] #replace column in original dataframe with new datetime object column
            flights[col] = pd.to_datetime(flights[col], format='%H:%M') #convert column to datetime object
            col_position += 1 #increase col_position to 1 and run again for arr_time
        
        
        if agg_obj == 'median':
            print('Aggregating by hourly median...')
            flights = flights.groupby(by=[flights['crs_dep_time'].dt.hour, 
                                          flights['crs_arr_time'].dt.hour, 
                                          'mkt_unique_carrier', 
                                          'origin', 
                                          'dest']).median()['arr_delay'].reset_index()
            
            print('Cleaning output...')
            #there are 483 routes in the table that do not exist for some airlines during specific times. Will drop
            flights = flights.dropna().reset_index(drop=True)
            flights.rename(columns={'crs_dep_time': 'Scheduled Departure (Hour)',
                                    'crs_arr_time': 'Scheduled Arrival (Hour)',
                                    'mkt_unique_carrier': 'Airline', 
                                    'arr_delay': 'Hourly Arrival Delay(Median)',
                                    'origin': 'Departing Airport',
                                    'dest': 'Arriving Airport'}, inplace=True)
            
        elif agg_obj == 'mode':
            print('Aggregating by hourly mode...')
            flights = flights.groupby(by=[flights['crs_dep_time'].dt.hour, 
                                          flights['crs_arr_time'].dt.hour, 
                                          'mkt_unique_carrier', 
                                          'origin', 
                                          'dest'])['arr_delay'].agg(pd.Series.mode).reset_index()
            
            print('Cleaning output...')
            #there are 483 routes in the table that do not exist for some airlines during specific times. Will drop
            flights = flights.dropna().reset_index(drop=True)
            flights.rename(columns={'crs_dep_time': 'Scheduled Departure (Hour)',
                                    'crs_arr_time': 'Scheduled Arrival (Hour)',
                                    'mkt_unique_carrier': 'Airline', 
                                    'arr_delay': 'Hourly Arrival Delay(Mode)',
                                    'origin': 'Departing Airport',
                                    'dest': 'Arriving Airport'}, inplace=True)
            
            mode_list = []
            for row in range(len(flights)):
                if 'ndarray' in str(type(flights['Hourly Arrival Delay(Mode)'][row])):
                    mode_list.append(flights['Hourly Arrival Delay(Mode)'][row].mean()) #if there are multiple modes, take the mean of them all
                    
                else:
                    mode_list.append(flights['Hourly Arrival Delay(Mode)'][row])
                    
            flights['Hourly Arrival Delay(Mode)'] = mode_list #replace column with a single number for each row
            flights.dropna(inplace=True) #drop the 400 or so rows that dont have routes
            
        else:
            print('Please enter a valid agg_obj. Options are "median" and "mode"')
        
              
        print('Complete! Aggregated dataframe returned.\n')
        return flights
    
    else:
        print('Please enter a valid agg. Options are "monthly" and "hourly"')