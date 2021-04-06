import pandas as pd

col_needed = ['run', 'nWifi', 'CWmin', 'CWmax', 'pcWifi']
wifi_nr_results = pd.read_csv(
    '/home/cecylia/Documents/studies/thesis/validation/results_wifi_nr.csv',
    usecols=col_needed)


wifi_nr_results = wifi_nr_results.rename(columns={
    'nWifi': 'N',
    'CWmin': 'cw_min',
    'CWmax': 'cw_max',
    'pcWifi': 'p_coll_wifi_nr'
})


wifi_nr_results = wifi_nr_results.groupby([
    'N',
    'cw_min',
    'cw_max'
])['p_coll_wifi_nr'].mean().reset_index(name='p_coll_wifi_nr')

wifi_nr_results.to_csv(
    '/home/cecylia/Documents/studies/thesis/validation/results_wifi_nr_ready.csv')
