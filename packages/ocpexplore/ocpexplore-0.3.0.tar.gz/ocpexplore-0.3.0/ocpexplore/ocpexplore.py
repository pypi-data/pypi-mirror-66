"""Main module."""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# Define custom functions

def value_counter(df, obj_cols_only = True, unique_limit = 25):
    
    
    if obj_cols_only:
    
        info = 'Unprocessed variables with object dtype: '
        
        for column in df:
            if df[column].dtypes=='object' and len(df[column].unique()) < unique_limit:
                df_temp = df[column].value_counts(dropna=False).rename_axis('unique_values').reset_index(name='counts')
                df_temp_2 =  df[column].value_counts(dropna=False,normalize=True).rename_axis('unique_values').reset_index(name='counts')
                df_merged = df_temp.merge(df_temp_2, left_on='unique_values', right_on='unique_values')
                df_merged.columns = ['unique_values', 'value_counts','ratio']
                df_merged['ratio'] = df_merged['ratio'].round(3)

                print(column)                      
                print(df_merged)
                print('')
                plt.show(df_merged.plot.bar(x='unique_values', y='value_counts'))
                print('')

            elif df[column].dtypes=='object' and len(df[column].unique()) >= unique_limit:
                info = info + column + ', '
                
    elif obj_cols_only == False:
        
        info = 'Unprocessed variables of any dtype: '
        
        for column in df:
            if len(df[column].unique()) < unique_limit:
                df_temp = df[column].value_counts(dropna=False).rename_axis('unique_values').reset_index(name='counts')
                df_temp_2 =  df[column].value_counts(dropna=False,normalize=True).rename_axis('unique_values').reset_index(name='counts')
                df_merged = df_temp.merge(df_temp_2, left_on='unique_values', right_on='unique_values')
                df_merged.columns = ['unique_values', 'value_counts','ratio']
                df_merged['ratio'] = df_merged['ratio'].round(3)

                print(column)                      
                print(df_merged)
                print('')
                plt.show(df_merged.plot.bar(x='unique_values', y='value_counts'))
                print('')

            elif len(df[column].unique()) >= unique_limit:
                info = info + column + ', '
                
        
    
    if info[-2] == ':':
        info = info + 'NA'
    elif info[-2] == ',':
        info = info[:-2]
        
    print(info)
    
    
def check_ID(df):
    for column in df:
        full = len(df[column]) 
        unique = len(df[column].unique())
        pct = round(unique/full*100,2)
        print("{} has {} values, and {} of which are unique ({}%).".format(column, full, unique, pct))

        
def check_NA(df):
    df_temp = df.isna().sum().rename_axis('variables').reset_index(name='NANs')
    df_temp_2 = df.isna().mean().rename_axis('variables').reset_index(name='ratio')
    df_merged = df_temp.merge(df_temp_2, left_on='variables', right_on='variables')
    df_merged['ratio'] = df_merged['ratio'].round(3)
    print(df_merged)
    
    plt.show(df_merged.plot.bar(x='variables', y='ratio'))
    

    
def plot_continuous(df):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for column in df:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
            fig.suptitle(column)
            sns.boxplot(df[column].dropna(), ax = ax1)
            sns.distplot(df[column].dropna(), ax = ax2)
            plt.show()
    

def describe_continuous(df, interpolation = 'nearest'):
    
    result = df.columns.to_series().reset_index(name='variable')[['variable']]
    
    smin = df.min().rename_axis('variable').reset_index(name='Min')
    result = result.merge(smin, left_on='variable', right_on='variable')
    
    for x in [.01, .05, .1, .25, .5, .75, .9, .95, .99]:
        temp = df.quantile(x, interpolation = interpolation).rename_axis('variable').reset_index(name=x)
        result = result.merge(temp, left_on='variable', right_on='variable')
    
    smax = df.max().rename_axis('variable').reset_index(name='Max')
    result = result.merge(smax, left_on='variable', right_on='variable')
    
    mean = df.mean().rename_axis('variable').reset_index(name='Mean')
    result = result.merge(mean, left_on='variable', right_on='variable')
    
    na = df.isna().sum().rename_axis('variable').reset_index(name='NaN')
    result = result.merge(na, left_on='variable', right_on='variable')
    
    return result


def tail_density_table(df, interpolation = 'nearest'):
    
    result = pd.DataFrame(["low_extreme", "low_outlier", "non_outlier", "high_outlier", "high_extreme"],columns =['bucket'])
    
    for column in df:
        quantiles = []
        for x in [.25, .75]:
            quantiles.append(df[[column]].quantile(x, interpolation = interpolation)[0])
        iq_range = quantiles[1]-quantiles[0]
        
        cutpoints = [-np.inf,(quantiles[0]-3*iq_range),(quantiles[0]-1.5*iq_range),(quantiles[1]+1.5*iq_range),(quantiles[1]+3*iq_range),np.inf]
        temp = pd.cut(df[column],cutpoints,labels = ["low_extreme", "low_outlier", "non_outlier", "high_outlier", "high_extreme"])
        temp = temp.value_counts().rename_axis('bucket').reset_index(name=column)
        result = result.merge(temp, left_on='bucket', right_on='bucket')
        
        
    result.index = result['bucket']
    result = result.drop(['bucket'], axis=1)
    result = result.T
    return(result)

def obs_by_date(column, date_aggregation = 'M'):
    
    column = column.dt.to_period(date_aggregation)
    to_plot = column.value_counts(sort = False)
    to_plot.plot()
    
    return to_plot
    

def values_by_date(df, date_column, date_aggregation = 'M'):
    
    df_temp = df.copy()
    new_colname = str(date_column) + '_' + str(date_aggregation)
    df_temp[new_colname] = df_temp[date_column].dt.to_period(date_aggregation)
    cols_to_plot = df_temp.columns.drop([new_colname,date_column])
    for col in cols_to_plot:
        df_temp.boxplot(column=col, by=new_colname, figsize=(9,9), grid=False)

    
