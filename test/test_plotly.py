import pytest

from svl.plotly.plotly import (
    _extract_all_traces,
    plotly_histogram,
    plotly_bar,
    plotly_line,
    plotly_scatter,
    plotly_boxplot,
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
def color_appended_data():
    """ A fixture for data that's split by color and appended.
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
def color_agged_data():
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


def test_extract_all_traces_no_color(agged_data):
    """ Tests that the _extract_all_traces function returns the correct value
        when the plot has no color specifier.
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


def test_extract_all_traces_color(color_agged_data):
    """ Tests that the _extract_all_traces function returns the correct value
        when the plot has a color specifier.
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
        "color": {
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

    answer = _extract_all_traces(svl_plot, color_agged_data)

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
        "layout": {},
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
        "layout": {},
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
        "layout": {},
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


def test_plotly_bar_color(color_agged_data):
    """ Tests that the plotly_bar function returns the correct value when the
        data is split by a color field.
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
        "color": {
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

    answer = plotly_bar(svl_plot, color_agged_data)

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


def test_plotly_line_color(color_agged_data):
    """ Tests that the plotly_line function returns the correct value when
        the dataset contains a color split.
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
        "color": {
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

    answer = plotly_line(svl_plot, color_agged_data)

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


def test_plotly_scatter_color(color_appended_data):
    """ Tests that the plotly_scatter function returns the correct value when
        there's a color split.
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
        "color": {
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

    answer = plotly_scatter(svl_plot, color_appended_data)

    assert truth == answer


def test_plotly_boxplot(appended_data):
    """ Tests that the plotly_boxplot function returns the correct value.
    """
    svl_plot = {
        "type": "boxplot",
        "x": {
            "field": "date",
            "temporal": "DAY"
        },
        "y": {
            "field": "temperature"
        }
    }

    truth = {
        "data": [{
            "type": "boxplot",
            "x": [
                "2018-08-01T00:00:00Z",
                "2018-08-08T00:00:00Z",
                "2018-08-15T00:00:00Z"
            ],
            "y": [98, 102, 94]
        }],
        "layout": {}
    }

    answer = plotly_boxplot(svl_plot, appended_data)

    assert truth == answer


def test_plotly_boxplot_color(color_appended_data):
    """ Tests that the plotly_boxplot function returns the correct value with
        color aggregated data.
    """

    svl_plot = {
        "type": "boxplot",
        "x": {
            "field": "date",
            "temporal": "MONTH"
        },
        "y": {
            "field": "temperature"
        },
        "color": {
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
                "type": "boxplot"
            }, {
                "x": [
                    "2018-09-01T00:00:00Z",
                    "2018-09-01T00:00:00Z",
                    "2018-10-01T00:00:00Z"
                ],
                "y": [93, 92, 89],
                "name": "B",
                "type": "boxplot"
            }
        ],
        "layout": {
            "boxmode": "group"
        }
    }

    answer = plotly_boxplot(svl_plot, color_appended_data)

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
                    "layout": {},
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
                    "layout": {},
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
                    "layout": {},
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
