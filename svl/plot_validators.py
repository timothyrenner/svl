PLOT_VALIDATORS = [
    (
        {"line", "scatter", "bar"},
        lambda x: ("x" not in x) or ("y" not in x),
        "XY plot does not have X and Y."
    ), (
        {"histogram"},
        lambda x: ("step" in x) and ("bins" in x),
        "Histogram cannot have STEP and BINS."
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
