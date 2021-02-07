def create_carrier_sample(df, plot=False, max_iter=200, verbose=False):
    '''Function that returns a representative sample, if one exists, from the input dataset. Returns an error if no sample passes Kolmogorov-Smirnov test.
    
    Parameters:
    df: (DataFrame) Consolidated carrier dataframe.
    plot=False: (Bool) indicator of whether to return the histograms instead of the sample. If plot=True, function will not return a sample.
    max_iter=100: (int) maximum number of samples to test before returning a failed status.
    verbose=False: (Bool) classifier. If set to True, status updates will be provided.
    
    Returns:
    Dataframe: Sample DataFrame generated from input (if plot=False).
    Plot: side by side histogram plots of every feature in the sample compared to every feature in the input (if plot=True).
    
    This function accepts input dataframe, plot(optional), and max_iter(optional) arguments. Returns arandom sample taken from carrier dataframe, if one exists, or a "fail" response if no viable sample is found. If plot is set to True, this function will return histograms of sample features against input dataset features for visualization.   
    
    '''
    
    import pandas as pd, numpy as np
    from sklearn.utils import shuffle #shuffle used to generate random sample
    from scipy.stats import ks_2samp #2 sample Kolmogorov-Smirnov test. Will determine if generated sample has same distribution as carrier
    carrier = df.copy(deep=True) #copy input df
    pop_size = 15927485 #total size of flights table
    pop_sample_size = 100000 #total size of final population sample (inlcudes all airlines)
    carrier_sample_size = int(pop_sample_size/pop_size * len(carrier)) #frequency of this carrier in final sample shall have the same frequency it had in the entire flights dataset
    
    carrier_num = carrier.select_dtypes(include=['float'])
    carrier_obj = carrier.select_dtypes(exclude=['float'])
    
    complete = 0
    iterator = 0
    while iterator < max_iter and complete == 0:

        if verbose == True and (iterator) in np.arange(0, 101, 5): #if verbose is set to True, provide status update every 5 iterations
            print(f'Generating and testing samples.\nAttempt: {iterator}\nRandom_State: {iterator + 10}')

        #generate random sample    
        carrier_sample_num, carrier_sample_obj = shuffle(carrier_num,
                                                         carrier_obj,
                                                         n_samples=carrier_sample_size,
                                                         random_state=iterator + 10
                                                         )

        #begin sample equality test
        p_values = []
        passed = False #variable to track if sample has passed the KS test
        for feature in carrier_num.columns:            
            _, p_value = ks_2samp(carrier_sample_num[feature], carrier_num[feature]) #compare sample to carrier feature for feature

            if p_value >= 0.05: #if p-value less than 0.05, then the two samples do not share the same distribution and the test fails
                p_values.append(True)
            
            else:
                p_values.append(False)

        if False not in p_values:
            passed = True
            complete = 1 #exit loop if all p-values passed
            
        else:
            iterator +=1
                
    if verbose == True and passed == True:
        print(f'Sample passed KS test with Random_State: {iterator + 10}')

    #code to genrate plots if plot=True. Note, this will prevent a dataframe from being returned
    if plot == True:
        
        if verbose == True:
            print('Generating plots.')
        elif passed == True:
            print(f'Sample passed KS test with Random_State: {iterator + 10}\nGenerating plots.')
            
        #output hist plot of sample vs carrier
        #this can be used to visually inspect the feature distributions for the sample vs the carrier
        import matplotlib.pyplot as plt

        plt.figure(figsize=(20, 200))
        plot = 1 #tracking position of plot to generate
        
        for i,j in enumerate(carrier_sample_num.columns):
                #total number of rows = total number of columns. 2 plots per row (sample vs carrier)
                plt.subplot(len(carrier_sample_num.columns), 2, plot) 
                plt.hist(carrier_sample_num[j]) #sample plot
                plt.title(f'{carrier_sample_num.columns[i]} (Carrier Sample)')
                plot += 1 #increase plot by one for next plot position

                plt.subplot(len(carrier_sample_num.columns), 2, plot) #carrier plot will be positioned to the right of sample plot
                plt.hist(carrier_num[j]) #carrier plot
                plt.title(f'{carrier_num.columns[i]} (Carrier)')
                plot += 1 #increase plot by one and repeat untill all columns have been plotted for both DF

        plt.tight_layout()
        plt.show() #display the plots
    
    
    elif passed == True: #if sample passes test and plot not equal to True, return sample       
        if verbose == True:
            print('Process complete. Sample returned')
        
        output_sample = pd.concat([carrier_sample_num, carrier_sample_obj], axis=1)
        output_sample = output_sample[carrier.columns]
        
        return output_sample
    
    else:
        print('Max iterations reached. Sample failed to pass equality test') #if no sample passes the test after max_iter has been reached, return an error


        
        
        
def save_sample(df, file_name, path='../Data Exploration/samples/'):
    '''Function that will save a sample as a new csv file in "Data Exploration/samples"
    
    Parameters:
    df: (DF) sample dataframe to save
    file_name: (str) name of file
    path="../samples/": destination path to save file. Default is "Data Exploration/samples/"'''
    
    import pandas as pd
    sample = df.copy(deep=True)
    sample.to_csv(path + file_name + '.csv', sep=';', index=False)
    print('Sample saved.')