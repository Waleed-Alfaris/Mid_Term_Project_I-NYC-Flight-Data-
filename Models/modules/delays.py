'''
This module currently contains 3 functions.

- delays()
- get_traffic()
- get_taxi_times()

See individual docstrings for more information.
'''




def delays(df, agg='monthly', agg_obj='median'):
    '''Function that accepts a dataframe with columns ['fl_date', 'mkt_unique_carrier', 'origin', 'dest', 'crs_dep_time', 'crs_arr_time', 'arr_delay']
    and returns an aggregated dataframe with the median or mode of arrival delays. Aggreagation is by airline->origin->destination.
    
        Parameters:
        df: (dataframe) to aggregate.
        
        agg: (str) options {'monthly', 'hourly'}. Type of aggregation to perform. Default='monthly'.
        
        agg_obj: (str) options {'median', 'mode'}. Objective of aggregation. Default='median'.
        
        Returns:
        df: dataframe with aggregated information on median or mode of delays.'''   
    
    import numpy as np, pandas as pd
    import math
    from scipy.stats import mode
    flights = df.copy(deep=True)
    

    #drop columns we don't need
    print('Dropping columns...') 
    flights = flights.loc[:, ['fl_date', 'mkt_unique_carrier', 'origin', 'dest', 'crs_dep_time', 'crs_arr_time', 'arr_delay']]


    #monthly aggregation parameter
    if agg == 'monthly':

        #median parameter
        if agg_obj == 'median':
            print('Aggregating by monthly median...')

            flights = flights.groupby(by=[flights['fl_date'].dt.month, 'origin']).median()['arr_delay'].reset_index()

            print('Cleaning output...')
            #there are 465 routes in the table that do not exist for some airlines during specific months. Will drop
            flights = flights.dropna().reset_index(drop=True)

            flights.rename(columns={'fl_date': 'Month', 
                                    'arr_delay': 'Monthly Arrival Delay (Median)',
                                    'origin': 'Departing Airport'}, inplace=True)

            print('Complete! Aggregated dataframe returned.\n')

        #mode parameter
        elif agg_obj == 'mode':
            print('Aggregating by monthly mode...')
            

            flights = flights.groupby(by=[flights['fl_date'].dt.month, 'origin'])['arr_delay'].agg(pd.Series.mode).reset_index()

            print('Cleaning output...')
            #there are 465 routes in the table that do not exist for some airlines during specific months. Will drop
            flights = flights.dropna().reset_index(drop=True)
            flights.rename(columns={'fl_date': 'Month', 
                                    'arr_delay': 'Monthly Arrival Delay (Mode)',
                                    'origin': 'Departing Airport'}, inplace=True)

            mode_list = []
            for row in range(len(flights)):
                if 'ndarray' in str(type(flights['Monthly Arrival Delay (Mode)'][row])):
                    mode_list.append(flights['Monthly Arrival Delay (Mode)'][row].mean()) #if there are multiple modes, take the mean of them all

                else:
                    mode_list.append(flights['Monthly Arrival Delay (Mode)'][row])


            flights['Monthly Arrival Delay (Mode)'] = mode_list #replace column with a single number for each row
            flights.dropna(inplace=True) #drop the 400 or so rows that dont have routes

            print('Complete! Aggregated dataframe returned.\n')

        else:
            print('Please enter a valid agg_obj. Options are "median" and "mode"')   

        return flights



    #hourly aggregation paramter
    elif agg == 'hourly':


        if agg_obj == 'median':
            print('Aggregating by hourly median...')
            
            flights = flights.groupby(by=[flights['crs_dep_time'].dt.hour, 
                                          flights['crs_arr_time'].dt.hour, 
                                          'origin']).median()['arr_delay'].reset_index()

            print('Cleaning output...')
            #there are 483 routes in the table that do not exist for some airlines during specific times. Will drop
            flights = flights.dropna().reset_index(drop=True)
            flights.rename(columns={'crs_dep_time': 'Scheduled Departure (Hour)',
                                    'crs_arr_time': 'Scheduled Arrival (Hour)',
                                    'arr_delay': 'Hourly Arrival Delay (Median)',
                                    'origin': 'Departing Airport'}, inplace=True)

        elif agg_obj == 'mode':
            print('Aggregating by hourly mode...')
            #getting error (ValueError: Function does not reduce) on this code block. Was working when 'dest' column was present??
            flights = flights.groupby(by=[flights['crs_dep_time'].dt.hour, 
                                          flights['crs_arr_time'].dt.hour, 
                                          flights['origin']])['arr_delay'].agg(pd.Series.mode).reset_index()

            print('Cleaning output...')
            #there are 483 routes in the table that do not exist for some airlines during specific times. Will drop
            flights = flights.dropna().reset_index(drop=True)
            flights.rename(columns={'crs_dep_time': 'Scheduled Departure (Hour)',
                                    'crs_arr_time': 'Scheduled Arrival (Hour)',
                                    'arr_delay': 'Hourly Arrival Delay (Mode)',
                                    'origin': 'Departing Airport'}, inplace=True)

            mode_list = []
            for row in range(len(flights)):
                if 'ndarray' in str(type(flights['Hourly Arrival Delay (Mode)'][row])):
                    mode_list.append(flights['Hourly Arrival Delay (Mode)'][row].mean()) #if there are multiple modes, take the mean of them all

                else:
                    mode_list.append(flights['Hourly Arrival Delay (Mode)'][row])

            flights['Hourly Arrival Delay(Mode)'] = mode_list #replace column with a single number for each row
            flights.dropna(inplace=True) #drop the 400 or so rows that dont have routes

        else:
            print('Please enter a valid agg_obj. Options are "median" and "mode"')


        print('Complete! Aggregated dataframe returned.\n')
        return flights

    else:
        print('Please enter a valid agg. Options are "monthly" and "hourly"')

            
            
            
def get_taxi_times(df, agg_obj='median'):
    '''Function that accepts a dataframe with columns ['crs_dep_time', 'crs_arr_time', 'taxi_out', 'taxi_in', 'origin', 'dest']
    and returns an aggregated dataframe with the median or mode of taxi times. Aggreagation is by Dep Hour -> Arr Hour -> origin -> destination.
    
    Parameters:
    df: (dataframe) to aggregate.

    agg_obj: (str) options {'median', 'mode'}. Objective of aggregation. Default='median'.

    Returns:
    df: dataframe with aggregated information on median or mode of delays.'''  


    import numpy as np, pandas as pd
    import math
    from scipy.stats import mode
    flights = df.copy(deep=True)


    print('Dropping columns...') 
    flights = flights.loc[:, ['crs_dep_time', 'crs_arr_time', 'taxi_out', 'taxi_in', 'origin', 'dest']]        


    if agg_obj == 'median':
        print('Aggregating by hourly median...')
        flights = flights.groupby(by=[flights['crs_dep_time'].dt.hour,
                                      flights['crs_arr_time'].dt.hour]).median()[['taxi_out', 'taxi_in']].reset_index()

        print('Cleaning output...')
        #there are 300 or so routes in the table that do not exist for some airlines during specific times. Will drop
        flights = flights.dropna().reset_index(drop=True)
        flights.rename(columns={'crs_dep_time': 'Scheduled Departure (Hour)',
                                'crs_arr_time': 'Scheduled Arrival (Hour)',
                                'taxi_in': 'Hourly Taxi-In Duration (Median)',
                                'taxi_out': 'Hourly Taxi-Out Duration (Median)'}, inplace=True)



    elif agg_obj == 'mode':
        print('Aggregating by hourly median...')
        flights = flights.groupby(by=[flights['crs_dep_time'].dt.hour,
                                      flights['crs_arr_time'].dt.hour])[['taxi_out', 'taxi_in']].agg(pd.Series.mode).reset_index()

        print('Cleaning output...')
        #there are 300 or so routes in the table that do not exist for some airlines during specific times. Will drop
        flights = flights.dropna().reset_index(drop=True)
        flights.rename(columns={'crs_dep_time': 'Scheduled Departure (Hour)',
                                'crs_arr_time': 'Scheduled Arrival (Hour)',
                                'taxi_in': 'Hourly Taxi-In Duration (Mode)',
                                'taxi_out': 'Hourly Taxi-Out Duration (Mode)'}, inplace=True)

        mode_list_t_in, mode_list_t_out = [], []
        for row in range(len(flights)):
            if 'ndarray' in str(type(flights['Hourly Taxi-In Duration (Mode)'][row])) and 'ndarray' in str(type(flights['Hourly Taxi-Out Duration (Mode)'][row])):
                mode_list_t_in.append(flights['Hourly Taxi-In Duration (Mode)'][row].mean()) #if there are multiple modes, take the mean of them all
                mode_list_t_out.append(flights['Hourly Taxi-Out Duration (Mode)'][row].mean())

            elif 'ndarray' in str(type(flights['Hourly Taxi-In Duration (Mode)'][row])): #if not in both, check if in taxi-in
                mode_list_t_in.append(flights['Hourly Taxi-In Duration (Mode)'][row].mean())
                mode_list_t_out.append(flights['Hourly Taxi-Out Duration (Mode)'][row])

            elif 'ndarray' in str(type(flights['Hourly Taxi-Out Duration (Mode)'][row])): #if not in taxi-in, check if in taxi-out
                mode_list_t_in.append(flights['Hourly Taxi-In Duration (Mode)'][row])
                mode_list_t_out.append(flights['Hourly Taxi-Out Duration (Mode)'][row].mean())

            else:
                mode_list_t_in.append(flights['Hourly Taxi-In Duration (Mode)'][row])
                mode_list_t_out.append(flights['Hourly Taxi-Out Duration (Mode)'][row])

        flights['Hourly Taxi-In Duration (Mode)'] = mode_list_t_in #replace column with a single number for each row
        flights['Hourly Taxi-Out Duration (Mode)'] = mode_list_t_out
        flights.dropna(inplace=True) #drop the 400 or so rows that dont have routes


    else:
        print('Please enter a valid agg_obj. Options are "median" and "mode"')

    print('Complete! Aggregated dataframe returned.\n')
    return flights




def get_traffic(df):
    '''WARNING! For large datasets, this function will take a long time to complete.
    
    Function that accepts a dataframe with columns ['origin', 'dest', 'crs_dep_time', 'crs_arr_time', 'flights'] and returns avg hourly airport traffic in the form of number of flights taking off in that hour.
    
    Parameters:
    df: (dataframe) to aggregate.
    
    Returns:
    df: dataframe with aggregated information on median or mode of delays.
    '''
    
    import numpy as np, pandas as pd
    import math
    from scipy.stats import mode
    flights = df.copy(deep=True)
    

    #drop columns we don't need
    print('Dropping columns...') 
    flights = flights.loc[:, ['origin', 'dest', 'crs_dep_time', 'crs_arr_time', 'flights']]
        
    
    # will find the total number of flights that have departed and arrived at a given airport per hour over the 2 years
    # will then take this number as a traffic indicator. With scaling, I should not need to divide by the max value (scaling should do this for me)
    print('Calculating flights...')
    flights_origin = flights.groupby(by=[flights['crs_dep_time'].dt.hour, 'origin']).count()['flights'].reset_index() #hourly flights departing per hour by airport
    flights_dest = flights.groupby(by=[flights['crs_arr_time'].dt.hour, 'dest']).count()['flights'].reset_index() #hourly flights arriving per hour by airport

    flights_origin.rename(columns={'origin': 'Airport'}, inplace=True) #for simplicity
    flights_dest.rename(columns={'dest': 'Airport'}, inplace=True)
    
    #will use this dictionary to store listed tuples. The keys of the dictionary will be the unique airport, the values will be a list of tuples
    #tuplles will take the form (Hour, Sum of arriving and departing flights)
    temp_dict = {}
    
    #for every row in origin, iterate through every row in dest to find a matching airport and hour
    #when a match is found, store that airport as a key, if it does not already exist and store a tuple as its value
    #if key exists, simply append a new tuple
    print('Searching for matching records...')
    for i in range(len(flights_origin)):
        for j in range(len(flights_dest)): #search for a match
            if (flights_origin['Airport'][i] == flights_dest['Airport'][j]) and (flights_origin['crs_dep_time'][i] == flights_dest['crs_arr_time'][j]): 
                if flights_origin['Airport'][i] not in list(temp_dict.keys()): #check that airport is not already a key
                    temp_dict[flights_origin['Airport'][i]] = [(flights_origin['crs_dep_time'][i], (flights_origin['flights'][i] + flights_dest['flights'][j]))] 
                    #create new key for the airport and store the tuple
                    
                    
                else: #if already a key, append the new tuple
                    temp_dict[flights_origin['Airport'][i]].append((flights_origin['crs_dep_time'][i], (flights_origin['flights'][i] + flights_dest['flights'][j])))
                
                
    #WOW! this crazy list comprehension was taken from stackoverflow. Pretty amazing.
    #Will need someone to explain how this is working (in particular the *t)
    #this line of code will convert the dictionary into a list that can be passed into pd.DataFrame
    L = [(k, *t) for k, v in temp_dict.items() for t in v]          
    
    #generate final output
    flights = pd.DataFrame(L, columns=['Airport','Hour','Flights'])
    
    print('Complete! Aggregated dataframe returned.\n')
    return flights
