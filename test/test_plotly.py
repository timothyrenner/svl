import pytest

from svl.plotly.plotly import (
    _extract_all_traces,
    plotly_histogram,
    plotly_bar,
    plotly_line,
    plotly_scatter,
    plotly_template,
    plotly_template_vars
)


@pytest.fixture
def appended_data():
    """ A fixture for data that's been generated without aggregations.
    """
    return {
        "x": [
            "2018-08-01T00:00:00Z",
            "2018-08-08T00:00:00Z",
            "2018-08-15T00:00:00Z"
        ],
        "y": [98, 102, 94]
    }


@pytest.fixture
def univariate_appended_data():
    """ A fixture for univariate data.
    """
    return {
        "x": [98, 102, 94]
    }


@pytest.fixture
def split_by_appended_data():
    """ A fixture for data that's split by and appended.
    """
    return {
        "A": {
            "x": [
                "2018-08-01T00:00:00Z",
                "2018-08-01T00:00:00Z",
                "2018-09-01T00:00:00Z"
            ],
            "y": [98, 99, 94]
        },
        "B": {
            "x": [
                "2018-09-01T00:00:00Z",
                "2018-09-01T00:00:00Z",
                "2018-10-01T00:00:00Z"
            ],
            "y": [93, 92, 89]
        }
    }


@pytest.fixture
def agged_data():
    """ A fixture for data that's been aggregated by date.
    """
    return {
        "x": [
            "2018-08-01T00:00:00Z",
            "2018-09-01T00:00:00Z",
            "2018-10-01T00:00:00Z"
        ],
        "y": [98, 94, 89]
    }


@pytest.fixture
def split_by_agged_data():
    """ A fixture for data that's been split by classification and aggregated
        by date.
    """
    return {
        "A": {
            "x": [
                "2018-08-01T00:00:00Z",
                "2018-09-01T00:00:00Z",
                "2018-10-01T00:00:00Z"
            ],
            "y": [98, 94, 89]
        },
        "B": {
            "x": [
                "2018-08-01T00:00:00Z",
                "2018-09-01T00:00:00Z",
                "2018-10-01T00:00:00Z"
            ],
            "y": [99, 92, 87]
        }
    }


def test_extract_all_traces_no_split_by(agged_data):
    """ Tests that the _extract_all_traces function returns the correct value
        when the plot has no split by specifier.
    """
    svl_plot = {
        "x": {
            "field": "date",
            "temporal": "MONTH"
        },
        "y": {
            "field": "temperature",
            "agg": "MAX"
        }
    }

    truth = [{
        "x": [
            "2018-08-01T00:00:00Z",
            "2018-09-01T00:00:00Z",
            "2018-10-01T00:00:00Z"
        ],
        "y": [98, 94, 89]
    }]

    answer = _extract_all_traces(svl_plot, agged_data)

    assert truth == answer


def test_extract_all_traces_split_by(split_by_agged_data):
    """ Tests that the _extract_all_traces function returns the correct value
        when the plot has a split by specifier.
    """
    svl_plot = {
        "x": {
            "field": "date",
            "temporal": "MONTH"
        },
        "y": {
            "field": "temperature",
            "agg": "MAX"
        },
        "split_by": {
            "field": "classification"
        }
    }

    truth = [
        {
            "x": [
                "2018-08-01T00:00:00Z",
                "2018-09-01T00:00:00Z",
                "2018-10-01T00:00:00Z"
            ],
            "y": [98, 94, 89]
        }, {
            "x": [
                "2018-08-01T00:00:00Z",
                "2018-09-01T00:00:00Z",
                "2018-10-01T00:00:00Z"
            ],
            "y": [99, 92, 87]
        }
    ]

    answer = _extract_all_traces(svl_plot, split_by_agged_data)

    assert truth == answer


def test_plotly_histogram_auto(univariate_appended_data):
    """ Tests that the plotly_histogram function returns the correct value
        when there's no step or bin provided.
    """

    svl_plot = {
        "type": "histogram",
        "field": "temperature"
    }

    truth = {
        "layout": {
            "title": "temperature",
            "xaxis": {
                "title": "temperature"
            }
        },
        "data": [{
            "type": "histogram",
            "x": [98, 102, 94],
            "autobinx": True
        }]
    }

    answer = plotly_histogram(svl_plot, univariate_appended_data)

    assert truth == answer


def test_plotly_histogram_step(univariate_appended_data):
    """ Tests that the plotly_histogram function returns the correct value with
        a step argument.
    """

    svl_plot = {
        "type": "histogram",
        "field": "temperature",
        "step": 5
    }

    truth = {
        "layout": {
            "title": "temperature",
            "xaxis": {
                "title": "temperature"
            }
        },
        "data": [{
            "type": "histogram",
            "x": [98, 102, 94],
            "xbins": {
                "size": 5
            }
        }]
    }

    answer = plotly_histogram(svl_plot, univariate_appended_data)

    assert truth == answer


def test_plotly_histogram_bins(univariate_appended_data):
    """ Tests that the plotly_histogram function returns the correct value with
        a bins argument.
    """

    svl_plot = {
        "type": "histogram",
        "field": "temperature",
        "bins": 25
    }

    truth = {
        "layout": {
            "title": "temperature",
            "xaxis": {
                "title": "temperature"
            }
        },
        "data": [{
            "type": "histogram",
            "x": [98, 102, 94],
            "nbinsx": 25
        }]
    }

    answer = plotly_histogram(svl_plot, univariate_appended_data)

    assert truth == answer


def test_plotly_bar(agged_data):
    """ Tests that the plotly_bar function returns the correct value.
    """

    svl_plot = {
        "type": "bar",
        "x": {
            "field": "date",
            "temporal": "MONTH"
        },
        "y": {
            "agg": "MAX",
            "field": "temperature"
        }
    }

    truth = {
        "layout": {},
        "data": [{
            "type": "bar",
            "x": [
                "2018-08-01T00:00:00Z",
                "2018-09-01T00:00:00Z",
                "2018-10-01T00:00:00Z"
            ],
            "y": [98, 94, 89]
        }]
    }

    answer = plotly_bar(svl_plot, agged_data)

    assert truth == answer


def test_plotly_bar_split_by(split_by_agged_data):
    """ Tests that the plotly_bar function returns the correct value when the
        data is split by a split by field.
    """
    svl_plot = {
        "type": "bar",
        "x": {
            "field": "date",
            "temporal": "MONTH"
        },
        "y": {
            "field": "temperature",
            "agg": "MAX"
        },
        "split_by": {
            "field": "classification"
        }
    }

    truth = {
        "layout": {
            "barmode": "group"
        },
        "data": [
            {
                "type": "bar",
                "name": "A",
                "x": [
                    "2018-08-01T00:00:00Z",
                    "2018-09-01T00:00:00Z",
                    "2018-10-01T00:00:00Z"
                ],
                "y": [98, 94, 89]
            }, {
                "type": "bar",
                "name": "B",
                "x": [
                    "2018-08-01T00:00:00Z",
                    "2018-09-01T00:00:00Z",
                    "2018-10-01T00:00:00Z"
                ],
                "y": [99, 92, 87]
            }
        ]
    }

    answer = plotly_bar(svl_plot, split_by_agged_data)

    assert truth == answer


def test_plotly_line(agged_data):
    """ Tests that the plotly_line function returns the correct value.
    """

    svl_plot = {
        "type": "line",
        "x": {
            "field": "date",
            "temporal": "MONTH"
        },
        "y": {
            "field": "temperature",
            "agg": "MAX"
        }
    }

    truth = {
        "layout": {},
        "data": [{
            "mode": "lines+markers",
            "type": "scatter",
            "x": [
                "2018-08-01T00:00:00Z",
                "2018-09-01T00:00:00Z",
                "2018-10-01T00:00:00Z"
            ],
            "y": [98, 94, 89]
        }]
    }

    answer = plotly_line(svl_plot, agged_data)

    assert truth == answer


def test_plotly_line_split_by(split_by_agged_data):
    """ Tests that the plotly_line function returns the correct value when
        the dataset contains a split by.
    """
    svl_plot = {
        "type": "line",
        "x": {
            "field": "date",
            "temporal": "MONTH"
        },
        "y": {
            "field": "temperature",
            "agg": "MAX"
        },
        "split_by": {
            "field": "classification"
        }
    }

    truth = {
        "layout": {},
        "data": [
            {
                "type": "scatter",
                "mode": "lines+markers",
                "name": "A",
                "x": [
                    "2018-08-01T00:00:00Z",
                    "2018-09-01T00:00:00Z",
                    "2018-10-01T00:00:00Z"
                ],
                "y": [98, 94, 89]
            }, {
                "type": "scatter",
                "mode": "lines+markers",
                "name": "B",
                "x": [
                    "2018-08-01T00:00:00Z",
                    "2018-09-01T00:00:00Z",
                    "2018-10-01T00:00:00Z"
                ],
                "y": [99, 92, 87]
            }
        ]
    }

    answer = plotly_line(svl_plot, split_by_agged_data)

    assert truth == answer


def test_plotly_scatter(appended_data):
    """ Tests that the plotly_scatter function returns the correct value.
    """
    svl_plot = {
        "type": "scatter",
        "x": {
            "field": "date",
            "temporal": "DAY"
        },
        "y": {
            "field": "temperature"
        }
    }

    truth = {
        "layout": {},
        "data": [{
            "mode": "markers",
            "type": "scatter",
            "x": [
                "2018-08-01T00:00:00Z",
                "2018-08-08T00:00:00Z",
                "2018-08-15T00:00:00Z"
            ],
            "y": [98, 102, 94]
        }]
    }

    answer = plotly_scatter(svl_plot, appended_data)

    assert truth == answer


def test_plotly_scatter_split_by(split_by_appended_data):
    """ Tests that the plotly_scatter function returns the correct value when
        there's a split by split.
    """
    svl_plot = {
        "type": "scatter",
        "x": {
            "field": "date",
            "temporal": "MONTH"
        },
        "y": {
            "field": "temperature"
        },
        "split_by": {
            "field": "classification"
        }
    }

    truth = {
        "data": [
            {
                "x": [
                    "2018-08-01T00:00:00Z",
                    "2018-08-01T00:00:00Z",
                    "2018-09-01T00:00:00Z"
                ],
                "y": [98, 99, 94],
                "name": "A",
                "type": "scatter",
                "mode": "markers"
            }, {
                "x": [
                    "2018-09-01T00:00:00Z",
                    "2018-09-01T00:00:00Z",
                    "2018-10-01T00:00:00Z"
                ],
                "y": [93, 92, 89],
                "name": "B",
                "type": "scatter",
                "mode": "markers"
            }
        ],
        "layout": {}
    }

    answer = plotly_scatter(svl_plot, split_by_appended_data)

    assert truth == answer


def test_plotly_template_vars(univariate_appended_data):
    """ Tests that the plotly_template_vars function returns the correct value.
    """
    svl_plots = [
        {
            "row_start": 0,
            "row_end": 1,
            "column_start": 0,
            "column_end": 2,
            "type": "histogram",
            "field": "temperature",
            "bins": 25
        }, {
            "row_start": 1,
            "row_end": 2,
            "column_start": 0,
            "column_end": 1,
            "type": "histogram",
            "field": "temperature",
            "bins": 15
        }, {
            "row_start": 1,
            "row_end": 2,
            "column_start": 1,
            "column_end": 2,
            "type": "histogram",
            "field": "temperature",
            "bins": 10
        }
    ]

    datas = [univariate_appended_data]*3

    truth = {
        "num_rows": 2,
        "num_columns": 2,
        "plots": [
            {
                "row_start": 1,
                "row_end": 2,
                "column_start": 1,
                "column_end": 3,
                "plotly": {
                    "layout": {
                        "title": "temperature",
                        "xaxis": {
                            "title": "temperature"
                        }
                    },
                    "data": [{
                        "type": "histogram",
                        "x": [98, 102, 94],
                        "nbinsx": 25
                    }]
                }
            }, {
                "row_start": 2,
                "row_end": 3,
                "column_start": 1,
                "column_end": 2,
                "plotly": {
                    "layout": {
                        "title": "temperature",
                        "xaxis": {
                            "title": "temperature"
                        }
                    },
                    "data": [{
                        "type": "histogram",
                        "x": [98, 102, 94],
                        "nbinsx": 15
                    }],
                }
            }, {
                "row_start": 2,
                "row_end": 3,
                "column_start": 2,
                "column_end": 3,
                "plotly": {
                    "layout": {
                        "title": "temperature",
                        "xaxis": {
                            "title": "temperature"
                        }
                    },
                    "data": [{
                        "type": "histogram",
                        "x": [98, 102, 94],
                        "nbinsx": 10
                    }]
                }
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
