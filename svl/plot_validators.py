from toolz import get

PLOT_VALIDATORS = [
    (
        {"line", "scatter", "bar"},
        lambda x: ("x" not in x) or ("y" not in x),
        "XY plot does not have X and Y."
    ),
    (
        {"histogram"},
        lambda x: ("step" in x) and ("bins" in x),
        "Histogram cannot have STEP and BINS."
    ),
    (
        {"line", "scatter", "bar"},
        lambda x: ("agg" in x["x"]) and ("agg" in x["y"]),
        "XY plot cannot have an aggregation on X and Y."
    ),
    (
        {"histogram", "pie"},
        lambda x: (
            "agg" in get("x", x, {})
        ) or (
            "agg" in get("y", x, {})
        ) or (
            "agg" in get("axis", x, {})
        ),
        "Histograms and pie charts cannot have aggregations."
    ),
    (
        {"histogram", "pie"},
        lambda x: (
            "temporal" in get("x", x, {})
        ) or (
            "temporal" in get("y", x, {})
        ) or (
            "temporal" in get("axis", x, {})
        ),
        "Histograms and pie charts cannot have temporal axes."
    ),
    (
        {"histogram"},
        lambda x: ("x" in x) and ("y" in x),
        "Histograms can have X or Y, not both."
    ),
    (
        {"histogram"},
        lambda x: ("x" not in x) and ("y" not in x),
        "Histograms must have an X or Y."
    ),
    (
        {"pie"},
        lambda x: "axis" not in x,
        "Pie charts must have an axis."
    ),
    (
        {"line", "bar"},  # SORT is a no-op for scatter.
        lambda x: ("sort" in x["x"]) and ("sort" in x["y"]),
        "Cannot sort by two axes."
    ),
    (
        {"pie"},
        lambda x: (get("hole", x, 0.0) < 0) or (get("hole", x, 0.0) > 1),
        "HOLE must be between zero and one."
    )
]


def validate_plot(svl_plot):
    """ Validates the SVL plot.

        Parameters
        ----------
        svl_plot : dict
            The SVL plot specifier.

        Returns
        -------
        Tuple[bool, str]
            A boolean indicating whether the plot is valid and a message
            indicating that the plot is either valid or which validations it
            failed.
    """
    ok = True
    failure_messages = []

    for plots, validator, message in PLOT_VALIDATORS:
        if (svl_plot["type"] in plots) and validator(svl_plot):
            ok = False
            failure_messages.append(message)

    return ok, "\n".join(failure_messages)
