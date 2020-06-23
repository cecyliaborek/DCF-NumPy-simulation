from simulation import dcf_simulation
import matplotlib.pyplot as plt
import pandas as pd

N = 10 #number of contending stations
no_stations = [i + 1 for i in range(N)]
runs = [i+1 for i in range(10)]

cw_min = 15
cw_max = 1023

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

simulation_results.to_csv(f'results/simulation_results_{cw_min}_{cw_max}.csv')

final_results = simulation_results.groupby([
    'N',
    'cw_min',
    'cw_max',
    'p_coll_model'
    ])['p_coll_simulation'].mean().reset_index(name='p_coll_simulation')

final_results = final_results.merge(p_coll_matlab, on='N')

final_results.to_csv(f'results/final_results_{cw_min}_{cw_max}.csv')

plt.plot(
    no_stations,
    final_results['p_coll_simulation'],
    'bo',
    no_stations,
    final_results['p_coll_model'],
    'ro',
    no_stations,
    final_results['p_coll_matlab'],
    'go'
    )
plt.title(f"dcf simulation for cwmin={cw_min} and cwmax={cw_max}")
plt.xlabel('number of contending stations')
plt.ylabel('mean probability of collision')
plt.legend(['simulation', 'model', 'matlab simulation'])
plt.savefig(f'results/graphs/simulation_result_{cw_min}_{cw_max}.png')