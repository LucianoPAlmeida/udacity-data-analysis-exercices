import pandas as pd

# Examples of vectorized operations on DataFrames:
# Change False to True for each block of code to see what it does

# Adding DataFrames with the column names
if False:
    df1 = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]})
    df2 = pd.DataFrame({'a': [10, 20, 30], 'b': [40, 50, 60], 'c': [70, 80, 90]})
    print df1 + df2
    
# Adding DataFrames with overlapping column names 
if False:
    df1 = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]})
    df2 = pd.DataFrame({'d': [10, 20, 30], 'c': [40, 50, 60], 'b': [70, 80, 90]})
    print df1 + df2

# Adding DataFrames with overlapping row indexes
if False:
    df1 = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]},
                       index=['row1', 'row2', 'row3'])
    df2 = pd.DataFrame({'a': [10, 20, 30], 'b': [40, 50, 60], 'c': [70, 80, 90]},
                       index=['row4', 'row3', 'row2'])
    print df1 + df2

# --- Quiz ---
# Cumulative entries and exits for one station for a few hours.
# entries_and_exits = pd.DataFrame({
#     'ENTRIESn': [3144312, 3144335, 3144353, 3144424, 3144594,
#                  3144808, 3144895, 3144905, 3144941, 3145094],
#     'EXITSn': [1088151, 1088159, 1088177, 1088231, 1088275,
#                1088317, 1088328, 1088331, 1088420, 1088753]
# })
entries_and_exits = pd.DataFrame(
    {'ENTRIESn': [10, 40, 60, 65, 85], 'EXITSn': [0, 10, 20, 60, 60]},
    index=[0, 1, 2, 3, 4]
)

def get_hourly_entries_and_exits(entries_and_exits):
    return entries_and_exits.diff(periods=1, axis=0)
print get_hourly_entries_and_exits(entries_and_exits)