from simulation import dcf_simulation
import csv

N = 10
no_stations = [i + 1 for i in range(N)]

cw_min = 16
cw_max = 16
collision_probability = list(map(lambda n: dcf_simulation(n, cw_min, cw_max), no_stations))

with open('simulation_results.csv', 'w', newline='') as results:
    results_writer = csv.writer(results)
    headers = ["N", "CWmin", "CWmax", "collision probability"]
    results_writer.writerow(headers)
    for result in range(N):
        row = [no_stations[result], cw_min, cw_max, collision_probability[result]]
        results_writer.writerow(row)