from simulation import dcf_simulation
import pandas as pd
import numpy as np


# configuration data for simulation
N = 10 #number of contending stations
R = 10 #number of times simulation for each quantity of contending stations is repeated to get more probable results
cw_min = 15
cw_max = 1023
retry_limit = True #

# creating lists with number of contending stations and run numbers  
no_stations = [i + 1 for i in range(N)]
runs = [i + 1 for i in range(R)]
if retry_limit:
    retry = 'retry'
else:
    retry = 'no_retry'

# running the simulation on defined variables
simulation_results = []

for n in no_stations:
    for r in runs:
        current_run = [r, n, cw_min, cw_max]
        run_results = dcf_simulation(N=n, cw_min=cw_min, cw_max=cw_max, seed=r, mac_payload=1472)
        current_run.extend([
            run_results.mean_collision_probability,
            run_results.network_throughput])
        simulation_results.append(current_run)

simulation_results = np.array(simulation_results)

# probability of collision results
p_coll_results = pd.DataFrame(np.delete(simulation_results, -1, axis=1), columns=[
    'run',
    'N',
    'cw_min',
    'cw_max',
    'p_coll_simulation'
])

# grouping the results by the same value of N and calculating the mean of probability of collision for each N
p_coll_results = p_coll_results.groupby([
    'N',
    'cw_min',
    'cw_max'
    ])['p_coll_simulation'].mean().reset_index(name='p_coll_simulation')

#throughput results
throughput_results = pd.DataFrame(np.delete(simulation_results, -2, axis=1), columns=[
    'run',
    'N',
    'cw_min',
    'cw_max',
    'throughput_simulation'
])

#grouping the results with the same N and calculating mean throughput for each N
throughput_results = throughput_results.groupby([
    'N',
    'cw_min',
    'cw_max'
])['throughput_simulation'].mean().reset_index(name='throughput_simulation')

#converting the throughput into Mbits/s
throughput_results['throughput_simulation'] = throughput_results['throughput_simulation'].div(1e6).round(4)

#merging averege results of throughput and p_coll and saving as simulation results
dcf_simulation_results = pd.merge(p_coll_results, throughput_results, on=['N', 'cw_min', 'cw_max'])
dcf_simulation_results.to_csv(f'results/simulation_results_{cw_min}_{cw_max}_{retry}.csv', index=False)
