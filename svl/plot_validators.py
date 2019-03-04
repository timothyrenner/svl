PLOT_VALIDATORS = [
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
