import scipy.stats as st
import numpy as np


def confidence_intervals(results, field, alpha=0.05):
    std = results.groupby('N').std().loc[:, field]
    n = results.groupby('N').count().loc[:, field]
    yerr = std / np.sqrt(n) * st.t.ppf(1-alpha/2, n - 1)
    return yerr