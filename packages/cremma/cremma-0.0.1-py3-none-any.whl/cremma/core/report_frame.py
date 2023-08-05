

class Report():

    """
    Collection of metrics organized into a Pandas dataframe.

    Parameters
    ----------
    data : ndarray (structured or homogeneous), Iterable, dict, or DataFrame
        Dict can contain Series, arrays, constants, or list-like objects.
        .. versionchanged:: 0.23.0
           If data is a dict, column order follows insertion-order for
           Python 3.6 and later.

    See Also
    --------
    read_table : Read general delimited file into DataFrame.
    read_csv : Read a comma-separated values (csv) file into DataFrame.
    DataFrame.from_dict : From dicts of Series, arrays, or dicts.
        
    Examples
    --------
    Constructing DataFrame from a dictionary.
    >>> d = {'col1': [1, 2], 'col2': [3, 4]}
    return
    """

    def __init__(self, metrics=[], datasource=dict(), data=pd.DataFrame()):
        self.metrics = metrics
        self.datasource = datasource
        self.data = data
    
    def generate(self):
        for metric in self.metrics :
            pass
    