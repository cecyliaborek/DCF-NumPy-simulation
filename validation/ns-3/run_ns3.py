import subprocess
import pandas as pd
import os

dir_path = os.path.dirname(os.path.realpath(
    __file__))  # directory of this script

# same data as for DCF-NumPy simulation
N = 10
R = 10
no_stations = [i + 1 for i in range(N)]
runs = [i + 1 for i in range(R)]

ns3_results = []

for n in no_stations:
    for r in runs:
        print(n, r)
        stream = subprocess.check_output(
            f'cd ~/ns-allinone-3.31/ns-3.31/ && ./waf --run "scratch/80211a-performance --RngRun={r} --simulationTime=10 --nWifi={n}" | tail -n 2',
            shell=True
        )

        results = stream.decode('utf-8').strip().split()
        thr = float(results[3])
        p_coll = float(results[-1])

        current_run = [n, r, thr, p_coll]
        ns3_results.append(current_run)

ns3_results_dt = pd.DataFrame(ns3_results, columns=[
    'N',
    'run',
    'thr_ns3',
    'p_coll_ns3'
])

ns3_results_dt.to_csv(f'{dir_path}/ns3_raw.csv')

