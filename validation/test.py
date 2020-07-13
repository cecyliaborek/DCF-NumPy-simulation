import subprocess
import os
import pandas as pd





data = {'n': [1, 2, 2, 3, 3, 4, 5, 6, 7], 'l': [2, 3,6, 7, 6, 4, 2, 3, 6],'o' : [3, 4, 5, 6, 5, 8, 9, 1, 2]}
dt = pd.DataFrame(data)

grouped = dt.groupby('n')[['l', 'o']].mean()

grouped.columns = ['l', 'o']
grouped = grouped.reset_index(0)

print(grouped)