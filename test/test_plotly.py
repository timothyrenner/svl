import pytest

from svl.plotly.plotly import (
    _extract_trace_data,
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
    """ A fixture for data that's been generated by the append reducer.
    """
    return {
        "date": [
            "2018-08-01T00:00:00Z",
            "2018-08-08T00:00:00Z",
            "2018-08-15T00:00:00Z"
        ],
        "temperature": [98, 102, 94]
    }


@pytest.fixture
def color_appended_data():
    """ A fixture for data that's split by color and appended.
    """
    return {
        "A": {
            "date": [
                "2018-08-01T00:00:00Z",
                "2018-08-01T00:00:00Z",
                "2018-09-01T00:00:00Z"
            ],
            "temperature": [98, 99, 94]
        },
        "B": {
            "date": [
                "2018-09-01T00:00:00Z",
                "2018-09-01T00:00:00Z",
                "2018-10-01T00:00:00Z"
            ],
            "temperature": [93, 92, 89]
        }
    }


@pytest.fixture
def agged_data():
    """ A fixture for data that's been aggregated by date.
    """
    return {
        "2018-08-01T00:00:00Z": 98,
        "2018-09-01T00:00:00Z": 94,
        "2018-10-01T00:00:00Z": 89
    }


@pytest.fixture
def color_agged_data():
    """ A fixture for data that's been split by classification and aggregated
        by date.
    """
    return {
        "A": {
            "2018-08-01T00:00:00Z": 98,
            "2018-09-01T00:00:00Z": 94,
            "2018-10-01T00:00:00Z": 89
        },
        "B": {
            "2018-08-01T00:00:00Z": 99,
            "2018-09-01T00:00:00Z": 92,
            "2018-10-01T00:00:00Z": 87
        }
    }


def test_extract_trace_data_no_agg(appended_data):
    """ Tests that the _extract_trace_data function returns the correct value
        when the dataset is present with no aggregations.
    """
    svl_field_x = {
        "field": "date",
        "temporal": "DAY"
    }

    svl_field_y = {
        "field": "temperature"
    }

    truth = {
        "x": [
            "2018-08-01T00:00:00Z",
            "2018-08-08T00:00:00Z",
            "2018-08-15T00:00:00Z"
        ],
        "y": [98, 102, 94]
    }

    answer = _extract_trace_data(svl_field_x, svl_field_y, appended_data)

    assert truth == answer


def test_extract_trace_data_agg_x(agged_data):
    """ Tests that the _extract_trace_data function returns the correct value
        when the x field is aggregated.
    """
    svl_field_x = {
        "field": "temperature",
        "agg": "MAX"
    }

    svl_field_y = {
        "field": "date",
        "temporal": "MONTH"
    }

    truth = {
        "x": [98, 94, 89],
        "y": [
            "2018-08-01T00:00:00Z",
            "2018-09-01T00:00:00Z",
            "2018-10-01T00:00:00Z"
        ]
    }

    answer = _extract_trace_data(svl_field_x, svl_field_y, agged_data)

    assert truth == answer


def test_extract_trace_data_agg_y(agged_data):
    """ Tests that the _extract_trace_data function returns the correct value
        when the y field is aggregated.
    """
    svl_field_x = {
        "field": "date",
        "temporal": "MONTH"
    }

    svl_field_y = {
        "field": "temperature",
        "agg": "MIN"
    }

    truth = {
        "x": [
            "2018-08-01T00:00:00Z",
            "2018-09-01T00:00:00Z",
            "2018-10-01T00:00:00Z"
        ],
        "y": [98, 94, 89]
    }

    answer = _extract_trace_data(svl_field_x, svl_field_y, agged_data)

    assert truth == answer


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

    truth = [{
        "type": "bar",
        "x": [
            "2018-08-01T00:00:00Z",
            "2018-09-01T00:00:00Z",
            "2018-10-01T00:00:00Z"
        ],
        "y": [98, 94, 89]
    }]

    answer = plotly_bar(svl_plot, agged_data)

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

    truth = [{
        "mode": "lines+markers",
        "type": "scatter",
        "x": [
            "2018-08-01T00:00:00Z",
            "2018-09-01T00:00:00Z",
            "2018-10-01T00:00:00Z"
        ],
        "y": [98, 94, 89]
    }]

    answer = plotly_line(svl_plot, agged_data)

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

    truth = [{
        "mode": "markers",
        "type": "scatter",
        "x": [
            "2018-08-01T00:00:00Z",
            "2018-08-08T00:00:00Z",
            "2018-08-15T00:00:00Z"
        ],
        "y": [98, 102, 94]
    }]

    answer = plotly_scatter(svl_plot, appended_data)

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
                "name": "A"
            }, {
                "x": [
                    "2018-09-01T00:00:00Z",
                    "2018-09-01T00:00:00Z",
                    "2018-10-01T00:00:00Z"
                ],
                "y": [93, 92, 89],
                "name": "B"
            }
        ],
        "layout": {
            "boxmode": "group"
        }
    }

    answer = plotly_boxplot(svl_plot, color_appended_data)

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
