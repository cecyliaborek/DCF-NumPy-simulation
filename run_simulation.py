from simulation import dcf_simulation
import csv
import matplotlib.pyplot as plt
import pandas as pd

N = 10 #number of contending stations
no_stations = [i + 1 for i in range(N)]

cw_min = 15
cw_max = 15
collision_probability = list(map(lambda n: dcf_simulation(n, cw_min, cw_max), no_stations))

validation_results = pd.read_csv('results/results_validation.csv')
validation_p_coll = validation_results['p_coll'].tolist()

with open('results/simulation_results.csv', 'w', newline='') as results:
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
plt.xlabel('number of contending stations')
plt.ylabel('mean probability of collision')
plt.legend(['simulation', 'model'])
plt.savefig('results/simulation_result.png')