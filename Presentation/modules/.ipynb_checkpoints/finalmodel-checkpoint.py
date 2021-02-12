def final_results():
    import pandas as pd
    
    
    params_dictionary = {'booster': 'gbtree',
    'colsample_bylevel': 0.5,
    'colsample_bytree': 0.5,
    'learning_rate': 0.1,
    'max_depth': 2,
    'n_estimators': 125,
    'reg_alpha': 0.5,
    'reg_lambda': 1,
    'subsample': 1}
    
    
    print(pd.DataFrame(params_dictionary, index=['Values']))
    print('\n')
    
    scores_t = {'XGB Baseline': [0.015, 0.07],
           'XGB Engineered': [0.026, 0.05]}
    
    print(pd.DataFrame(scores_t, index=[['Test', 'Train']]))