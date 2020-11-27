import numpy as np
from simulation import dcf_simulation
import matplotlib.pyplot as plt
import pandas as pd
import statistics


N = 16  # number of contending stations
R = 10  # number of runs for each input parameters

# consecutive values of cw; cw_min=cw_max=cw
cw_values = [2 ** i for i in range(11)]
runs = [i + 1 for i in range(R)]

simulation_results = []

for r in runs:
    for cw in cw_values:
        current_run = [r, cw]
        run_results, _ = dcf_simulation(N=N, cw_min=cw, cw_max=cw, seed=r)
        current_run.append(run_results.network_throughput)
        simulation_results.append(current_run)

simulation_results = np.array(simulation_results)

simulation_results_dt = pd.DataFrame(simulation_results, columns=[
    'run',
    'cw',
    'throughput'
])

simulation_results_dt = simulation_results_dt.groupby(
    'cw')['throughput'].mean().reset_index(name='throughput')
simulation_results_dt['throughput'] = simulation_results_dt['throughput']

simulation_results_dt['throughput'] = simulation_results_dt['throughput'].div(1e6).round(4)


# throughput for default cw_min cw_max values
cw_min_default = 15
cw_max_default = 1023

default_results = []

for r in runs:
    results, _ = dcf_simulation(
        N=N, cw_min=cw_min_default, cw_max=cw_max_default, seed=r)
    default_results.append(results.network_throughput)

default_throughput = statistics.mean(default_results)
default_throughput = default_throughput/(1e6)

default_throughput_col = [default_throughput] * len(cw_values)
simulation_results_dt['default_thr'] = default_throughput_col

simulation_results_dt.to_csv('results/backoff_optimization_n16.csv')