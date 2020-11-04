from simulation import transmission_time
import numpy as np
import matplotlib.pyplot as plt

data_rate = 54
control_rate = 6
mac_payload = 1500

# DCF-NumPy simulation frame time: getting second result, which is frame time in s
dcf_numpy_time = transmission_time(backoff_slots=0, data_rate=data_rate,
                                   control_rate=control_rate, mac_payload=mac_payload, collision=False)['frame_time']

# AirTime calculator frame time (returns results in microseconds):
air_time_calc_time = 252e-6
# matlab IEEE_802_11_a simulation frame time:
matlab_802_11_time = 0.000252000000000000
#ns-3 frame duration
ns3_time = 248e-6


frame_times = (dcf_numpy_time, matlab_802_11_time, air_time_calc_time, ns3_time)

y_pos = np.arange(len(frame_times))
labels = ('Dcf-NumPy', 'Frame Duration\nMatlab Model', 'AirTime\nCalculator', 'ns-3')

fig, ax = plt.subplots()

rects = plt.bar(y_pos, frame_times, align='center')
plt.xticks(y_pos, labels)
plt.ylabel('Air time [s]')
ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))

plt.savefig('results/graphs/frame_time_comparison.pdf')