from simulation import dcf_simulation
import numpy as np
import pandas as pd

N = 10  # number of contending stations
R = 10  # number of times simulation for each quantity of contending stations is repeated to get more probable results
cw_min = 15
cw_max = 1023
payload = 1500


runs = [i + 1 for i in range(R)]
mcs_values = [0, 1, 2, 3, 4, 5, 6, 7]

# dict mapping mcs values to rates in Mbps
msc_rate = dict([(0, 6), (1, 9), (2, 12),
                 (3, 18), (4, 24), (5, 36), (6, 48), (7, 54)])

dcf_numpy_results = []

for mcs in mcs_values:
    for r in runs:
        current_run = [r, mcs]
        data_rate = msc_rate[mcs]
        run_results = dcf_simulation(
            N=N, cw_min=cw_min, cw_max=cw_max, seed=r, mac_payload=payload, data_rate=data_rate)
        current_run.append(run_results.network_throughput)
        dcf_numpy_results.append(current_run)

dcf_numpy_results = np.array(dcf_numpy_results)

dcf_numpy_dt = pd.DataFrame(dcf_numpy_results, columns=[
    'run', 'mcs', 'DCF-NumPy_thr'])
dcf_numpy_dt = dcf_numpy_dt.groupby(
    'mcs')['DCF-NumPy_thr'].mean().reset_index(name='DCF-NumPy_thr')

dcf_numpy_dt.to_csv('thr_vs_mcs/dcf_numpy.csv', index=False)
