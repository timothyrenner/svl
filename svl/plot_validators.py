def _validate_xy_plot_has_x_and_y(svl_plot):
    """ If the plot is an XY plot, validates that it has both X and Y.

        Parameters
        ----------
        svl_plot : dict
            The SVL plot specifier.

        Returns
        -------
        Tuple[bool, str]
            A boolean indicating whether the plot is valid and a message
            indicating the validation that failed.
    """
    ok = True
    message = "Valid."

    if svl_plot["type"] not in {"scatter", "line", "bar"}:
        return ok, message

    if ("x" not in svl_plot) or ("y" not in svl_plot):
        ok = False
        message = "XY plot does not have X and Y."

    return ok, message


def _validate_histogram_does_not_have_step_and_bins(svl_plot):
    """ If the plot is a histogram, validates that it has step or bins, but
        not both.

        Parameters
        ----------
        svl_plot : dict
            The SVL plot specifier.

        Returns
        -------
        Tuple[bool, str]
            A boolean indicating whether the plot is valid and a message
            indicating the validation that failed.
    """
    ok = True
    message = "Valid."

    if svl_plot["type"] != "histogram":
        return ok, message

    if ("step" in svl_plot) and ("bins" in svl_plot):
        ok = False
        message = "Histogram cannot have STEP and BINS."

    return ok, message


PLOT_VALIDATORS = [
    _validate_xy_plot_has_x_and_y,
    _validate_histogram_does_not_have_step_and_bins
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

    for validator in PLOT_VALIDATORS:
        valid, message = validator(svl_plot)

        if not valid:
            ok = False
            failure_messages.append(message)

    return ok, "\n".join(failure_messages)
