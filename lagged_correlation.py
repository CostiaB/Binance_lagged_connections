import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def crosscorr(data_x, data_y, lag=0):
    '''
    Lag_N cross correlation.
    Params:
    data_x, data_y: pandas series of the same length
    
    Returns:
    correlation: float
    '''
    return data_x.corr(data_y.shift(lag))

def window_lagged_crosscorr(data1, data2, lags_range, lag_steps, no_splits, return_corr=False):
    '''
    data1, data2: pandas series of the same length
    lags_range (int): range borders of lags (from  -lags_range to  lags_range)
    lags_steps (int): step of lags
    no_splits (int): number of splits
    return_corr (bool): whether to return correlations dataframe or not
    '''
    samples_per_split = data1.shape[0] / no_splits
    crosscorrs = []
    d1_name = data1.name
    d2_name = data2.name
    arr = np.array(range(-int(lags_range), int(lags_range+1), lag_steps))
    step = len(range(-int(lags_range), int(lags_range+1), lag_steps)) // 8
    ticks = list(np.where(np.in1d(arr, arr[::step]))[0])
    ticks_labels = list(arr[::step])
    range_val = range(-int(lags_range), int(lags_range+1), lag_steps) 
    
    for t in range(0, no_splits):
        
        d1 = data1.loc[(t)*samples_per_split:(t+1)*samples_per_split]
        d2 = data2.loc[(t)*samples_per_split:(t+1)*samples_per_split]
        window_corrs = [crosscorr(d1, d2, lag) for lag in range_val]
        crosscorrs.append(window_corrs)
        
    crosscorrs = pd.DataFrame(crosscorrs)
    f, ax = plt.subplots(figsize=(20,10))
    sns.heatmap(crosscorrs, cmap='RdBu_r', ax=ax)
    ax.set(title=f'Windowed Time Lagged Cross Correlation between \n {d1_name} and {d2_name}',
           xlabel='Offset, minutes',
           ylabel='Window number')
    ax.set_xticks(ticks)
    ax.set_xticklabels(ticks_labels, rotation=70, fontsize=14)
    plt.show()
    if return_corr == True:
        return crosscorrs

def rolling_window_lagged_crosscorr(data1, data2, lags_range, lag_steps, 
                                    window_size, step_size , return_corr=False,
                                    plot_graph = True):
    '''
    data1, data2: pandas series of the same length
    lags_range (int): range borders of lags (from  -lags_range to  lags_range)
    lags_step (int): step of lags
    window_size (int): window size
    step_size (int): step for window moving
    return_corr (bool): whether to return correlations dataframe or not
    plot_graph (bool): whether plot the correlations plot or not
    '''
    t_start = 0
    t_end = t_start + window_size
    crosscorrs = []
    idx = []
    d1_name = data1.name
    d2_name = data2.name
    arr = np.array(range(-int(lags_range), int(lags_range+1), lag_steps))
    range_val = range(-int(lags_range), int(lags_range+1), lag_steps)
    step = len(range(-int(lags_range), int(lags_range+1), lag_steps)) // 8
    ticks = list(np.where(np.in1d(arr, arr[::step]))[0])
    ticks_labels = list(arr[::step])
    
    while t_end < data1.shape[0]:
        
        d1 = data1.iloc[t_start:t_end]
        d2 = data2.iloc[t_start:t_end]
        window_corrs  = [crosscorr(d1, d2, lag) for lag in range_val]
        idx.append(t_start)
        crosscorrs.append(window_corrs)
        t_start = t_start + step_size
        t_end = t_end + step_size
        
    crosscorrs = pd.DataFrame(crosscorrs, index=idx)
    if plot_graph == True:
        f,ax = plt.subplots(figsize=(20,20))
        sns.heatmap(crosscorrs, cmap='RdBu_r', ax=ax)
        ax.set(title=f'Rolling Windowed Time Lagged Cross Correlation between \n {d1_name } and {d2_name }',
               xlabel='Offset, minutes',
               ylabel='Window number')
        ax.set_xticks(ticks)
        ax.set_xticklabels(ticks_labels, rotation=70, fontsize=14)
        plt.show()
    if return_corr == True:
        return crosscorrs

def best_lags(df, arr, threshold=0.95, drop_zero_lag=True):
    
    '''
    Inputs:
    df(pd.Dataframe): dataframe with correlations between two tickers
    arr(np.array): array with lags values
    threshld(float): threshold levelfor correlation
    Returns:
    check(pd.Dataframe): dataframe with lags above threshold with window start
    '''
    top_corr_list = []
    for i in range(0, len(df)):
        
        test = pd.DataFrame()
        test['corr'] = df.iloc[i,:][df[abs(df)>threshold].iloc[i,:].notnull()]
        test.index = arr[df.iloc[i,:][df[abs(df)>threshold].iloc[i,:].notnull()].index]
        if len(test) > 0:
            name = [df.iloc[i,:].name]
            val = [[{'lag':i, 'corr':j} for i, j in zip(test.index, test.iloc[:,0])]]
            if drop_zero_lag==True:
                val = [[el for el in val[0] if el['lag']!=0]]
            if len(val[0]) != 0:
                top_corr_list.append(name+val)
            
    check = pd.DataFrame(top_corr_list)
    check.columns = ['window_start', 'lags']
    check['lags'] = check.lags.apply(lambda y: sorted(y, key=lambda x: abs(x['corr']), reverse=True))
    return check


def plot_corr_windows(col1, col2, lags_range, lag_step,
                                    window_size, step_size,
                                    arr, threshold=0.95):
    '''
    Inputs:
    col1,col2 pandas series of the same length
    lags_range (int): range borders of lags (from  -lags_range to  lags_range)
    lags_step (int): step of lags
    window_size (int): window size
    step_size (int): step for window moving
    arr(np.array): array with lags values
    threshld(float): threshold levelfor correlation
    '''
    
    df = rolling_window_lagged_crosscorr(
                                    col1,
                                    col2,
                                    lags_range, lag_step,
                                    window_size, step_size,
                                    return_corr=True,
                                    plot_graph=False)
    check = best_lags(df, arr, threshold)
    fig, axs = plt.subplots(2,3, figsize=(16,10))
    for i in range(0,6):
        lag, wind, corr = check.iloc[i,1][0]['lag'], check.iloc[i,0], check.iloc[i,1][0]['corr']
        name1 = col1.name
        name2 = col2.name

        data1 = col1 \
                 [wind + lag:  wind + window_size + lag].\
                 reset_index(drop = True) 
        data2 = col2 \
                 [wind:wind + window_size].reset_index(drop = True)
        data1 -= data1.mean()
        data2 -= data2.mean()
        axs[i//3, i%3].plot(data1, label = name1)
        axs[i//3, i%3].plot(data2, label = name2)
        axs[i//3, i%3].set_title(f"Window: {wind} lag:{lag} minutes corr: {round(corr,2)}" )
        axs[i//3, i%3].legend()
    plt.show()

def most_common_lags(df):
    '''
    Input:
    df(pd.Dataframe) : dataframe with lags above threshold with window start
    Returns:
    lag_count (dict) : dictionary with count of lags
    '''
    lags_count = {}
    for _, lag in df.iterrows():
        for el in lag[1]:

            if el['lag'] in lags_count.keys():
                lags_count[el['lag']] += 1
            else:
                lags_count[el['lag']] = 1
    lags_count = {k: lags_count[k] for k in sorted(
                                            lags_count,
                                            key=lags_count.get,
                                            reverse=True)}
    return lags_count    