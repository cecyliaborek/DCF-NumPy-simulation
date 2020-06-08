import pandas as pd

col_needed = ['run', 'nWifi', 'CWmin', 'CWmax', 'pcWifi']
matlab_results = pd.read_csv('/home/cecylia/Documents/studies/thesis/validation/results_matlab.csv', usecols=col_needed)


matlab_results = matlab_results.rename(columns={
    'nWifi':'N',
    'CWmin':'cw_min',
    'CWmax':'cw_max',
    'pcWifi':'p_coll_matlab'
    })


matlab_results = matlab_results.groupby([
    'N',
    'cw_min',
    'cw_max'
    ])['p_coll_matlab'].mean().reset_index(name='p_coll_matlab')

matlab_results.to_csv('/home/cecylia/Documents/studies/thesis/validation/results_matlab_ready.csv')