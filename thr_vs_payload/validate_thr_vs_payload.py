import pandas as pd

dcf_numpy_dt = pd.read_csv('thr_vs_payload/dcf_numpy.csv')
ns3_results_dt = pd.read_csv('thr_vs_payload/ns3.csv')

#selecting results for payload lower than 2300 (from this value fragemntation is done)
ns3_results_dt = ns3_results_dt.loc[ns3_results_dt['payload'] < 2300]

# dividing thr from dcf by 1e6 to receive results in Mb/s
dcf_numpy_dt['DCF-NumPy_thr'] = dcf_numpy_dt['DCF-NumPy_thr'].div(1e6)
#selecting results for payload lower than 2300 (from this value fragemntation is done)
dcf_numpy_dt = dcf_numpy_dt.loc[dcf_numpy_dt['payload'] < 2300]

combined_results = dcf_numpy_dt.merge(ns3_results_dt, on='payload')
combined_results.to_csv('results/thr_vs_payload.csv', index=False)
