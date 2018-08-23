import pytest

from svl.plotly.plotly import (
    plotly_histogram,
    plotly_template,
    plotly_template_vars
)


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


def test_plotly_template_vars(appended_data):
    """ Tests that the plotly_template_vars function returns the correct value.
    """
    svl_plots = [
        {
            "row_start": 1,
            "row_end": 2,
            "column_start": 1,
            "column_end": 3,
            "type": "histogram",
            "field": "temperature",
            "bins": 25
        }, {
            "row_start": 2,
            "row_end": 3,
            "column_start": 1,
            "column_end": 2,
            "type": "histogram",
            "field": "temperature",
            "bins": 15
        }, {
            "row_start": 2,
            "row_end": 3,
            "column_start": 2,
            "column_end": 3,
            "type": "histogram",
            "field": "temperature",
            "bins": 10
        }
    ]

    datas = [appended_data]*3

    truth = {
        "num_rows": 2,
        "num_columns": 2,
        "plots": [
            {
                "row_start": 1,
                "row_end": 2,
                "column_start": 1,
                "column_end": 3,
                "plotly": [{
                    "type": "histogram",
                    "x": [98, 102, 94],
                    "nbinsx": 25
                }]
            }, {
                "row_start": 2,
                "row_end": 3,
                "column_start": 1,
                "column_end": 2,
                "plotly": [{
                        "type": "histogram",
                        "x": [98, 102, 94],
                        "nbinsx": 15
                }]
            }, {
                "row_start": 2,
                "row_end": 3,
                "column_start": 2,
                "column_end": 3,
                "plotly": [{
                    "type": "histogram",
                    "x": [98, 102, 94],
                    "nbinsx": 10
                }]
            }
        ]
    }

    answer = plotly_template_vars(svl_plots, datas)

    assert truth == answer


def test_plotly_template():
    """ Tests that the plotly_template function returns the correct value.
    """

    answer = plotly_template()

    truth = "index.jinja"

    assert truth == answer.name
