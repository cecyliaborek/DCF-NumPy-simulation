import pandas as pd

dcf_numpy_dt = pd.read_csv('thr_vs_mcs/dcf_numpy.csv')
ns3_results_dt = pd.read_csv('thr_vs_mcs/ns3.csv')

# dividing thr from dcf by 1e6 to receive results in Mb/s
dcf_numpy_dt['DCF-NumPy_thr'] = dcf_numpy_dt['DCF-NumPy_thr'].div(1e6)


combined_results = dcf_numpy_dt.merge(ns3_results_dt, on='mcs')
combined_results.to_csv('results/thr_vs_mcs.csv', index=False)
