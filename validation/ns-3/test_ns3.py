import pandas as pd
import conf_intervals
import os


def delete_anomallies(results, column):
    """Deletes anomallies from dataframe, i.e. deltes the runs where result values equals 0

    Args:
        results (pandas.df): dataframe with results where anomallies may occur
        column (string): name of column in df where anomallies should be deleted
        returns (pandas.df): dataframe with results without 0 values in specified column
    """
    results_no_anomallies = results.drop(
        results[results[column] == 0].index)

    return results_no_anomallies


ns3_results_dt = pd.read_csv(
    '/home/cecylia/Documents/studies/thesis/validation/ns-3/ns3_raw.csv')

ns3_results_dt = delete_anomallies(ns3_results_dt, 'thr_ns3')
# calculating the confidence intervals for throughput results
ns3_conf_intervals = conf_intervals.confidence_intervals(
    ns3_results_dt, 'thr_ns3')

# gruping the results with same N and calculating mean value for each N
mean_ns3_results = ns3_results_dt.groupby(
    'N')[['thr_ns3', 'p_coll_ns3']].mean()
mean_ns3_results.columns = ['thr_ns3', 'p_coll_ns3']
mean_ns3_results = mean_ns3_results.reset_index()

# adding confidence intervals as column to results
mean_ns3_results['ns3_conf_intervals'] = ns3_conf_intervals

dir_path = os.path.dirname(os.path.realpath(__file__))

mean_ns3_results.to_csv(f'{dir_path}/ns3_results.csv', index=False)
