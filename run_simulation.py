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
        run_results = dcf_simulation(n, cw_min, cw_max, r)
        current_run.extend([
            run_results.mean_collision_probability,
            run_results.mean_throughput])
        simulation_results.append(current_run)

simulation_results = np.array(simulation_results)

# probability of collision validation
p_coll_results = pd.DataFrame(np.delete(simulation_results, -1, axis=1), columns=[
    'run',
    'N',
    'cw_min',
    'cw_max',
    'p_coll_simulation'
])

# extracting probability of collision from results of model calculation
validation_results = pd.read_csv(f'validation/results_validation_{cw_min}_{cw_max}.csv')
validation_p_coll = validation_results[['N', 'p_coll']]

#extracting probability of collision from results of matlab wifi_nr_model simulation
matlab_results = pd.read_csv('validation/results_matlab_ready.csv')
p_coll_matlab = matlab_results[['N', 'p_coll_matlab']]

#merging the simulation and model results
p_coll_results = p_coll_results.merge(validation_p_coll, on='N')
p_coll_results = p_coll_results.rename(columns={'p_coll':'p_coll_model'})

p_coll_results.to_csv(f'results/simulation_results_{cw_min}_{cw_max}_{retry}.csv')

# grouping the results by the same value of N and calculating the mean of probability of collision for each N
final_p_coll_results = p_coll_results.groupby([
    'N',
    'cw_min',
    'cw_max',
    'p_coll_model'
    ])['p_coll_simulation'].mean().reset_index(name='p_coll_simulation')

#merging matlab results
final_p_coll_results = final_p_coll_results.merge(p_coll_matlab, on='N')

# throughput validation
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

#merging throughput to the final results
final_results = final_p_coll_results.merge(throughput_results, on=['N', 'cw_min', 'cw_max'])

#saving results as csv file
final_results.to_csv(f'results/final_results_{cw_min}_{cw_max}_{retry}.csv')
