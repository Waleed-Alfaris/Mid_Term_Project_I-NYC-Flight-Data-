def create_carrier_sample(df, plot=False, max_iter=100, verbose=False):
    '''Generates a random sample from the input carrier and returns a representative sample, if one exists. Returns an error if no sample passes Kolmogorov-Smirnov test.    
    
    Parameters:
    df: (DataFrame) Consolidated carrier dataframe.
    plot=False: (Bool) indicator of whether to plot the histograms or not. If plot=True, function will not return a sample.
    max_iter=100: (int) maximum number of samples to test before returning a failed status.
    verbose=False: (Bool) classifier. If set to True, status updates will be provided.
    
    Returns:
    Dataframe: Sample DataFrame generated from input (if plot=False).
    Plot: side by side histogram plots of every feature in the sample compared to every feature in the input (if plot=True).
    
    This function accepts input dataframe, random_state(optional), plot(optional), and max_iter(optional) arguments. Returns arandom sample taken from carrier dataframe, if one exists, or a "fail" response if no viable sample is found. If plot is set to True, this function will return histogram plots of sample vs carrier for sample evaluation.   
    
    '''
    
    import pandas as pd
    carrier = df.copy(deep=True) #copy input df
    pop_size = 15927485 #total size of flights table
    pop_sample_size = 100000 #total size of final population sample (inlcudes all airlines)
    carrier_sample_size = int(pop_sample_size/pop_size * len(carrier)) #frequency of this carrier in final sample shall have the same frequency it had in the entire flights dataset

    
    #create seperate dataset for object types and numerical types
    #this will help in checking if sample is a good representation of population
    carrier_obj = carrier.select_dtypes(include='object')
    carrier_num = carrier.select_dtypes(include=['int64', 'float'])


    from sklearn.utils import shuffle #shuffle the two datasets in unison and provide a sample fo each to test
    rand_state=120 #random seed to use
    

    for iterator in range(max_iter):

        if verbose == True and (iterator + 1) in [1, 25, 50, 75, 100]: #if verbose is set to True, provide status update every 25 iterations
            print(f'Generating and testing sample.\nAttempt: {iterator + 1}\nRandom_State: {rand_state}')

        carrier_num_sample, carrier_obj_sample = shuffle(carrier_num, 
                                                         carrier_obj,
                                                         n_samples=carrier_sample_size,
                                                         random_state=rand_state
                                                         )

        from scipy.stats import ks_2samp #2 sample Kolmogorov-Smirnov test. Will determine if generated sample has same distribution as carrier
        passed = True #variable to track if sample has passed the KS test

        p_values = [] #empty list to store p-values
        for i,j in enumerate(carrier_num.columns):            
            _, p_value = ks_2samp(carrier_num_sample[j], carrier_num[j]) #compare sample to carrier feature for feature

            if p_value <= 0.05: #if p-value less than 0.05, then the two sample do not share the same distribution and the test failed
                passed = False #set passed status to false
                rand_state += 1 #change random state so we can try again with a new sample
                break #exit the loop and start again with the new random_seed
         
        if verbose == True:
            print(f'Sample passed KS test.\nAttempt: {iterator + 1}\nRandom_State: {rand_state}')
            break

    #code to genrate plots if plot=True. Note, this will prevent a dataframe from being returned
    if plot == True:
        
        if verbose == True:
            print('Generating plots.')
            
        #output hist plot of sample vs carrier
        #this can be used to visually inspect the feature distributions for the sample vs the carrier
        import matplotlib.pyplot as plt

        plt.figure(figsize=(20, 200))
        plot = 1 #tracking position of plot to generate
        
        for i,j in enumerate(carrier_num_sample.columns):
                #total number of rows = total number of columns. 2 plots per row (sample vs carrier)
                plt.subplot(len(carrier_num_sample.columns), 2, plot) 
                plt.hist(carrier_num_sample[j]) #sample plot
                plt.title(f'{carrier_num_sample.columns[i]} (Carrier Sample)')
                plot += 1 #increase plot by one for next plot position

                plt.subplot(len(carrier_num_sample.columns), 2, plot) #carrier plot will be positioned to the right of sample plot
                plt.hist(carrier_num[j]) #carrier plot
                plt.title(f'{carrier_num.columns[i]} (Carrier)')
                plot += 1 #increase plot by one and repeat untill all columns have been plotted for both DF

        plt.tight_layout()
        plt.show() #display the plots
    
    
    elif passed == True: #if sample passes test and plot not equal to True, return sample       
        if verbose == True:
            print('Process complete. Sample returned')
        
        output_sample = pd.concat([carrier_num_sample, carrier_obj_sample], axis=1)
        output_sample = output_sample[list(carrier.columns.values)] #format df to have same order as input
        return output_sample
    
    else:
        print('Max iterations reached. Sample failed to pass equality test') #if no sample passes the test after max_iter has been reached, return an error


        
        
        
def save_sample(df, file_name, path='../Data Exploration/samples/'):
    '''Function that will save a sample as a new csv file in "Data Exploration/samples"
    
    Parameters:
    df: (DF) sample dataframe to save
    file_name: (str) name of file
    path="../samples/": destination path to save file. Default is "Data Exploration/samples/"'''
    
    sample = df.copy(deep=True)
    sample.to_csv(path + file_name + '.csv', sep=';')
    print('Sample saved.')