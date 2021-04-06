from simulation import dcf_simulation
import numpy as np
import pandas as pd

N = 10  # number of contending stations
R = 10  # number of times simulation for each quantity of contending stations is repeated to get more probable results
cw_min = 15
cw_max = 1023


runs = [i + 1 for i in range(R)]
mac_paylaods = [i for i in range(100, 2304, 100)]

dcf_numpy_results = []

for paylaod in mac_paylaods:
    for r in runs:
        current_run = [r, paylaod]
        run_results = dcf_simulation(
            N=N,
            cw_min=cw_min,
            cw_max=cw_max,
            seed=r,
            mac_payload=paylaod,
            control_rate=24,
            data_rate=54)
        current_run.append(run_results.network_throughput)
        dcf_numpy_results.append(current_run)

dcf_numpy_results = np.array(dcf_numpy_results)

# creating a pandas data frame from list
dcf_numpy_dt = pd.DataFrame(dcf_numpy_results, columns=[
    'run', 'payload', 'DCF-NumPy_thr'])

dcf_numpy_dt.to_csv('thr_vs_payload/dcf_numpy_raw.csv', index=False)
