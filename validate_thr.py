import pandas as pd
from simulation import dcf_simulation
import numpy as np
import subprocess
import matplotlib.pyplot as plt

# parameters
cw_min = 0
cw_max = 0
N = 1
runs = [i + 1 for i in range(10)]

# running dcf NumPy simulation to get results for given parameters
dcf_numpy_thr = dcf_simulation(
    N=N, cw_min=cw_min, cw_max=cw_max, seed=1).network_throughput
#convertinh into Mbps
dcf_numpy_thr = dcf_numpy_thr/(1e6)

# running ns-3 simulation to get results for given parameter
stream = subprocess.check_output(
    f'cd ~/ns-allinone-3.31/ns-3.31/ && ./waf --run "scratch/80211a-performance --cwMin={cw_min} --cwMax={cw_max} --simulationTime=10 --nWifi={N}" | tail -n 2',
    shell=True
)
results = stream.decode('utf-8').strip().split()
print(results)
ns3_thr = float(results[3])

# matlab IEEE_802_11a.m simulator
matlab_thr = 34.601371204701266

results = (dcf_numpy_thr, ns3_thr, matlab_thr)

#throughput bar graph
y_pos = np.arange(len(results))
labels = ('Dcf NumPy', 'Ns-3', 'Matlab 802_11_a.m')

plt.bar(y_pos, results, align='center')
plt.xticks(y_pos, labels)
plt.ylabel('Throughput [Mbps]')
plt.title(f'Throuhput comparison for CWmin={cw_min}, CWmax={cw_max}, N={N}')
plt.savefig('results/graphs/thr_comparision.png')