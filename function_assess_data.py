# %%
import pandas as pd
import numpy as np
import matplotlib as mpl

# %%
# function to quickly assess a dataframe's completeness and basic descriptive statistics
# makes a distinction between missing (na) and emtpy strings, strings that are just whitespace, etc.
# returns counts for strings; gregates for numeric columns
# optional argument styles output dataframe with color bars

from collections import defaultdict

def assess_data(df, highlight_color):

    np.seterr(divide='ignore', invalid='ignore')
    all_dict = defaultdict(list) 
    str_cols = df.select_dtypes(include=[object]).columns.tolist()
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    for i in df[str_cols]:
        str_is_null = df[i].isna().sum()
        str_spaces = df[i].str.contains(r'^\s{1,}$').sum()
        str_empty_string = len(df.loc[df[i]==''])

        string_dict = {'str_is_null' : str_is_null, 'str_spaces' : str_spaces
                       , 'str_empty_string' : str_empty_string}
        all_dict[i].append(string_dict)
    
    for i in df[num_cols]:
        num_is_null = df[i].isna().sum()
        num_mean_val = df[i].mean()
        num_min_val = df[i].min()
        num_max_val = df[i].max()
        num_unique_count = df[i].nunique()

        num_dict = {'num_is_null' : num_is_null, 'num_mean_val' : num_mean_val, 'num_min_val' : num_min_val
                    , 'num_max_val' : num_max_val, 'num_unique_count' : num_unique_count}
        all_dict[i].append(num_dict)

    x = pd.DataFrame(data=all_dict).T
    x.columns = ['column_summary']
    x.index.name = 'column_name'
    summarized_df = pd.json_normalize(x['column_summary'])
    summarized_df.index = x.index
    summarized_df = summarized_df.fillna(0)
    
    return summarized_df.style.format(precision=1, thousands=",").bar(color=highlight_color)


# %%
# test 

mydict = {'food' : ['sandwich', 'cereal', 'pizza', 'ice cream', np.nan, "   ", "  ", np.nan],
'animals' : ['puppy', 'kitty', 'dolphin', 'penguin', np.nan, '', '', np.nan],
'numbers' : [1, 2, np.nan, 0, 5, 6, np.nan, np.nan],
'pcts' : [.4, .02, 1.0, np.nan, .2, .0002, .66, np.nan]
}

my_df = pd.DataFrame(data=mydict)

# %%
assess_data(my_df, 'green')


# %%
# compare output of assess_data to output of 'describe'

my_df.describe(include='all') 
