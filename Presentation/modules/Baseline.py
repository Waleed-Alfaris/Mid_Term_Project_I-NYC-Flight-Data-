def baseline_results():
    
    import pandas as pd
    scores_b = {'LinReg': [-0.04, 0.016],
    'PolyLinReg': [-2.96, 0.023],
    'RandomForest': [0.014, 0.029],
    'XGB (Best)': [0.015, 0.07]}
    
    
    baseline_scores_df = pd.DataFrame(scores_b, index=['Test', 'Train'])
    print(baseline_scores_df)
    
    
    import plotly.express as px
    fig19 = px.bar(x=baseline_scores_df.columns,
              y=baseline_scores_df.iloc[0,:].values,
              width=1000,
              height=200,
              range_y=(0, 0.02))

    fig20 = px.bar(x=baseline_scores_df.columns,
              y=baseline_scores_df.iloc[1,:].values,
              width=1000,
              height=200,
              range_y=(0, 0.08))
    
    fig19.show()
    fig20.show()