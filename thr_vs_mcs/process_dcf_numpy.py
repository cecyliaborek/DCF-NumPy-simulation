import pandas as pd
import sys
from helpers import conf_intervals

sys.path.append('helpers')

dcf_numpy_dt = pd.read_csv('thr_vs_mcs/dcf_numpy_raw.csv')

# calculating confidance intervals
thr_yerr = conf_intervals.confidence_intervals(
    results=dcf_numpy_dt, field='DCF-NumPy_thr', key='mcs')
# grouping results with same mcs
dcf_numpy_dt = dcf_numpy_dt.groupby(
    'mcs')['DCF-NumPy_thr'].mean().reset_index(name='DCF-NumPy_thr')
# adding conf intervals to results
dcf_numpy_dt = dcf_numpy_dt.merge(thr_yerr, on='mcs', suffixes=('', '_conf'))

dcf_numpy_dt.to_csv('thr_vs_mcs/dcf_numpy.csv', index=False)
