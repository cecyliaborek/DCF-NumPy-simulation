import pandas as pd
import sys
import numpy as np
from helpers import conf_intervals
import matplotlib.pyplot as plt

sys.path.append('helpers')

times = pd.read_csv('performance/times.csv')

ns3_yerr = conf_intervals.confidence_intervals(
    results=times, field='ns-3', key='params')[1]
dcf_numpy_yerr = conf_intervals.confidence_intervals(
    results=times, field='DCF-NumPy', key='params')[1]

ns3_time = times.groupby('params')['ns-3'].mean()[1]
dcf_numpy_time = times.groupby('params')['DCF-NumPy'].mean()[1]

final_times = [ns3_time, dcf_numpy_time]
conf_int = [ns3_yerr, dcf_numpy_yerr]

x = np.arange(len(final_times))
labels = ['ns-3', 'DCF-NumPy']

print(final_times)

plt.figure()

ax = plt.subplot(111)
ax.bar(x, final_times, yerr=conf_int, capsize=14)
plt.xticks(x, labels)
plt.ylabel('Execution time [s]')

plt.savefig('results/graphs/performance.pdf')
