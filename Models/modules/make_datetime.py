def make_datetime(df):
    import numpy as np, pandas as pd
    flights = df.copy(deep=True)
    
    print('Converting fl_date...')
    flights['fl_date'] = pd.to_datetime(flights['fl_date'].astype(str), format='%Y-%m-%d') #convert fl_date feature into datetime
    
    
    #convert crs_dep_time and crs_arrival_time into datetime objects
    #first have to go through and fix the format of the original columns
    time_of_day_df = flights[['crs_dep_time', 'crs_arr_time']].astype(str) #convert to string to be able to iterate through indecies
    col_position = 0 #position of column being changed in reformatting loop below

    #THIS SHOULD BE A FUNCTION. COME BACK TO IT LATER
    for col in ['crs_dep_time', 'crs_arr_time']: #run on both columns

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


        flights[col] = time_of_day_df[col] #replace column in original dataframe with new datetime object column
        flights[col] = pd.to_datetime(flights[col], format='%H:%M') #convert column to datetime object
        col_position += 1 #increase col_position to 1 and run again for arr_time
        
    print('Complete! Converted df returned.')
    return flights
