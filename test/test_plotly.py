import pytest

from toolz import dissoc
from svl.plotly.plotly import (
    _get_field_name,
    _extract_all_traces,
    _get_bins,
    _get_title,
    _get_axis_label,
    _get_colorspec,
    plotly_histogram,
    plotly_pie,
    plotly_bar,
    plotly_line,
    plotly_scatter,
    plotly_template,
    plotly_template_vars,
)


@pytest.fixture
def appended_data():
    """ A fixture for data that's been generated without aggregations.
    """
    return {
        "x": [
            "2018-08-01T00:00:00Z",
            "2018-08-08T00:00:00Z",
            "2018-08-15T00:00:00Z",
        ],
        "y": [98, 102, 94],
    }


@pytest.fixture
def univariate_appended_data_x():
    """ A fixture for univariate data.
    """
    return {"x": [98, 102, 94]}


@pytest.fixture
def univariate_appended_data_y():
    """ A fixture for univariate data on the y axis.
    """
    return {"y": [98, 102, 94]}


@pytest.fixture
def univariate_categorical_data():
    """ A fixture for univariate categorical data.
    """
    return {"labels": ["Class A", "Class B", "Class C"], "values": [10, 5, 1]}


@pytest.fixture
def split_by_univariate_data():
    """ A fixture for univariate data that's split by.
    """
    return {"A": {"y": [98, 99, 94]}, "B": {"y": [93, 92, 89]}}


@pytest.fixture
def split_by_appended_data():
    """ A fixture for data that's split by and appended.
    """
    return {
        "A": {
            "x": [
                "2018-08-01T00:00:00Z",
                "2018-08-01T00:00:00Z",
                "2018-09-01T00:00:00Z",
            ],
            "y": [98, 99, 94],
        },
        "B": {
            "x": [
                "2018-09-01T00:00:00Z",
                "2018-09-01T00:00:00Z",
                "2018-10-01T00:00:00Z",
            ],
            "y": [93, 92, 89],
        },
    }


@pytest.fixture
def agged_data():
    """ A fixture for data that's been aggregated by date.
    """
    return {
        "x": [
            "2018-08-01T00:00:00Z",
            "2018-09-01T00:00:00Z",
            "2018-10-01T00:00:00Z",
        ],
        "y": [98, 94, 89],
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
                "2018-10-01T00:00:00Z",
            ],
            "y": [98, 94, 89],
        },
        "B": {
            "x": [
                "2018-08-01T00:00:00Z",
                "2018-09-01T00:00:00Z",
                "2018-10-01T00:00:00Z",
            ],
            "y": [99, 92, 87],
        },
    }


@pytest.fixture()
def color_by_agged_data():
    """ A fixture for data that's been colored by temperature and aggregated
        by date.
    """
    return {
        "x": [
            "2017-01-01T00:00:00Z",
            "2018-01-01T00:00:00Z",
            "2019-01-01T00:00:00Z",
        ],
        "y": [99, 98, 99],
        "color_by": [0.3, 0.2, 0.1],
    }


def test_get_field_name_transform():
    """ Tests that the _get_field_name function returns the correct value
        when the svl axis has a transform.
    """
    svl_axis = {"transform": "x+1"}
    truth = "x+1"
    answer = _get_field_name(svl_axis)
    assert truth == answer


def test_get_field_name_field():
    """ Tests that the _get_field_name function returns the correct value
        when the svl axis has a field.
    """
    svl_axis = {"field": "date"}
    truth = "date"
    answer = _get_field_name(svl_axis)
    assert truth == answer


def test_get_field_name_none():
    """ Tests that the _get_field_name function returns the correct value when
        there is no field in the SVL axis.
    """
    svl_axis = {"agg": "MAX"}
    truth = "*"
    answer = _get_field_name(svl_axis)
    assert truth == answer


def test_extract_all_traces_no_split_by(agged_data):
    """ Tests that the _extract_all_traces function returns the correct value
        when the plot has no split by specifier.
    """
    svl_plot = {
        "x": {"field": "date", "temporal": "MONTH"},
        "y": {"field": "temperature", "agg": "MAX"},
    }

    truth = [
        {
            "x": [
                "2018-08-01T00:00:00Z",
                "2018-09-01T00:00:00Z",
                "2018-10-01T00:00:00Z",
            ],
            "y": [98, 94, 89],
        }
    ]

    answer = _extract_all_traces(svl_plot, agged_data)

    assert truth == answer


def test_extract_all_traces_split_by(split_by_agged_data):
    """ Tests that the _extract_all_traces function returns the correct value
        when the plot has a split by specifier.
    """
    svl_plot = {
        "x": {"field": "date", "temporal": "MONTH"},
        "y": {"field": "temperature", "agg": "MAX"},
        "split_by": {"field": "classification"},
    }

    truth = [
        {
            "x": [
                "2018-08-01T00:00:00Z",
                "2018-09-01T00:00:00Z",
                "2018-10-01T00:00:00Z",
            ],
            "y": [98, 94, 89],
        },
        {
            "x": [
                "2018-08-01T00:00:00Z",
                "2018-09-01T00:00:00Z",
                "2018-10-01T00:00:00Z",
            ],
            "y": [99, 92, 87],
        },
    ]

    answer = _extract_all_traces(svl_plot, split_by_agged_data)

    assert truth == answer


def test_extract_all_traces_color_by(color_by_agged_data):
    """ Tests that the _extract_all_traces function returns the correct value
        when there's a color_by axis in the svl specifier.
    """
    svl_plot = {
        "x": {"field": "date", "temporal": "MONTH"},
        "y": {"field": "temperature", "agg": "MAX"},
        "color_by": {"field": "humidity", "agg": "MAX"},
    }

    truth = [
        {
            "x": [
                "2017-01-01T00:00:00Z",
                "2018-01-01T00:00:00Z",
                "2019-01-01T00:00:00Z",
            ],
            "y": [99, 98, 99],
        }
    ]

    answer = _extract_all_traces(svl_plot, color_by_agged_data)

    assert truth == answer


def test_get_title_explicit():
    """ Tests that the _get_title function returns the correct value when the
        title is explicitly provided.
    """
    svl_plot = {
        "dataset": "bigfoot",
        "x": {"field": "latitude"},
        "y": {"field": "temperature_mid"},
        "title": "Temperature by Latitude",
        "type": "scatter",
    }

    truth = "Temperature by Latitude"
    answer = _get_title(svl_plot)

    assert truth == answer


def test_get_title_histogram():
    """ Tests that the _get_title function returns the correct value for
        histograms.
    """
    svl_plot = {
        "data": "bigfoot",
        "x": {"field": "temperature_mid"},
        "type": "histogram",
    }

    truth = "bigfoot: temperature_mid"
    answer = _get_title(svl_plot)

    assert truth == answer


def test_get_title_pie():
    """ Tests that the _get_title function returns the correct value for
        pie charts.
    """
    svl_plot = {
        "data": "bigfoot",
        "axis": {"field": "classification"},
        "type": "pie",
    }

    truth = "bigfoot: classification"
    answer = _get_title(svl_plot)

    assert truth == answer


def test_get_title_xy():
    """ Tests that the _get_title function returns the correct value for xy
        plots.
    """
    svl_plot = {
        "data": "bigfoot",
        "type": "bar",
        "x": {"field": "classification"},
        "y": {"field": "*", "agg": "COUNT"},
    }

    truth = "bigfoot: classification - *"
    answer = _get_title(svl_plot)
    assert truth == answer


def test_get_axis_label():
    """ Tests that the _get_axis_label function returns the correct value when
        the label is provided.
    """
    svl_plot = {
        "data": "bigfoot",
        "type": "line",
        "x": {"field": "date", "temporal": "YEAR", "label": "Date"},
        "y": {"field": "*", "agg": "COUNT", "label": "Number of Sightings"},
        "title": "Bigfoot Sightings by Year",
    }

    truth = "Date"
    answer = _get_axis_label(svl_plot, axis="x")

    assert truth == answer


def test_get_bins_x():
    """ Tests that the _get_bins function returns the correct value when there
        is no bin specifier.
    """
    svl_plot = {
        "type": "histogram",
        "data": "bigfoot",
        "x": {"field": "temperature_mid"},
    }

    truth = {"autobinx": True}
    answer = _get_bins(svl_plot)

    assert truth == answer


def test_get_bins_y():
    """ Tests that the _get_bins function returns the correct value when there
        is no bin specifier.
    """
    svl_plot = {
        "type": "histogram",
        "data": "bigfoot",
        "y": {"field": "temperature_mid"},
    }

    truth = {"autobiny": True}
    answer = _get_bins(svl_plot)

    assert truth == answer


def test_get_bins_step_x():
    """ Tests that the _get_bins function returns the correct value when there
        is a step bin specifier.
    """
    svl_plot = {
        "type": "histogram",
        "data": "bigfoot",
        "x": {"field": "temperature_low"},
        "step": 5,
    }

    truth = {"xbins": {"size": 5}}
    answer = _get_bins(svl_plot)

    assert truth == answer


def test_get_bins_step_y():
    """ Tests that the _get_bins function returns the correct value when there
        is a step bin specifier.
    """
    svl_plot = {
        "type": "histogram",
        "data": "bigfoot",
        "y": {"field": "temperature_low"},
        "step": 5,
    }

    truth = {"ybins": {"size": 5}}
    answer = _get_bins(svl_plot)

    assert truth == answer


def test_get_bins_bins_x():
    """ Tests that the _get_bins function returns the correct value when there
        is a "bins" bin specifier.
    """
    svl_plot = {
        "type": "histogram",
        "data": "bigfoot",
        "x": {"field": "temperature_mid"},
        "bins": 50,
    }

    truth = {"nbinsx": 50}
    answer = _get_bins(svl_plot)

    assert truth == answer


def test_get_bins_bins_y():
    """ Tests that the _get_bins function returns the correct value when there
        is a "bins" bin specifier.
    """
    svl_plot = {
        "type": "histogram",
        "data": "bigfoot",
        "x": {"field": "temperature_mid"},
        "bins": 50,
    }

    truth = {"nbinsx": 50}
    answer = _get_bins(svl_plot)

    assert truth == answer


def test_get_axis_label_histogram_with_label():
    """ Tests that the _get_axis_label function returns the correct value for
        histogram plots when a label is provided.
    """
    svl_plot = {
        "type": "histogram",
        "data": "bigfoot",
        "x": {"field": "wind_speed", "label": "Wind Speed (MPH)"},
    }

    truth = "Wind Speed (MPH)"
    answer = _get_axis_label(svl_plot, "x")

    assert truth == answer


def test_get_axis_label_histogram():
    """ Tests that the _get_axis_label function returns the correct value for
        histogram plots.
    """
    svl_plot = {
        "data": "bigfoot",
        "type": "histogram",
        "x": {"field": "wind_speed"},
    }

    truth = "wind_speed"
    answer = _get_axis_label(svl_plot, "x")

    assert truth == answer


def test_get_axis_label_xy_agg():
    """ Tests that the _get_axis_label function returns the correct value for
        xy plots when an aggregation is on the axis.
    """
    svl_plot = {
        "data": "bigfoot",
        "type": "line",
        "x": {"field": "date", "temporal": "YEAR"},
        "y": {"field": "*", "agg": "COUNT"},
    }

    truth = "* (COUNT)"
    answer = _get_axis_label(svl_plot, axis="y")

    assert truth == answer


def test_get_axis_label_xy_noagg():
    """ Tests that the _get_axis_label function returns the correct value for
        xy plots.
    """
    svl_plot = {
        "type": "scatter",
        "data": "bigfoot",
        "x": {"field": "latitude"},
        "y": {"field": "temperature_mid"},
    }

    truth = "temperature_mid"
    answer = _get_axis_label(svl_plot, axis="y")

    assert truth == answer


def test_get_colorspec_no_color_by(agged_data):
    """ Tests that the _get_colorspec function returns the correct value when
        the dataset doesn't have a color spec.
    """

    svl_plot = {
        "data": "bigfoot",
        "type": "bar",
        "x": {"field": "date"},
        "y": {"field": "temperature_mid", "agg": "MAX"},
    }

    truth = {}

    answer = _get_colorspec(svl_plot, agged_data)

    assert truth == answer


def test_get_colorspec(color_by_agged_data):
    """ Tests that the _get_colorspec function returns the correct value when
        the plot and data have a color by axis.
    """
    svl_plot = {
        "dataset": "bigfoot",
        "type": "bar",
        "x": {"field": "date", "temporal": "DAY"},
        "y": {"field": "temperature_mid", "agg": "MAX"},
        "color_by": {
            "field": "humidity",
            "agg": "MAX",
            "label": "Humidity",
            "color_scale": "Jet",
        },
    }

    truth = {
        "marker": {
            "color": [0.3, 0.2, 0.1],
            "colorbar": {"title": "Humidity"},
            "colorscale": "Jet",
        }
    }

    answer = _get_colorspec(svl_plot, color_by_agged_data)

    assert truth == answer


def test_get_colorspec_no_label_no_scale(color_by_agged_data):
    """ Tests that the _get_colorspec function returns the correct value when
        there's no color by axis label or color scale.
    """

    svl_plot = {
        "dataset": "bigfoot",
        "type": "bar",
        "x": {"field": "date", "temporal": "DAY"},
        "y": {"field": "temperature_mid", "agg": "MAX"},
        "color_by": {"field": "humidity", "agg": "MAX"},
    }

    truth = {
        "marker": {
            "color": [0.3, 0.2, 0.1],
            "colorbar": {"title": "humidity (MAX)"},
            "colorscale": None,
        }
    }

    answer = _get_colorspec(svl_plot, color_by_agged_data)

    assert truth == answer


def test_plotly_histogram_x(univariate_appended_data_x):
    """ Tests that the plotly_histogram function returns the correct value
        when the values are on the x axis.
    """

    svl_plot = {
        "type": "histogram",
        "x": {"field": "temperature"},
        "data": "bigfoot",
    }

    truth = {
        "layout": {
            "title": "bigfoot: temperature",
            "xaxis": {"title": "temperature"},
        },
        "data": [{"type": "histogram", "x": [98, 102, 94], "autobinx": True}],
    }

    answer = plotly_histogram(svl_plot, univariate_appended_data_x)

    assert truth == answer


def test_plotly_histogram_y(univariate_appended_data_y):
    """ Tests that the plotly_histogram function returns the correct value
        when the values are on the y axis.
    """

    svl_plot = {
        "type": "histogram",
        "y": {"field": "temperature"},
        "data": "bigfoot",
    }

    truth = {
        "layout": {
            "title": "bigfoot: temperature",
            "yaxis": {"title": "temperature"},
        },
        "data": [{"type": "histogram", "y": [98, 102, 94], "autobiny": True}],
    }

    answer = plotly_histogram(svl_plot, univariate_appended_data_y)

    assert truth == answer


def test_plotly_histogram_split_by(split_by_univariate_data):
    svl_plot = {
        "type": "histogram",
        "data": "bigfoot",
        "y": {"field": "temperature_mid"},
        "split_by": {"field": "classification"},
    }

    truth = {
        "layout": {
            "barmode": "overlay",
            "title": "bigfoot: temperature_mid",
            "yaxis": {"title": "temperature_mid"},
        },
        "data": [
            {
                "type": "histogram",
                "name": "A",
                "y": [98, 99, 94],
                "autobiny": True,
                "opacity": 0.6,
            },
            {
                "type": "histogram",
                "name": "B",
                "y": [93, 92, 89],
                "autobiny": True,
                "opacity": 0.6,
            },
        ],
    }

    answer = plotly_histogram(svl_plot, split_by_univariate_data)

    assert truth == answer


def test_plotly_pie(univariate_categorical_data):
    """ Tests that the plotly_pie function returns the correct value.
    """

    svl_plot = {
        "type": "pie",
        "axis": {"field": "classification"},
        "data": "bigfoot",
    }

    truth = {
        "layout": {"title": "bigfoot: classification"},
        "data": [
            {
                "type": "pie",
                "labels": ["Class A", "Class B", "Class C"],
                "values": [10, 5, 1],
                "hole": 0,
            }
        ],
    }

    answer = plotly_pie(svl_plot, univariate_categorical_data)
    assert truth == answer


def test_plotly_pie_hole(univariate_categorical_data):
    """ Tests that the plotly_pie function returns the correct value when a
        hole value is provided.
    """
    svl_plot = {
        "type": "pie",
        "axis": {"field": "classification"},
        "data": "bigfoot",
        "hole": 0.4,
        "title": "Bigfoot Sightings by Classification",
    }

    truth = {
        "layout": {"title": "Bigfoot Sightings by Classification"},
        "data": [
            {
                "type": "pie",
                "labels": ["Class A", "Class B", "Class C"],
                "values": [10, 5, 1],
                "hole": 0.4,
            }
        ],
    }

    answer = plotly_pie(svl_plot, univariate_categorical_data)
    assert truth == answer


def test_plotly_bar(agged_data):
    """ Tests that the plotly_bar function returns the correct value.
    """

    svl_plot = {
        "data": "bigfoot",
        "type": "bar",
        "x": {"field": "date", "temporal": "MONTH"},
        "y": {"agg": "MAX", "field": "temperature"},
    }

    truth = {
        "layout": {
            "title": "bigfoot: date - temperature",
            "xaxis": {"title": "date"},
            "yaxis": {"title": "temperature (MAX)"},
        },
        "data": [
            {
                "type": "bar",
                "x": [
                    "2018-08-01T00:00:00Z",
                    "2018-09-01T00:00:00Z",
                    "2018-10-01T00:00:00Z",
                ],
                "y": [98, 94, 89],
            }
        ],
    }

    answer = plotly_bar(svl_plot, agged_data)

    assert truth == answer


def test_plotly_bar_split_by(split_by_agged_data):
    """ Tests that the plotly_bar function returns the correct value when the
        data is split by a split by field.
    """
    svl_plot = {
        "type": "bar",
        "data": "bigfoot",
        "x": {"field": "date", "temporal": "MONTH"},
        "y": {"field": "temperature", "agg": "MAX"},
        "split_by": {"field": "classification"},
    }

    truth = {
        "layout": {
            "barmode": "group",
            "title": "bigfoot: date - temperature",
            "xaxis": {"title": "date"},
            "yaxis": {"title": "temperature (MAX)"},
        },
        "data": [
            {
                "type": "bar",
                "name": "A",
                "x": [
                    "2018-08-01T00:00:00Z",
                    "2018-09-01T00:00:00Z",
                    "2018-10-01T00:00:00Z",
                ],
                "y": [98, 94, 89],
            },
            {
                "type": "bar",
                "name": "B",
                "x": [
                    "2018-08-01T00:00:00Z",
                    "2018-09-01T00:00:00Z",
                    "2018-10-01T00:00:00Z",
                ],
                "y": [99, 92, 87],
            },
        ],
    }

    answer = plotly_bar(svl_plot, split_by_agged_data)

    assert truth == answer


def test_plotly_bar_color_by(color_by_agged_data):
    """ Tests that the plotly_bar function returns the correct value when
        there's a color_by axis.
    """
    svl_plot = {
        "type": "bar",
        "data": "bigfoot",
        "x": {"field": "date", "temporal": "YEAR"},
        "y": {"field": "temperature_mid", "agg": "MAX"},
        "color_by": {"field": "humidity", "agg": "MAX"},
    }

    truth = {
        "layout": {
            "title": "bigfoot: date - temperature_mid",
            "xaxis": {"title": "date"},
            "yaxis": {"title": "temperature_mid (MAX)"},
        },
        "data": [
            {
                "type": "bar",
                "x": [
                    "2017-01-01T00:00:00Z",
                    "2018-01-01T00:00:00Z",
                    "2019-01-01T00:00:00Z",
                ],
                "y": [99, 98, 99],
                "marker": {
                    "color": [0.3, 0.2, 0.1],
                    "colorbar": {"title": "humidity (MAX)"},
                    "colorscale": None,
                },
            }
        ],
    }

    answer = plotly_bar(svl_plot, color_by_agged_data)

    assert truth == answer


def test_plotly_line(agged_data):
    """ Tests that the plotly_line function returns the correct value.
    """

    svl_plot = {
        "data": "bigfoot",
        "type": "line",
        "x": {"field": "date", "temporal": "MONTH"},
        "y": {"field": "temperature", "agg": "MAX"},
    }

    truth = {
        "layout": {
            "title": "bigfoot: date - temperature",
            "xaxis": {"title": "date"},
            "yaxis": {"title": "temperature (MAX)"},
        },
        "data": [
            {
                "mode": "lines+markers",
                "type": "scatter",
                "x": [
                    "2018-08-01T00:00:00Z",
                    "2018-09-01T00:00:00Z",
                    "2018-10-01T00:00:00Z",
                ],
                "y": [98, 94, 89],
            }
        ],
    }

    answer = plotly_line(svl_plot, agged_data)

    assert truth == answer


def test_plotly_line_split_by(split_by_agged_data):
    """ Tests that the plotly_line function returns the correct value when
        the dataset contains a split by.
    """
    svl_plot = {
        "type": "line",
        "data": "bigfoot",
        "x": {"field": "date", "temporal": "MONTH"},
        "y": {"field": "temperature", "agg": "MAX"},
        "split_by": {"field": "classification"},
    }

    truth = {
        "layout": {
            "title": "bigfoot: date - temperature",
            "xaxis": {"title": "date"},
            "yaxis": {"title": "temperature (MAX)"},
        },
        "data": [
            {
                "type": "scatter",
                "mode": "lines+markers",
                "name": "A",
                "x": [
                    "2018-08-01T00:00:00Z",
                    "2018-09-01T00:00:00Z",
                    "2018-10-01T00:00:00Z",
                ],
                "y": [98, 94, 89],
            },
            {
                "type": "scatter",
                "mode": "lines+markers",
                "name": "B",
                "x": [
                    "2018-08-01T00:00:00Z",
                    "2018-09-01T00:00:00Z",
                    "2018-10-01T00:00:00Z",
                ],
                "y": [99, 92, 87],
            },
        ],
    }

    answer = plotly_line(svl_plot, split_by_agged_data)

    assert truth == answer


def test_plotly_line_color_by(color_by_agged_data):
    """ Tests that the plotly_line function returns the correct value when
        there's a color_by axis.
    """
    svl_plot = {
        "type": "line",
        "data": "bigfoot",
        "x": {"field": "date", "temporal": "YEAR"},
        "y": {"field": "temperature_mid", "agg": "MAX"},
        "color_by": {"field": "humidity", "agg": "MAX"},
    }

    truth = {
        "layout": {
            "title": "bigfoot: date - temperature_mid",
            "xaxis": {"title": "date"},
            "yaxis": {"title": "temperature_mid (MAX)"},
        },
        "data": [
            {
                "type": "scatter",
                "mode": "lines+markers",
                "x": [
                    "2017-01-01T00:00:00Z",
                    "2018-01-01T00:00:00Z",
                    "2019-01-01T00:00:00Z",
                ],
                "y": [99, 98, 99],
                "marker": {
                    "color": [0.3, 0.2, 0.1],
                    "colorbar": {"title": "humidity (MAX)"},
                    "colorscale": None,
                },
            }
        ],
    }

    answer = plotly_line(svl_plot, color_by_agged_data)

    assert truth == answer


def test_plotly_scatter(appended_data):
    """ Tests that the plotly_scatter function returns the correct value.
    """
    svl_plot = {
        "type": "scatter",
        "data": "bigfoot",
        "x": {"field": "date", "temporal": "DAY"},
        "y": {"field": "temperature"},
    }

    truth = {
        "layout": {
            "title": "bigfoot: date - temperature",
            "xaxis": {"title": "date"},
            "yaxis": {"title": "temperature"},
        },
        "data": [
            {
                "mode": "markers",
                "type": "scatter",
                "x": [
                    "2018-08-01T00:00:00Z",
                    "2018-08-08T00:00:00Z",
                    "2018-08-15T00:00:00Z",
                ],
                "y": [98, 102, 94],
            }
        ],
    }

    answer = plotly_scatter(svl_plot, appended_data)

    assert truth == answer


def test_plotly_scatter_split_by(split_by_appended_data):
    """ Tests that the plotly_scatter function returns the correct value when
        there's a split by split.
    """
    svl_plot = {
        "type": "scatter",
        "data": "bigfoot",
        "x": {"field": "date", "temporal": "MONTH"},
        "y": {"field": "temperature"},
        "split_by": {"field": "classification"},
    }

    truth = {
        "data": [
            {
                "x": [
                    "2018-08-01T00:00:00Z",
                    "2018-08-01T00:00:00Z",
                    "2018-09-01T00:00:00Z",
                ],
                "y": [98, 99, 94],
                "name": "A",
                "type": "scatter",
                "mode": "markers",
            },
            {
                "x": [
                    "2018-09-01T00:00:00Z",
                    "2018-09-01T00:00:00Z",
                    "2018-10-01T00:00:00Z",
                ],
                "y": [93, 92, 89],
                "name": "B",
                "type": "scatter",
                "mode": "markers",
            },
        ],
        "layout": {
            "title": "bigfoot: date - temperature",
            "xaxis": {"title": "date"},
            "yaxis": {"title": "temperature"},
        },
    }

    answer = plotly_scatter(svl_plot, split_by_appended_data)

    assert truth == answer


def test_plotly_scatter_color_by(color_by_agged_data):
    """ Tests that the plotly_scatter function returns the correct value when
        there's a color_by axis.
    """
    svl_plot = {
        "type": "scatter",
        "data": "bigfoot",
        "x": {"field": "date", "temporal": "YEAR"},
        "y": {"field": "temperature_mid", "agg": "MAX"},
        "color_by": {"field": "humidity", "agg": "MAX"},
    }

    truth = {
        "layout": {
            "title": "bigfoot: date - temperature_mid",
            "xaxis": {"title": "date"},
            "yaxis": {"title": "temperature_mid (MAX)"},
        },
        "data": [
            {
                "type": "scatter",
                "mode": "markers",
                "x": [
                    "2017-01-01T00:00:00Z",
                    "2018-01-01T00:00:00Z",
                    "2019-01-01T00:00:00Z",
                ],
                "y": [99, 98, 99],
                "marker": {
                    "color": [0.3, 0.2, 0.1],
                    "colorbar": {"title": "humidity (MAX)"},
                    "colorscale": None,
                },
            }
        ],
    }

    answer = plotly_scatter(svl_plot, color_by_agged_data)

    assert truth == answer


def test_plotly_template_vars(univariate_appended_data_x):
    """ Tests that the plotly_template_vars function returns the correct value.
    """
    svl_plots = [
        {
            "row_start": 0,
            "row_end": 1,
            "column_start": 0,
            "column_end": 2,
            "type": "histogram",
            "x": {"field": "temperature"},
            "bins": 25,
            "data": "bigfoot",
        },
        {
            "row_start": 1,
            "row_end": 2,
            "column_start": 0,
            "column_end": 1,
            "type": "histogram",
            "x": {"field": "temperature"},
            "bins": 15,
            "data": "bigfoot",
        },
        {
            "row_start": 1,
            "row_end": 2,
            "column_start": 1,
            "column_end": 2,
            "type": "histogram",
            "x": {"field": "temperature"},
            "bins": 10,
            "data": "bigfoot",
        },
    ]

    datas = [univariate_appended_data_x] * 3

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
                        "title": "bigfoot: temperature",
                        "xaxis": {"title": "temperature"},
                    },
                    "data": [
                        {"type": "histogram", "x": [98, 102, 94], "nbinsx": 25}
                    ],
                },
            },
            {
                "row_start": 2,
                "row_end": 3,
                "column_start": 1,
                "column_end": 2,
                "plotly": {
                    "layout": {
                        "title": "bigfoot: temperature",
                        "xaxis": {"title": "temperature"},
                    },
                    "data": [
                        {"type": "histogram", "x": [98, 102, 94], "nbinsx": 15}
                    ],
                },
            },
            {
                "row_start": 2,
                "row_end": 3,
                "column_start": 2,
                "column_end": 3,
                "plotly": {
                    "layout": {
                        "title": "bigfoot: temperature",
                        "xaxis": {"title": "temperature"},
                    },
                    "data": [
                        {"type": "histogram", "x": [98, 102, 94], "nbinsx": 10}
                    ],
                },
            },
        ],
    }

    answer = plotly_template_vars(svl_plots, datas)

    assert "plotly_js" in answer
    assert truth == dissoc(answer, "plotly_js")


def test_plotly_template():
    """ Tests that the plotly_template function returns the correct value.
    """

    answer = plotly_template()

    truth = "index.jinja"

    assert truth == answer.name
