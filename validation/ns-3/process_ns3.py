import pandas as pd
import delete_anomallies
from helpers import conf_intervals
import os

dir_path = os.path.dirname(os.path.realpath(
    __file__))  # directory of this script

ns3_results_dt = pd.read_csv(f'{dir_path}/ns3_raw.csv')

# deleting anomallies i.e. runs where thr was equal to 0
ns3_results_dt = delete_anomallies.delete_zeroes(ns3_results_dt, 'thr_ns3')

# calculating the confidence intervals for throughput results
ns3_thr_intervals = conf_intervals.confidence_intervals(
    ns3_results_dt, 'thr_ns3')

# calculating the confidence intervals for p_coll results
ns3_p_coll_intervals = conf_intervals.confidence_intervals(
    ns3_results_dt, 'p_coll_ns3')

# gruping the results with same N and calculating mean value for each N
mean_ns3_results = ns3_results_dt.groupby(
    'N')[['thr_ns3', 'p_coll_ns3']].mean()
mean_ns3_results.columns = ['thr_ns3', 'p_coll_ns3']
mean_ns3_results = mean_ns3_results.reset_index()

# adding confidence intervals as column to results
mean_ns3_results['ns3_thr_intervals'] = ns3_thr_intervals
mean_ns3_results['ns3_p_coll_intervals'] = ns3_p_coll_intervals

# saving results in the same directory as this script
mean_ns3_results.to_csv(f'{dir_path}/ns3_results.csv', index=False)
