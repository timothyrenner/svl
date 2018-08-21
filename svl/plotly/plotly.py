from toolz import merge


def plotly_histogram(svl_plot, data):
    """ Transforms an svl plot and dataset into a plotly dict.

        Parameters
        ----------
        svl_plot : dict
            The SVL plot as produced from the parser.

        data : dict
            The dataset built from the data module.

        Returns
        -------
        dict
            A plotly histogram of the dataset.
    """

    trace = {
        "type": "histogram",
        "x": data[svl_plot["field"]]
    }

    if "step" in svl_plot:
        # Set the bins - note this might require another pass over the dataset
        # if the start / end args are required. If that's the case it might be
        # possible to add it to the aggregator in data.py.
        bins = {"xbins": {"size": svl_plot["step"]}}
    elif "bins" in svl_plot:
        # Set the number of bins.
        bins = {"nbinsx": svl_plot["bins"]}
    else:
        # Activate autobins.
        bins = {"autobinx": True}

    return [merge(trace, bins)]


def plotly_bar(svl_plot, data):
    pass  # TODO: Implement.


def plotly_line(svl_plot, data):
    pass  # TODO: Implement.


def plotly_scatter(svl_plot, data):
    pass  # TODO: Implement.


def plotly_boxplot(svl_plot, data):
    pass  # TODO: Implement.
