from simulation import dcf_simulation
import pandas as pd


# configuration data for simulation
N = 10 #number of contending stations
cw_min = 15
cw_max = 1023
retry_limit = True

no_stations = [i + 1 for i in range(N)]
runs = [i + 1 for i in range(10)]
if retry_limit:
    retry = 'retry'
else:
    retry = 'no_retry'

collision_probability = [[r, n, cw_min, cw_max, dcf_simulation(n, cw_min, cw_max, r)] for n in no_stations for r in runs]

simulation_results = pd.DataFrame(collision_probability, columns=[
    'run',
    'N',
    'cw_min',
    'cw_max',
    'p_coll_simulation'
])

validation_results = pd.read_csv(f'validation/results_validation_{cw_min}_{cw_max}.csv')
validation_p_coll = validation_results[['N', 'p_coll']]

matlab_results = pd.read_csv('validation/results_matlab_ready.csv')
p_coll_matlab = matlab_results[['N', 'p_coll_matlab']]

simulation_results = simulation_results.merge(validation_p_coll, on='N')
simulation_results = simulation_results.rename(columns={'p_coll':'p_coll_model'})

simulation_results.to_csv(f'results/simulation_results_{cw_min}_{cw_max}_{retry}.csv')

final_results = simulation_results.groupby([
    'N',
    'cw_min',
    'cw_max',
    'p_coll_model'
    ])['p_coll_simulation'].mean().reset_index(name='p_coll_simulation')

final_results = final_results.merge(p_coll_matlab, on='N')

final_results.to_csv(f'results/final_results_{cw_min}_{cw_max}_{retry}.csv')
