from toolz import merge, compose, pluck
from jinja2 import Environment, PackageLoader, select_autoescape

listpluck = compose(list, pluck)


def _extract_trace_data(svl_field_x, svl_field_y, data):
    """ Extracts the data required for the x and y fields from the SVL data
        and converts them into an {"x": [ .. ], "y": [ .. ]} dict for
        plotly.

        Parameters
        ----------
        svl_field_x : dict
            The SVL specifier for the x field.
        svl_field_y : dict
            The SVL specifier for the y field.
        data : dict
            The SVL data.

        Returns
        -------
        dict
            A dictionary with an "x" and "y" field that maps to a list, ready
            to be put into a plotly trace.
    """
    x = []
    y = []

    if "agg" in svl_field_x:
        # If there's an agg in x, then the dataset's a dict with y as the
        # keys and x as the values.
        # TODO: Might want to ditch the sort and use an OrderedDict as the
        # data container.
        for group_val in sorted(data.keys()):
            x.append(data[group_val])
            y.append(group_val)
    elif "agg" in svl_field_y:
        # If there's an agg in y, then the dataset's a dict with x as the keys
        # and y as the values.
        for group_val in sorted(data.keys()):
            x.append(group_val)
            y.append(data[group_val])
    else:
        # If there's an agg in neither then this is simpler.
        x = data[svl_field_x["field"]]
        y = data[svl_field_y["field"]]

    return {"x": x, "y": y}


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
        # Set the bin size.
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


PLOTLY_PLOTS = {
    "histogram": plotly_histogram,
    "bar": plotly_bar,
    "line": plotly_line,
    "scatter": plotly_scatter,
    "boxplot": plotly_boxplot
}


def plotly_template_vars(svl_plots, datas):
    """ Constructs the variables needed for the plotly template from the
        SVL plots and their associated data values.

        Parameters
        ----------
        svl_plots : list
            A list of dicts defining the SVL plots in the format produced by
            the layout module.
        datas : list
            A list of dicts defining the data required for each plot in the
            format produced by the data module.

        Returns
        -------
        dict
            A dictionary of the keyword arguments required to render the plotly
            template. Specifically, num_rows, num_columns, and plots, which
            contain (respectively) the number of grid rows, the number of grid
            columns, and the plotly plots.
    """
    num_rows = max(listpluck("row_end", svl_plots)) - 1
    num_columns = max(listpluck("column_end", svl_plots)) - 1

    plots = [
        {
            "row_start": plot["row_start"],
            "row_end": plot["row_end"],
            "column_start": plot["column_start"],
            "column_end": plot["column_end"],
            "plotly": PLOTLY_PLOTS[plot["type"]](plot, data)
        } for plot, data in zip(svl_plots, datas)
    ]

    return {
        "num_rows": num_rows,
        "num_columns": num_columns,
        "plots": plots
    }


def plotly_template():
    """ Obtains the template for plotly plots.

        Returns
        -------
        `jinja2.Template`
            The tempate for plotly plots.
    """
    env = Environment(
        loader=PackageLoader("svl.plotly", "templates"),
        autoescape=select_autoescape(["html"])
    )

    return env.get_template("index.jinja")
