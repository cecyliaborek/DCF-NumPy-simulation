def delete_zeroes(results, column):
    """Deletes anomallies from dataframe, i.e. deletes the runs where result values equals 0

    Args:
        results (pandas.df): dataframe with results where anomallies may occur
        column (string): name of column in df where anomallies should be deleted
        returns (pandas.df): dataframe with results without 0 values in specified column
    """
    results_no_anomallies = results.drop(
        results[results[column] == 0].index)

    return results_no_anomallies