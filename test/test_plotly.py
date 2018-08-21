import pytest

from svl.plotly.plotly import plotly_histogram


@pytest.fixture
def appended_data():
    return {
        "date": [
            "2018-08-01T00:00:00Z",
            "2018-08-08T00:00:00Z",
            "2018-08-15T00:00:00Z"
        ],
        "temperature": [98, 102, 94]
    }


def test_plotly_histogram_auto(appended_data):
    """ Tests that the plotly_histogram function returns the correct value
        when there's no step or bin provided.
    """

    svl_plot = {
        "type": "histogram",
        "field": "temperature"
    }

    truth = [{
        "type": "histogram",
        "x": [98, 102, 94],
        "autobinx": True
    }]

    answer = plotly_histogram(svl_plot, appended_data)

    assert truth == answer


def test_plotly_histogram_step(appended_data):
    """ Tests that the plotly_histogram function returns the correct value with
        a step argument.
    """

    svl_plot = {
        "type": "histogram",
        "field": "temperature",
        "step": 5
    }

    truth = [{
        "type": "histogram",
        "x": [98, 102, 94],
        "xbins": {
            "size": 5
        }
    }]

    answer = plotly_histogram(svl_plot, appended_data)

    assert truth == answer


def test_plotly_histogram_bins(appended_data):
    """ Tests that the plotly_histogram function returns the correct value with
        a bins argument.
    """

    svl_plot = {
        "type": "histogram",
        "field": "temperature",
        "bins": 25
    }

    truth = [{
        "type": "histogram",
        "x": [98, 102, 94],
        "nbinsx": 25
    }]

    answer = plotly_histogram(svl_plot, appended_data)

    assert truth == answer
