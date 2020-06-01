from simulation import dcf_simulation
import csv
import matplotlib.pyplot as plt
import pandas as pd

N = 10 #number of contending stations
no_stations = [i + 1 for i in range(N)]

cw_min = 15
cw_max = 1023
#collision_probability = list(map(lambda n: dcf_simulation(n, cw_min, cw_max), no_stations))
collision_probability = [dcf_simulation(n, cw_min, cw_max) for n in no_stations]

validation_results = pd.read_csv(f'validation/results_validation_{cw_min}_{cw_max}.csv')
validation_p_coll = validation_results['p_coll'].tolist()

with open(f'results/simulation_results_{cw_min}_{cw_max}.csv', 'w', newline='') as results:
    results_writer = csv.writer(results)
    headers = ["N", "CWmin", "CWmax", "collision probability-simulation", "collision probability-model"]
    results_writer.writerow(headers)
    for result in range(N):
        row = [
            no_stations[result],
            cw_min,
            cw_max,
            collision_probability[result],
            validation_p_coll[result]]
        results_writer.writerow(row)

plt.plot(no_stations, collision_probability, 'ro', no_stations, validation_p_coll, 'bo')
plt.title(f"dcf simulation for cwmin={cw_min} and cwmax={cw_max}")
plt.xlabel('number of contending stations')
plt.ylabel('mean probability of collision')
plt.legend(['simulation', 'model'])
plt.savefig(f'results/graphs/simulation_result_{cw_min}_{cw_max}.png')