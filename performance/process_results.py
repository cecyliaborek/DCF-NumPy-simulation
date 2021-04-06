import pandas as pd

# ns3

ns3_results = []
with open('performance/ns3_times.txt') as ns3_txt:
    for line in ns3_txt:
        file_results = line.split()
        if len(file_results) == 0 or file_results[0] != 'real':
            continue
        ns3_results.append(file_results[1])


for idx, result in enumerate(ns3_results):
    mins = result[:2]
    secs = result[3:-1]
    result_secs = float(mins) * 60 + float(secs)
    ns3_results[idx] = result_secs

# dcf_numpy

dcf_numpy_results = []
with open('performance/dcf_numpy_times.txt') as dcf_txt:
    for line in dcf_txt:
        file_results = line.split()
        if len(file_results) == 0 or file_results[0] != 'real':
            continue
        dcf_numpy_results.append(file_results[1])


for idx, result in enumerate(dcf_numpy_results):
    mins = result[:1]
    secs = result[2:-1]
    result_secs = float(mins) * 60 + float(secs)
    dcf_numpy_results[idx] = result_secs

params = [1] * 10

combined_times = pd.DataFrame(list(zip(params, dcf_numpy_results, ns3_results)), columns=[
                              'params', 'DCF-NumPy', 'ns-3'])

combined_times.to_csv('performance/times_2.csv', index=False)
