import numpy as np
from simulation import dcf_simulation
import matplotlib.pyplot as plt


N = 10 # number of stations
cw_min = 15
cw_max = 1023

# getting all selected backoff values in one simulation run of DCF-NumPy
_, _, backoffs = dcf_simulation(N=N, cw_min=cw_min, cw_max=cw_max, seed=1, debug=True)

backoff_bins = [0] + [2 ** i for i in range(4, 11, 1)]
backoff_hist, _ = np.histogram(backoffs, backoff_bins)

plt.figure()

x = np.arange(1, len(backoff_bins))
plt.bar(x, backoff_hist, align='edge', width=-1.0)
plt.xticks(x, backoff_bins[1:])
plt.xlabel('Selected backoff')
plt.ylabel('Number of occurances')

plt.savefig('results/graphs/backoff_hist.pdf')