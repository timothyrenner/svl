import subprocess


def test_histogram_cli_debug():
    """ Tests that the command line interface works correctly on the test
        dataset for histogram plots when debug is turned on.
    """
    # NOTE: Hard coded file paths aren't the greatest. It's fixable here but
    # not in the SVL script at this time.
    subprocess.run([
        "svl",
        "test/test_scripts/histogram.svl",
        "--backend", "plotly",
        "--no-browser",
        "--debug"
    ], check=True)


def test_histogram_cli_plotly():
    """ Tests that the command line interface works correctly on the test
        dataset for histogram plots.
    """
    # NOTE: Hard coded file paths aren't the greatest. It's fixable here but
    # not in the SVL script at this time.
    subprocess.run([
        "svl",
        "test/test_scripts/histogram.svl",
        "--backend", "plotly",
        "--no-browser"
    ], check=True)
