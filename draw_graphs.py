import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# configuration data: which results to show on graph
cw_min = 15
cw_max = 1023
N = 10 #number of contending stations
retry_limit = True
no_stations = [i + 1 for i in range(N)]

if retry_limit:
    retry = 'retry'
else:
    retry = 'no_retry'
final_results = pd.read_csv(f'results/final_results_{cw_min}_{cw_max}_{retry}.csv')

# calculation of MSE
MSE_model = np.square(np.subtract(final_results['p_coll_simulation'], final_results['p_coll_model'])).mean()
MSE_matlab = np.square(np.subtract(final_results['p_coll_simulation'], final_results['p_coll_matlab'])).mean()
MSE_model = np.round(MSE_model, decimals=10)
MSE_matlab = np.round(MSE_matlab, decimals=10)
print(MSE_model)
print(MSE_matlab)

plt.figure()
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
plt.title(f"dcf simulation for cwmin={cw_min} and cwmax={cw_max} \n {retry}")
plt.xlabel('number of contending stations')
plt.ylabel('mean probability of collision')
plt.legend(['simulation', 'model', 'matlab simulation'])
plt.figtext(0.6, 0.25, f'MSE model: {MSE_model}')
plt.figtext(0.6, 0.2, f'MSE matlab: {MSE_matlab}')
plt.savefig(f'results/graphs/simulation_result_{cw_min}_{cw_max}_{retry}.png')