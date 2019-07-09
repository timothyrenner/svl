import importlib_resources

from toolz import merge, compose, pluck, get, dissoc, get_in
from jinja2 import Environment, PackageLoader, select_autoescape


listpluck = compose(list, pluck)


def _get_field_name(svl_axis):
    """ Extracts the name of the field for the SVL plot.

    Parameters
    ----------
    svl_axis : dict
        The SVL axis specifier.

    Returns
    -------
    str
        The name of the field in the axis, or the transform statement.
    """
    if "transform" in svl_axis:
        return svl_axis["transform"]
    elif "field" in svl_axis:
        return svl_axis["field"]
    else:
        return "*"


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
    if "split_by" not in svl_plot:
        return [dissoc(data, "color_by")]
    else:
        return [data[split_by] for split_by in sorted(data.keys())]


def _get_title(svl_plot):
    """ Gets the title of the plot if present, or provides a reasonable
        default.

        Parameters
        ----------
        svl_plot : dict
            The SVL plot specification.

        Returns
        -------
        str
            The title of the plot.
    """
    if "title" in svl_plot:
        return svl_plot["title"]
    elif svl_plot["type"] == "pie":
        return "{}: {}".format(
            svl_plot["data"], _get_field_name(svl_plot["axis"])
        )
    elif svl_plot["type"] == "histogram":
        svl_axis = "x" if "x" in svl_plot else "y"
        return "{}: {}".format(
            svl_plot["data"], _get_field_name(svl_plot[svl_axis])
        )
    else:
        # xy plot
        return "{}: {} - {}".format(
            svl_plot["data"],
            _get_field_name(svl_plot["x"]),
            _get_field_name(svl_plot["y"]),
        )


def _get_axis_label(svl_plot, axis):
    """ Gets the label of the provided axis if present, or generates a
        reasonable default.

        Parameters
        ----------
        svl_plot : dict
            The SVL plot specifier.
        axis : str
            The axis to get the label for. Default=None (for single axis
            plots).

        Returns
        -------
        str
            The label for the axis.
    """
    if "label" in svl_plot[axis]:
        # If a label is provided, use it.
        return svl_plot[axis]["label"]
    elif "agg" in svl_plot[axis]:
        # If there's an aggregation, include it.
        return "{} ({})".format(
            _get_field_name(svl_plot[axis]), svl_plot[axis]["agg"]
        )
    else:
        # Otherwise just grab the field name.
        return _get_field_name(svl_plot[axis])


def _get_bins(svl_plot):
    """ Gets the right bin specifier from the SVL plot.

        Parameters
        ----------
        svl_plot : dict

        Returns
        -------
        dict
            The bin specifier that plotly needs. Not necessarily the one it
            deserves.
    """
    svl_axis = "x" if "x" in svl_plot else "y"
    if "step" in svl_plot:
        # Set the bin size.
        bin_axis = svl_axis + "bins"
        bins = {bin_axis: {"size": svl_plot["step"]}}
    elif "bins" in svl_plot:
        # Set the number of bins.
        bin_axis = "nbins" + svl_axis
        bins = {bin_axis: svl_plot["bins"]}
    else:
        # Activate autobins.
        bin_axis = "autobin" + svl_axis
        bins = {bin_axis: True}
    return bins


def _get_colorspec(svl_plot, data):
    """ Extracts a markerspec (if applicable) from the SVL plot color axis.

        Parameters
        ----------
        svl_plot : dict
            The SVL plot specifier.
        data : dict[str, list]
            The data for the plot. The dict should have "color_by" if there's
            a color axis for the plot.

        Returns
        --------
        dict
            The marker spec that defines the color axis for the plot.
    """
    color = {}

    if "color_by" in svl_plot:
        color = {
            "marker": {
                "color": data["color_by"],
                "colorbar": {
                    "title": _get_axis_label(svl_plot, axis="color_by")
                },
                "colorscale": get_in(
                    ["color_by", "color_scale"], svl_plot, None
                ),
            }
        }

    return color


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

    plot_type = {"type": "histogram"}
    svl_axis = "x" if "x" in svl_plot else "y"
    layout_axis = svl_axis + "axis"
    layout = {
        "title": _get_title(svl_plot),
        layout_axis: {"title": _get_axis_label(svl_plot, axis=svl_axis)},
    }
    raw_traces = _extract_all_traces(svl_plot, data)

    if "split_by" in svl_plot:
        layout["barmode"] = "overlay"
        traces = [
            merge(
                plot_type,
                {"name": split_by, "opacity": 0.6},
                trace,
                _get_bins(svl_plot),
            )
            for split_by, trace in zip(sorted(data.keys()), raw_traces)
        ]
    else:
        traces = [
            merge(plot_type, trace, _get_bins(svl_plot))
            for trace in raw_traces
        ]

    return {"layout": layout, "data": traces}


def plotly_pie(svl_plot, data):
    """ Creates a plotly pie chart from the SVL plot and data specs.

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
    layout = {"title": _get_title(svl_plot)}

    trace = {
        "type": "pie",
        "labels": data["labels"],
        "values": data["values"],
        "hole": get("hole", svl_plot, 0),
    }

    return {"layout": layout, "data": [trace]}


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
    color = _get_colorspec(svl_plot, data)
    layout = {
        "title": _get_title(svl_plot),
        "xaxis": {"title": _get_axis_label(svl_plot, axis="x")},
        "yaxis": {"title": _get_axis_label(svl_plot, axis="y")},
    }
    raw_traces = _extract_all_traces(svl_plot, data)

    if "split_by" in svl_plot:
        layout["barmode"] = "group"
        traces = [
            merge(plot_type, {"name": split_by}, trace)
            # ! Danger!! Implicit coupling to order here.
            for split_by, trace in zip(sorted(data.keys()), raw_traces)
        ]
    else:
        traces = [merge(plot_type, color, trace) for trace in raw_traces]

    return {"layout": layout, "data": traces}


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
    color = _get_colorspec(svl_plot, data)

    layout = {
        "title": _get_title(svl_plot),
        "xaxis": {"title": _get_axis_label(svl_plot, axis="x")},
        "yaxis": {"title": _get_axis_label(svl_plot, axis="y")},
    }
    raw_traces = _extract_all_traces(svl_plot, data)

    if "split_by" in svl_plot:
        # If split_by is in the plot, color_by can't be in it.
        traces = [
            merge(plot_type, {"name": split_by}, trace)
            # ! Danger!! Implicit coupling to order here.
            for split_by, trace in zip(sorted(data.keys()), raw_traces)
        ]
    else:
        traces = [merge(plot_type, color, trace) for trace in raw_traces]

    return {"layout": layout, "data": traces}


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
    color = _get_colorspec(svl_plot, data)
    layout = {
        "title": _get_title(svl_plot),
        "xaxis": {"title": _get_axis_label(svl_plot, axis="x")},
        "yaxis": {"title": _get_axis_label(svl_plot, axis="y")},
    }
    raw_traces = _extract_all_traces(svl_plot, data)

    if "split_by" in svl_plot:
        traces = [
            merge(plot_type, {"name": split_by}, trace)
            # ! Danger!! Implicit coupling to order here.
            for split_by, trace in zip(sorted(data.keys()), raw_traces)
        ]
    else:
        traces = [merge(plot_type, color, trace) for trace in raw_traces]

    return {"layout": layout, "data": traces}


PLOTLY_PLOTS = {
    "histogram": plotly_histogram,
    "bar": plotly_bar,
    "line": plotly_line,
    "scatter": plotly_scatter,
    "pie": plotly_pie,
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
            format produced by the sqlite module.

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
            "plotly": PLOTLY_PLOTS[plot["type"]](plot, data),
        }
        for plot, data in zip(svl_plots, datas)
    ]

    # Right now we're just going to slurp that file every time. If that turns
    # out to be a perf issue or something we can always add a flag to the
    # function to skip.
    with importlib_resources.path(
        "svl.plotly.js", "plotly-latest.min.js"
    ) as plotly_js_path:
        # For some reason we need a string in Python 3.5.
        plotly_js = open(str(plotly_js_path), "r").read()

    return {
        "num_rows": num_rows,
        "num_columns": num_columns,
        "plots": plots,
        "plotly_js": plotly_js,
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
        autoescape=select_autoescape(["html"]),
    )

    return env.get_template("index.jinja")
