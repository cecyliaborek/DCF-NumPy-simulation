import pandas as pd


ns3_results_anomallies = pd.read_csv('./ns3_raw_anomallies.csv')

# deleting values where thr equals 0 - anomally
ns3_results_anomallies = ns3_results_anomallies.drop(
    ns3_results_anomallies[ns3_results_anomallies.thr_ns3 == 0].index)

mean_ns3_results_anomallies = ns3_results_anomallies.groupby(
    'N')[['thr_ns3', 'p_coll_ns3']].mean()
mean_ns3_results_anomallies.columns = ['thr_ns3', 'p_coll_ns3']
mean_ns3_results_anomallies = mean_ns3_results_anomallies.reset_index()



mean_ns3_results_anomallies.set_index('N', inplace=True)

mean_ns3_results_anomallies.to_csv(
    './ns3_results_anomallies.csv')

# replacing the values in ns3_results with the ones where anomallies where deleted
ns3_results = pd.read_csv('./ns3_results.csv')

anomallies = mean_ns3_results_anomallies.index.tolist()

for n in anomallies:
    print(n)
    ns3_results.loc[(ns3_results.N == n), 'thr_ns3'] = mean_ns3_results_anomallies.at[n, 'thr_ns3']
    print(ns3_results_anomallies.iloc[8]['p_coll_ns3'])
    ns3_results.loc[(ns3_results.N == n), 'p_coll_ns3'] = mean_ns3_results_anomallies.at[n, 'p_coll_ns3']

ns3_results.to_csv('./ns3_results.csv', index=False)