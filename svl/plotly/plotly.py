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


def _extract_all_traces(svl_plot, data):
    """ Extracts the traces for the SVL plot from the SVL data.

        Parameters
        ---------
        svl_plot : dict
            The SVL plot.

        data : dict
            The SVL data.

        Returns
        -------
        list
            A list of {"x": [ .. ], "y": [ .. ]} style dictionaries to be used
            as traces in plotly plots.
    """
    svl_field_x = svl_plot["x"]
    svl_field_y = svl_plot["y"]

    if "color" not in svl_plot:
        return [_extract_trace_data(svl_field_x, svl_field_y, data)]
    else:
        return [
            _extract_trace_data(svl_field_x, svl_field_y, data[color])
            for color in sorted(data.keys())  # TODO: Eliminate sorted.
        ]


def plotly_histogram(svl_plot, data):
    """ Transforms an svl plot and dataset into a plotly histogram.

        Parameters
        ----------
        svl_plot : dict
            The SVL plot as produced from the parser.

        data : dict
            The dataset built from the data module.

        Returns
        -------
        dict
            A plotly dict defining the histogram.
    """

    trace = {
        "type": "histogram",
        "x": data[svl_plot["field"]]
    }
    layout = {}

    if "step" in svl_plot:
        # Set the bin size.
        bins = {"xbins": {"size": svl_plot["step"]}}
    elif "bins" in svl_plot:
        # Set the number of bins.
        bins = {"nbinsx": svl_plot["bins"]}
    else:
        # Activate autobins.
        bins = {"autobinx": True}

    return {
        "layout": layout,
        "data": [merge(trace, bins)]
    }


def plotly_bar(svl_plot, data):
    """ Creates a plotly bar chart from the SVL plot and data specs.

        Parameters
        ----------
        svl_plot : dict
            The SVL plot specifier.

        data : dict
            The SVL data specifier.

        Returns
        -------
        dict
            The dictionary defining the plotly plot.
    """

    plot_type = {"type": "bar"}
    layout = {}
    raw_traces = _extract_all_traces(svl_plot, data)

    if "color" in svl_plot:
        layout = {"barmode": "group"}
        traces = [
            merge(plot_type, {"name": color}, trace)
            # NOTE: Danger!! Implicit coupling to order here.
            for color, trace in zip(sorted(data.keys()), raw_traces)
        ]
    else:
        traces = [
            merge(plot_type, trace)
            for trace in raw_traces
        ]

    return {
        "layout": layout,
        "data": traces
    }


def plotly_line(svl_plot, data):
    """ Creates a plotly line chart from the SVL plot and data specs.

        Parameters
        ----------
        svl_plot : dict
            The SVL plot specifier.

        data : dict
            The SVL data specifier.

        Returns
        -------
        dict
            The dictionary defining the plotly plot.
    """

    plot_type = {"mode": "lines+markers", "type": "scatter"}

    layout = {}
    raw_traces = _extract_all_traces(svl_plot, data)

    if "color" in svl_plot:
        traces = [
            merge(plot_type, {"name": color}, trace)
            # NOTE: Danger!! Implicit coupling to order here.
            for color, trace in zip(sorted(data.keys()), raw_traces)
        ]
    else:
        traces = [
            merge(plot_type, trace)
            for trace in raw_traces
        ]

    return {
        "layout": layout,
        "data": traces
    }


def plotly_scatter(svl_plot, data):
    """ Creates a plotly scatter chart dict from the SVL plot and data specs.

        Parameters
        ----------
        svl_plot : dict
            The SVL plot specifier.

        data : dict
            The SVL data specifier.

        Returns
        -------
        dict
            The dictionary defining the plotly plot.
    """

    plot_type = {"mode": "markers", "type": "scatter"}
    layout = {}
    raw_traces = _extract_all_traces(svl_plot, data)

    if "color" in svl_plot:
        traces = [
            merge(plot_type, {"name": color}, trace)
            # NOTE: Danger!! Implicit coupling to order here.
            for color, trace in zip(sorted(data.keys()), raw_traces)
        ]
    else:
        traces = [
            merge(plot_type, trace)
            for trace in raw_traces
        ]

    return {
        "layout": layout,
        "data": traces
    }


def plotly_boxplot(svl_plot, data):
    """ Creates a plotly boxplot chart dict from the SVL plot and data specs.

        Parameters
        ----------
        svl_plot : dict
            The SVL plot specifier.

        data : dict
            The SVL data specifier.

        Returns
        -------
        dict
            A {layout: ..., data: [ ... ] } dictionary defining the plotly
            chart.
    """
    layout = {}
    raw_traces = _extract_all_traces(svl_plot, data)

    # If there's a "color" element to this plot, adjust the layout and
    # attach names to the traces.
    if "color" in svl_plot:
        layout = {"boxmode": "group"}
        traces = [
            merge({"name": color, "type": "boxplot"}, trace)
            # NOTE: DANGER!! Implicit coupling to order here!!!
            for color, trace in zip(sorted(data.keys()), raw_traces)
        ]
    else:
        traces = [
            merge({"type": "boxplot"}, trace)
            for trace in raw_traces
        ]

    return {
        "data": traces,
        "layout": layout
    }


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
    num_rows = max(listpluck("row_end", svl_plots))
    num_columns = max(listpluck("column_end", svl_plots))

    plots = [
        {
            # CSS grids are 1-indexed, but the layout is zero indexed in the
            # svl layout module.
            "row_start": plot["row_start"] + 1,
            "row_end": plot["row_end"] + 1,
            "column_start": plot["column_start"] + 1,
            "column_end": plot["column_end"] + 1,
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
