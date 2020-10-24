from simulation import transmission_time
import numpy as np
import matplotlib.pyplot as plt

# script to compare 802.11 transmission time and display results on graph

data_rate = 54
control_rate = 6
mac_payload = 1472
slot_time = 9e-6

# DCF-NumPy simulation tx time: transmission_time() * slot_time as transmission_time() returns number of slots
dcf_numpy_time = transmission_time(backoff_slots=0, data_rate=data_rate,
                                   control_rate=control_rate, mac_payload=mac_payload, collision=False) * slot_time
# matlab IEEE_802_11_a simulation tx time:
matlab_802_11_time = 0.000340333333333333
# AirTime calculator tx time (returns results in microseconds):
air_time_calc_time = 347.2e-6

print(dcf_numpy_time)
print(air_time_calc_time)

air_times = (dcf_numpy_time, matlab_802_11_time, air_time_calc_time)

y_pos = np.arange(len(air_times))
labels = ('IEEE_802_11_a', 'Dcf-NumPy', 'AirTime Calculator')

fig, ax = plt.subplots()

rects = plt.bar(y_pos, air_times, align='center')
plt.xticks(y_pos, labels)
plt.ylabel('Air time [s]')
ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))

plt.savefig('results/graphs/air_time_comparison.pdf')