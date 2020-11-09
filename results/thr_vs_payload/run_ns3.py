from simulation import dcf_simulation
import numpy as np
import pandas as pd
import subprocess

N = 10  # number of contending stations
R = 10  # number of times simulation for each quantity of contending stations is repeated to get more probable results
cw_min = 15
cw_max = 1023


runs = [i + 1 for i in range(R)]
mac_paylaods = [i for i in range(100, 2304, 100)]


ns3_results = []

for r in runs:
    for payload in mac_paylaods:
        print(r, payload)
        stream = subprocess.check_output(
            f'cd ~/ns-allinone-3.31/ns-3.31/ && ./waf --run "scratch/80211a-performance --simulationTime=100 --nWifi={N} --payload={payload}" | tail -n 2',
            shell=True
        )

        results = stream.decode('utf-8').strip().split()
        thr = float(results[3])

        current_run = [r, payload, thr]
        ns3_results.append(current_run)

ns3_results_dt = pd.DataFrame(ns3_results, columns=[
    'run',
    'payload',
    'thr_ns3'
])

ns3_results_dt = ns3_results_dt.groupby(
    'payload')['thr_ns3'].mean().reset_index(name='thr_ns3')

ns3_results_dt.to_csv('results/thr_vs_payload/ns3.csv')
