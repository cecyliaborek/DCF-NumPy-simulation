import pandas as pd

# configuration data of the simulation
N = 10  # number of contending stations
R = 10  # number of times simulation for each quantity of contending stations is repeated to get more probable results
cw_min = 15
cw_max = 1023
retry_limit = True

if retry_limit:
    retry = 'retry'
else:
    retry = 'no_retry'

# simulation results
simulation_results = pd.read_csv(
    f'results/simulation_results_{cw_min}_{cw_max}_{retry}.csv',
    index_col=False)

# extracting probability of collision from results of model calculation
model_results = pd.read_csv(f'validation/results_model_{cw_min}_{cw_max}.csv')
model_p_coll = model_results[['N', 'p_coll']]
model_p_coll.columns = ['N', 'p_coll_model']

# extracting probability of collision from results of matlab wifi_nr_model
# simulation
wifi_nr_results = pd.read_csv('validation/results_wifi_nr_ready.csv')
wifi_nr_p_coll = wifi_nr_results[['N', 'p_coll_wifi_nr']]

# adding results from ns3 simulator
ns3_results = pd.read_csv('validation/ns-3/ns3_results.csv', index_col=False)
ns3_results = ns3_results[['N', 'p_coll_ns3', 'thr_ns3',
                           'ns3_thr_intervals', 'ns3_p_coll_intervals']]


# adding results from ns3 release 32
ns3_results_r32 = pd.read_csv(
    'validation/ns-3/ns3_results_r32.csv', index_col=False)
ns3_results_r32 = ns3_results_r32[[
    'N', 'p_coll_ns3_r32', 'thr_ns3_r32', 'ns3_conf_intervals_r32']]

# merging the simulation, model, wifi_nr and ns3 results
final_results = simulation_results.merge(model_p_coll, on='N')
final_results = final_results.merge(wifi_nr_p_coll, on='N')
final_results = final_results.merge(ns3_results, on='N')
final_results = final_results.merge(ns3_results_r32, on='N')

# saving results as csv file
final_results.to_csv(
    f'results/final_results_{cw_min}_{cw_max}_{retry}.csv', index=False)
