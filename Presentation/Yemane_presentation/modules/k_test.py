def different_distributions():
    import plotly.figure_factory as ff
    import numpy as np

    x1 = np.random.randn(200) - 2
    x2 = np.random.randn(200)
    x3 = np.random.randn(200) + 2

    hist_data = [x1, x2, x3]

    group_labels = ['Sample 1', 'Polation', 'Sample 2']
    colors = ['#A56CC1', '#A6ACEC', '#63F5EF']

    # Create distplot with curve_type set to 'normal'
    fig = ff.create_distplot(hist_data, group_labels, colors=colors,
                         bin_size=.2, show_rug=False)

    # Add title
    fig.update_layout(title_text='Sample Distribution Vs. Population Distribution')
    fig.show()