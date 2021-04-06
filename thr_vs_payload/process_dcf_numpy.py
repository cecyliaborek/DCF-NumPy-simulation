import pandas as pd
import sys
from helpers import conf_intervals

sys.path.append('helpers')

dcf_numpy_dt = pd.read_csv('thr_vs_payload/dcf_numpy_raw.csv')

# calculating confidance intervals
thr_yerr = conf_intervals.confidence_intervals(
    results=dcf_numpy_dt, field='DCF-NumPy_thr', key='payload')
# grouping the runs with the same payload
dcf_numpy_dt = dcf_numpy_dt.groupby(
    'payload')['DCF-NumPy_thr'].mean().reset_index(name='DCF-NumPy_thr')
# adding conf intervals as column
dcf_numpy_dt = dcf_numpy_dt.merge(
    thr_yerr, on='payload', suffixes=(
        '', '_conf'))

dcf_numpy_dt.to_csv('thr_vs_payload/dcf_numpy.csv', index=False)
