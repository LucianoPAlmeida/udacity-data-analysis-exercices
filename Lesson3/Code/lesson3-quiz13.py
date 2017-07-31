import numpy as np
import pandas as pd

df = pd.DataFrame({
    'a': [4, 5, 3, 1, 2],
    'b': [20, 10, 40, 50, 30],
    'c': [25, 20, 5, 15, 10]
})

# Change False to True for this block of code to see what it does
def second_largest_column(row):
    max_v = row.max()
    second = row.min()
    for i in row.index:
        if row.iloc[i] > second and row.iloc[i] != max_v:
            second = row[i]
    return second
# DataFrame apply() - use case 2
if False:   

    print df.apply(second_largest_column)
def second_largest(df):
    return df.apply(second_largest_column, axis=0)