import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from decimal import Decimal

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

# p_coll graph
# calculation of MSE
MSE_model = np.square(np.subtract(final_results['p_coll_simulation'], final_results['p_coll_model'])).mean()
MSE_matlab = np.square(np.subtract(final_results['p_coll_simulation'], final_results['p_coll_matlab'])).mean()
MSE_ns3 = np.square(np.subtract(final_results['p_coll_simulation'], final_results['p_coll_ns3'])).mean()
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
    'yo',
    no_stations,
    final_results['p_coll_ns3'],
    'co'
    )

plt.title(f"mean probability of collision for cwmin={cw_min} and cwmax={cw_max} \n {retry}")
plt.xlabel('number of contending stations')
plt.ylabel('mean probability of collision')
plt.legend(['simulation', 'model', 'matlab simulation', 'ns3'])
plt.figtext(0.6, 0.25, 'MSE model: %.4E' % Decimal(MSE_model))
plt.figtext(0.6, 0.2, 'MSE matlab: %.4E' % Decimal(MSE_matlab))
plt.figtext(0.6, 0.15, 'MSE ns3: %.4E' % Decimal(MSE_ns3))
plt.savefig(f'results/graphs/p_coll_result_{cw_min}_{cw_max}_{retry}.png')

#throughput graph

MSE_ns3_thr = np.square(np.subtract(final_results['throughput_simulation'], final_results['thr_ns3'])).mean()

plt.figure()
plt.plot(
    no_stations,
    final_results['throughput_simulation'],
    'bo',
    no_stations,
    final_results['thr_ns3'],
    'ro'
    )
plt.title(f"throughput per station for cwmin={cw_min} and cwmax={cw_max} \n {retry}")
plt.xlabel('number of contending stations')
plt.ylabel('throughput [Mb/s]')
plt.legend(['simulation', 'ns3'])
plt.figtext(0.6, 0.5, 'MSE ns3: %.4E' % Decimal(MSE_ns3_thr))
plt.savefig(f'results/graphs/throughput_result_{cw_min}_{cw_max}_{retry}.png')