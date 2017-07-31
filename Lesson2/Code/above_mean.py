import pandas as pd
   
def variable_correlation(variable1, variable2):
    total = ((variable1 < variable1.mean()).astype(int) + (variable2 < variable2.mean()).astype(int))
    num_same_direction = len(total[total != 1])
    num_different_direction = len(total[total == 1])   
    return (num_same_direction, num_different_direction)

print variable_correlation(pd.Series([1, 2, 3, 4]), pd.Series([7, 6, 5, 4]))