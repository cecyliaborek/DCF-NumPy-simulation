from simulation import dcf_simulation
import numpy as np
import pandas as pd
import subprocess

N = 10  # number of contending stations
R = 10  # number of times simulation for each quantity of contending stations is repeated to get more probable results
cw_min = 15
cw_max = 1023
payload = 1500


runs = [i + 1 for i in range(R)]
mcs_values = [0, 1, 2, 3, 4, 5, 6, 7]


ns3_results = []

for r in runs:
    for mcs in mcs_values:
        print(r, mcs)
        stream = subprocess.check_output(
            f'cd ~/ns-allinone-3.31/ns-3.31/ && ./waf --run "scratch/80211a-performance --simulationTime=100 --nWifi={N} --payload={payload} --mcs={mcs}" | tail -n 3 | head -n 2',
            shell=True
        )

        results = stream.decode('utf-8').strip().split()
        thr = float(results[3])

        current_run = [r, mcs, thr]
        ns3_results.append(current_run)

ns3_results_dt = pd.DataFrame(ns3_results, columns=[
    'run',
    'mcs',
    'thr_ns3'
])

ns3_results_dt.to_csv('thr_vs_mcs/ns3_raw.csv')
