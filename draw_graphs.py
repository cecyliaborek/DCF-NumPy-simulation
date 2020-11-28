import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from decimal import Decimal

# configuration data: which results to show on graph
cw_min = 15
cw_max = 1023
N = 10  # number of contending stations
retry_limit = True

if retry_limit:
    retry = 'retry'
else:
    retry = 'no_retry'
final_results = pd.read_csv(
    f'results/final_results_{cw_min}_{cw_max}_{retry}.csv')

# p_coll graph
# calculation of MSE
MSE_model = np.square(np.subtract(
    final_results['p_coll_simulation'], final_results['p_coll_model'])).mean()
MSE_matlab = np.square(np.subtract(
    final_results['p_coll_simulation'], final_results['p_coll_wifi_nr'])).mean()
MSE_ns3 = np.square(np.subtract(
    final_results['p_coll_simulation'], final_results['p_coll_ns3'])).mean()

plt.figure()
plt.plot(
    final_results['N'],
    final_results['p_coll_simulation'],
    'bo--',
    final_results['N'],
    final_results['p_coll_model'],
    'ro--',
    final_results['N'],
    final_results['p_coll_wifi_nr'],
    'yo--'
)
plt.errorbar(
    x=final_results['N'],
    y=final_results['p_coll_ns3'],
    yerr=final_results['ns3_p_coll_intervals'],
    capsize=6, marker='s',
    markersize=5,
    linestyle='dashed',
    color='c',
    mfc='c',
    mec='c'
)

# plt.title(
#    f"Mean probability of collision for cwmin={cw_min} and cwmax={cw_max} \n {retry}")
plt.xlabel('Number of Contending Stations')
plt.ylabel('Probability of Collision')
plt.legend(['DCF-NumPy', 'Analytical Model', 'Coexistance Model', 'ns-3'])
plt.figtext(0.50, 0.3, 'MSE:')
plt.figtext(0.50, 0.25, '* Analytical Model: %.4E' % Decimal(MSE_model))
plt.figtext(0.50, 0.2, '* Coexistance Model: %.4E' % Decimal(MSE_matlab))
plt.figtext(0.50, 0.15, '* ns-3: %.4E' % Decimal(MSE_ns3))
plt.savefig(f'results/graphs/p_coll_result_{cw_min}_{cw_max}_{retry}.pdf')

# throughput graph

MSE_ns3_thr = np.square(np.subtract(
    final_results['throughput_simulation'], final_results['thr_ns3'])).mean()

thr_sim = final_results['throughput_simulation']
sim_conf_intervals = final_results['throughput_simulation_conf']
n = final_results['N']
thr_ns3 = final_results['thr_ns3']
ns3_conf_intervals = final_results['ns3_thr_intervals']

fig = plt.figure()
plt.errorbar(x=n, y=thr_sim, yerr=sim_conf_intervals, capsize=6, marker='s',
             markersize=5, linestyle='dashed', color='b', mfc='b', mec='b')
plt.errorbar(x=n, y=thr_ns3, yerr=ns3_conf_intervals, capsize=6, marker='s',
             markersize=5, linestyle='dashed', color='c', mfc='c', mec='c')
# plt.title(
#    f"Throughput per station for cwmin={cw_min} and cwmax={cw_max} \n {retry}")
plt.xlabel('Number of Contending Stations')
plt.ylabel('Throughput [Mb/s]')
legend = plt.legend(['DCF-NumPy', 'ns-3'])

plt.text(8, 1, 'MSE: %.4E' % Decimal(MSE_ns3_thr))
plt.ylim(ymin=0, ymax=35)
plt.tight_layout()

plt.savefig(f'results/graphs/throughput_result_{cw_min}_{cw_max}_{retry}.pdf')


# throughput vs packet size graph

thr_vs_packet = pd.read_csv('results/thr_vs_payload.csv')

plt.figure()
plt.plot(
    thr_vs_packet['payload'],
    thr_vs_packet['DCF-NumPy_thr'],
    'bo--',
    thr_vs_packet['payload'],
    thr_vs_packet['thr_ns3'],
    'co--'
)

plt.xlabel('MAC Payload [B]')
plt.ylabel('Throughput [Mb/s]')
plt.legend(['DCF-NumPy', 'ns-3'])
plt.savefig(f'results/graphs/thr_vs_packet.pdf')

# throughput vs mcs graph

thr_vs_mcs = pd.read_csv('results/thr_vs_mcs.csv')

plt.figure()

x = thr_vs_mcs['mcs']

ax = plt.subplot(111)
offset = 0.3
ax.bar(x - offset/2, thr_vs_mcs['DCF-NumPy_thr'], width=offset, color='b')
ax.bar(x+offset/2, thr_vs_mcs['thr_ns3'], width=offset, color='c')

plt.xlabel('Modulation and coding scheme')
plt.ylabel('Throughput [Mb/s]')
plt.legend(['DCF-NumPy', 'ns-3'])
plt.savefig(f'results/graphs/thr_vs_mcs.pdf')


# backoff optimization
optimization_throughput = pd.read_csv('results/backoff_optimization_n16.csv')
cw_values = optimization_throughput['cw']
default_thr = optimization_throughput['default_thr'][1]

plt.figure()
plt.plot(
    cw_values,
    optimization_throughput['throughput'],
    'bo--')
plt.axhline(y=default_thr, color='r', linestyle='--')

plt.xlabel('CW values')
plt.ylabel('Throughput [Mb/s]')
#plt.legend('')

plt.savefig(f'results/graphs/backoff_optimization.pdf')
