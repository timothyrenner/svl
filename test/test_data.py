from svl.data import (
    _convert_datetime,
    _mean,
    transform,
    append,
    aggregate,
    color,
    plot_to_reducer,
    construct_data
)

import pytest
import math

from hypothesis import given
from hypothesis.strategies import (
    lists,
    fixed_dictionaries,
    floats,
    datetimes,
    sampled_from
)
from toolz import get, get_in


@pytest.fixture()
def data():
    """ Sample data.
    """
    return [
        {"date": "2018-08-01", "classification": "A", "temperature": 100},
        {"date": "2017-10-01", "classification": "B", "temperature": 50},
        {"date": "2017-06-01", "classification": "A", "temperature": 100},
        {"date": "2018-03-21", "classification": "B", "temperature": 50},
        {"date": "2018-12-31", "classification": "A", "temperature": 50},
        {"date": "2018-01-01", "classification": "B", "temperature": 25},
        {"date": "2017-04-24", "classification": "A", "temperature": 75},
        {"date": "2017-06-12", "classification": "B", "temperature": 100}
    ]


def generate_data():
    """ Creates the strategy for generating data via hypothesis.
    """
    return lists(
        fixed_dictionaries({
            "classification": sampled_from(["A", "B", "C"]),
            "temperature": floats(),
            "date": datetimes()
        })
    ).filter(lambda x: len(x) > 0)


def test_convert_datetime():
    """ Tests that the convert_datetime function returns the correct value.
    """

    dt = "2018-08-14"
    snap = "@mon"

    truth = "2018-08-01T00:00:00Z"

    answer = _convert_datetime(dt, snap=snap)

    assert truth == answer


def test_convert_datetime_empty():
    """ Tests that the convert_datetime function returns the correct value
        when the input is empty.
    """

    dt = None
    snap = "@day"

    truth = None

    answer = _convert_datetime(dt, snap=snap)

    assert truth == answer


def test_transform(data):
    """ Tests that the transform function returns the correct value.
    """

    field = "temperature"

    def transformation(x):
        return x+1

    datum = data[0]

    truth = {"date": "2018-08-01", "classification": "A", "temperature": 101}

    answer = transform(field, transformation, datum)

    assert truth == answer


def test_append(data):
    """ Tests that the append function returns the correct value.
    """

    appender = append("date", "temperature")

    assert appender(data[0]) == {"date": ["2018-08-01"], "temperature": [100]}
    assert appender(data[1]) == {
        "date": ["2018-08-01", "2017-10-01"],
        "temperature": [100, 50]
    }
    assert appender(data[2]) == {
        "date": ["2018-08-01", "2017-10-01", "2017-06-01"],
        "temperature": [100, 50, 100]
    }


def test_mean():
    """ Tests that the _mean function returns the correct value.
    """
    a = {"sum": 10, "count": 4}
    x = 10

    truth = {"sum": 20, "count": 5, "avg": 4}
    answer = _mean(a, x)

    assert truth == answer


def test_aggregate_count(data):
    """ Tests that the aggregate function returns the correct value.
    """
    group_field = "classification"
    agg_field = "temperature"
    agg_func = "COUNT"

    aggregator = aggregate(group_field, agg_field, agg_func)

    assert aggregator(data[0]) == {"A": 1}
    assert aggregator(data[1]) == {"A": 1, "B": 1}
    assert aggregator(data[2]) == {"A": 2, "B": 1}


def test_aggregate_min(data):
    """ Tests that the aggregate function returns the correct value for the
        minimum aggregation function.
    """
    group_field = "classification"
    agg_field = "temperature"
    agg_func = "MIN"

    aggregator = aggregate(group_field, agg_field, agg_func)

    assert aggregator(data[0]) == {"A": 100}
    assert aggregator(data[1]) == {"A": 100, "B": 50}
    assert aggregator(data[2]) == {"A": 100, "B": 50}
    assert aggregator(data[3]) == {"A": 100, "B": 50}
    assert aggregator(data[4]) == {"A": 50, "B": 50}
    assert aggregator(data[5]) == {"A": 50, "B": 25}


def test_aggregate_max(data):
    """ Tests that the aggregate function returns the correct value when the
        aggregator function is max.
    """
    group_field = "classification"
    agg_field = "temperature"
    agg_func = "MAX"

    aggregator = aggregate(group_field, agg_field, agg_func)

    assert aggregator(data[0]) == {"A": 100}
    assert aggregator(data[1]) == {"A": 100, "B": 50}
    assert aggregator(data[2]) == {"A": 100, "B": 50}
    assert aggregator(data[3]) == {"A": 100, "B": 50}
    assert aggregator(data[4]) == {"A": 100, "B": 50}
    assert aggregator(data[5]) == {"A": 100, "B": 50}


def test_aggregate_avg(data):
    """ Tests that the aggregate function returns the correct value when the
        aggregator is average.
    """
    group_field = "classification"
    agg_field = "temperature"
    agg_func = "AVG"

    aggregator = aggregate(group_field, agg_field, agg_func)

    assert aggregator(data[0]) == {
        "A": {
            "sum": 100,
            "count": 1,
            "avg": 100
        }
    }
    assert aggregator(data[1]) == {
        "A": {
            "sum": 100,
            "count": 1,
            "avg": 100
        },
        "B": {
            "sum": 50,
            "count": 1,
            "avg": 50
        }
    }
    assert aggregator(data[2]) == {
        "A": {
            "sum": 200,
            "count": 2,
            "avg": 100
        }, "B": {
            "sum": 50,
            "count": 1,
            "avg": 50
        }
    }


def test_aggregate_nan_agg_field():
    """ Tests that the aggregate function returns the correct value when the
        aggregated field is NaN.
    """

    datum = {"classification": "A", "temperature": math.nan}

    aggregator = aggregate("classification", "temperature", "MAX")

    assert aggregator(datum) == {}


def test_aggregate_none_agg_field():
    """ Tests that the aggregate function returns the correct value when the
        aggregated field is None.
    """

    datum = {"classification": "A", "temperature": None}

    aggregator = aggregate("classification", "temperature", "MAX")

    assert aggregator(datum) == {}


def test_aggregate_none_group_field():
    """ Tests that the aggregate function returns the correct value when the
        group field is None.
    """

    datum = {"classification": None, "temperature": 98.6}

    aggregator = aggregate("classification", "temperature", "MAX")

    assert aggregator(datum) == {"null": 98.6}


def test_color(data):
    """ Tests that the color function returns the correct value.
    """
    color_field = "classification"

    def transformer():
        return append("date", "temperature")

    color_transformer = color(color_field, transformer)

    assert color_transformer(data[0]) == {
        "A": {
            "date": ["2018-08-01"],
            "temperature": [100]
        }
    }
    assert color_transformer(data[1]) == {
        "A": {
            "date": ["2018-08-01"],
            "temperature": [100]
        },
        "B": {
            "date": ["2017-10-01"],
            "temperature": [50]
        }
    }
    assert color_transformer(data[2]) == {
        "A": {
            "date": ["2018-08-01", "2017-06-01"],
            "temperature": [100, 100]
        },
        "B": {
            "date": ["2017-10-01"],
            "temperature": [50]
        }
    }


def test_plot_to_reducer_histogram(data):
    """ Tests that the plot_to_reducer function returns the correct value
        for histogram plots.
    """
    svl_plot = {
        "type": "histogram",
        "field": "temperature"
    }

    reducer = plot_to_reducer(svl_plot)

    assert reducer(data[0]) == {"temperature": [100]}
    assert reducer(data[1]) == {"temperature": [100, 50]}
    assert reducer(data[2]) == {"temperature": [100, 50, 100]}


def test_plot_to_reducer_temporal_x_count_y(data):
    """ Tests that the plot_to_reducer function returns the correct value
        when there's a temporal transformation on x and a count aggregation
        on y.
    """
    svl_plot = {
        "type": "line",
        "x": {
            "field": "date",
            "temporal": "YEAR"
        },
        "y": {
            "agg": "COUNT",
            "field": "date"
        }
    }

    reducer = plot_to_reducer(svl_plot)

    assert reducer(data[0]) == {"2018-01-01T00:00:00Z": 1}
    assert reducer(data[1]) == {
        "2018-01-01T00:00:00Z": 1,
        "2017-01-01T00:00:00Z": 1
    }
    assert reducer(data[2]) == {
        "2018-01-01T00:00:00Z": 1,
        "2017-01-01T00:00:00Z": 2
    }


def test_plot_to_reducer_temporal_y_min_x(data):
    """ Tests that the plot_to_reducer function returns the correct value
        when there's a temporal transformation on y and a min aggregation
        on x.
    """
    svl_plot = {
        "type": "bar",
        "x": {
            "agg": "MIN",
            "field": "temperature"
        },
        "y": {
            "temporal": "YEAR",
            "field": "date"
        }
    }

    reducer = plot_to_reducer(svl_plot)

    assert reducer(data[0]) == {"2018-01-01T00:00:00Z": 100}
    assert reducer(data[1]) == {
        "2018-01-01T00:00:00Z": 100,
        "2017-01-01T00:00:00Z": 50
    }
    assert reducer(data[2]) == {
        "2018-01-01T00:00:00Z": 100,
        "2017-01-01T00:00:00Z": 50
    }


def test_plot_to_reducer_color_append_x_append_y(data):
    """ Tests that the plot_to_reducer function returns the correct value when
        there's a color field and append aggregators for x and y.
    """
    svl_plot = {
        "type": "scatter",
        "x": {
            "field": "date",
            "temporal": "DAY"
        },
        "y": {
            "field": "temperature"
        },
        "color": {
            "field": "classification"
        }
    }

    reducer = plot_to_reducer(svl_plot)

    assert reducer(data[0]) == {
        "A": {
            "date": ["2018-08-01T00:00:00Z"],
            "temperature": [100]
        }
    }
    assert reducer(data[1]) == {
        "A": {
            "date": ["2018-08-01T00:00:00Z"],
            "temperature": [100]
        },
        "B": {
            "date": ["2017-10-01T00:00:00Z"],
            "temperature": [50]
        }
    }
    assert reducer(data[2]) == {
        "A": {
            "date": ["2018-08-01T00:00:00Z", "2017-06-01T00:00:00Z"],
            "temperature": [100, 100]
        },
        "B": {
            "date": ["2017-10-01T00:00:00Z"],
            "temperature": [50]
        }
    }


def test_plot_to_reducer_color_group_x_max_y(data):
    """ Tests that the plot_to_reducer function returns the correct value when
        there's a color field, a group on x and a minimum agg function on y.
    """
    svl_plot = {
        "type": "bar",
        "x": {
            "field": "temperature",
            "agg": "MAX"
        },
        "y": {
            "field": "date",
            "temporal": "YEAR"
        },
        "color": {
            "field": "classification"
        }
    }

    reducer = plot_to_reducer(svl_plot)

    assert reducer(data[0]) == {"A": {"2018-01-01T00:00:00Z": 100}}
    assert reducer(data[1]) == {
        "A": {"2018-01-01T00:00:00Z": 100},
        "B": {"2017-01-01T00:00:00Z": 50}
    }
    assert reducer(data[2]) == {
        "A": {
            "2018-01-01T00:00:00Z": 100,
            "2017-01-01T00:00:00Z": 100
        },
        "B": {
            "2017-01-01T00:00:00Z": 50
        }
    }
    assert reducer(data[3]) == {
        "A": {
            "2018-01-01T00:00:00Z": 100,
            "2017-01-01T00:00:00Z": 100
        },
        "B": {
            "2017-01-01T00:00:00Z": 50,
            "2018-01-01T00:00:00Z": 50
        }
    }
    assert reducer(data[4]) == {
        "A": {
            "2018-01-01T00:00:00Z": 100,
            "2017-01-01T00:00:00Z": 100
        },
        "B": {
            "2017-01-01T00:00:00Z": 50,
            "2018-01-01T00:00:00Z": 50
        }
    }


def test_plot_to_reducer_temporal_color_group_x_mean_y(data):
    """ Tests that the plot_to_reducer function returns the correct value
        when there's a temporal converter on the color field and a mean
        aggregation on the y field.
    """
    svl_plot = {
        "type": "bar",
        "x": {
            "field": "classification"
        },
        "y": {
            "agg": "AVG",
            "field": "temperature"
        },
        "color": {
            "field": "date",
            "temporal": "YEAR"
        }
    }

    reducer = plot_to_reducer(svl_plot)

    assert reducer(data[0]) == {
        "2018-01-01T00:00:00Z": {"A": {"sum": 100, "count": 1, "avg": 100}}
    }
    assert reducer(data[1]) == {
        "2018-01-01T00:00:00Z": {"A": {"sum": 100, "count": 1, "avg": 100}},
        "2017-01-01T00:00:00Z": {"B": {"sum": 50, "count": 1, "avg": 50}}
    }
    assert reducer(data[2]) == {
        "2018-01-01T00:00:00Z": {
            "A": {"sum": 100, "count": 1, "avg": 100}
        },
        "2017-01-01T00:00:00Z": {
            "A": {"sum": 100, "count": 1, "avg": 100},
            "B": {"sum": 50, "count": 1, "avg": 50}
        }
    }
    assert reducer(data[3]) == {
        "2018-01-01T00:00:00Z": {
            "A": {"sum": 100, "count": 1, "avg": 100},
            "B": {"sum": 50, "count": 1, "avg": 50}
        },
        "2017-01-01T00:00:00Z": {
            "A": {"sum": 100, "count": 1, "avg": 100},
            "B": {"sum": 50, "count": 1, "avg": 50}
        }
    }
    assert reducer(data[4]) == {
        "2018-01-01T00:00:00Z": {
            "A": {"sum": 150, "count": 2, "avg": 75},
            "B": {"sum": 50, "count": 1, "avg": 50}
        },
        "2017-01-01T00:00:00Z": {
            "A": {"sum": 100, "count": 1, "avg": 100},
            "B": {"sum": 50, "count": 1, "avg": 50}
        }
    }
    assert reducer(data[5]) == {
        "2018-01-01T00:00:00Z": {
            "A": {"sum": 150, "count": 2, "avg": 75},
            "B": {"sum": 75, "count": 2, "avg": 37.5}
        },
        "2017-01-01T00:00:00Z": {
            "A": {"sum": 100, "count": 1, "avg": 100},
            "B": {"sum": 50, "count": 1, "avg": 50}
        }
    }
    assert reducer(data[6]) == {
        "2018-01-01T00:00:00Z": {
            "A": {"sum": 150, "count": 2, "avg": 75},
            "B": {"sum": 75, "count": 2, "avg": 37.5}
        },
        "2017-01-01T00:00:00Z": {
            "A": {"sum": 175, "count": 2, "avg": 87.5},
            "B": {"sum": 50, "count": 1, "avg": 50}
        }
    }
    assert reducer(data[7]) == {
        "2018-01-01T00:00:00Z": {
            "A": {"sum": 150, "count": 2, "avg": 75},
            "B": {"sum": 75, "count": 2, "avg": 37.5}
        },
        "2017-01-01T00:00:00Z": {
            "A": {"sum": 175, "count": 2, "avg": 87.5},
            "B": {"sum": 150, "count": 2, "avg": 75}
        }
    }


def test_construct_data(data):
    """ Tests that the construct_data function returns the correct value.
    """
    svl_plots = [
        {
            "type": "bar",
            "x": {"field": "classification"},
            "y": {"agg": "COUNT", "field": "classification"}
        }, {
            "type": "line",
            "x": {"field": "date", "temporal": "YEAR"},
            "y": {"agg": "MIN", "field": "temperature"},
            "color": {"field": "classification"}
        }, {
            "type": "histogram",
            "field": "temperature"
        }, {
            "type": "scatter",
            "x": {"field": "date", "temporal": "MONTH"},
            "y": {"field": "temperature"}
        }
    ]

    constructed_data_truth = [
        {
            "A": 4,
            "B": 4
        }, {
            "A": {"2017-01-01T00:00:00Z": 75, "2018-01-01T00:00:00Z": 50},
            "B": {"2017-01-01T00:00:00Z": 50, "2018-01-01T00:00:00Z": 25}
        }, {
            "temperature": [100, 50, 100, 50, 50, 25, 75, 100]
        }, {
            "date": [
                "2018-08-01T00:00:00Z",
                "2017-10-01T00:00:00Z",
                "2017-06-01T00:00:00Z",
                "2018-03-01T00:00:00Z",
                "2018-12-01T00:00:00Z",
                "2018-01-01T00:00:00Z",
                "2017-04-01T00:00:00Z",
                "2017-06-01T00:00:00Z"
            ],
            "temperature": [100, 50, 100, 50, 50, 25, 75, 100]
        }
    ]

    constructed_data_answer = construct_data(svl_plots, data)

    assert constructed_data_truth == constructed_data_answer


@given(
    # Generated test data is lists of dictionaries. There's no point in testing
    # the empty case because the function won't be called.
    generated_data=generate_data()
)
def test_append_properties(generated_data):
    """ Tests that the append function produces a dict with the correct
        fields, and that the lengths of the fields are the same.
    """
    appender = append("date", "temperature")

    result = None
    for datum in generated_data:
        result = appender(datum)

    assert "date" in result
    assert "temperature" in result
    assert len(result.keys()) == 2
    assert len(result["date"]) == len(result["temperature"])


@given(
    # This function will not be called on empty lists.
    generated_data=lists(floats()).filter(lambda x: len(x) > 0)
)
def test_mean_properties(generated_data):
    """ Tests that the _mean function produces a dict with the correct fields
        with counts greater than zero and the correct calculated average.
    """
    accumulator = {
        "sum": 0,
        "count": 0,
        "avg": math.nan
    }

    for datum in generated_data:
        accumulator = _mean(accumulator, datum)

    assert "sum" in accumulator
    assert "count" in accumulator
    assert len(accumulator.keys()) == 3
    assert accumulator["count"] == len(
        list(filter(lambda x: not math.isnan(x), generated_data))
    )
    # If the only values generated are nans, then that means no counters were
    # active, which would fail the test. Use math.isnan to short circuit around
    # the zero division error.
    assert math.isnan(accumulator["avg"]) or (
        accumulator["avg"] == (accumulator["sum"] / accumulator["count"])
    )


@given(
    generated_data=generate_data()
)
def test_aggregate_properties_count(generated_data):
    """ Tests that the aggregate function produces a dict with the correct
        fields and values, and ensures that each iteration produces a count
        that's one greater than the last for that field.
    """
    aggregator = aggregate("classification", "classification", "COUNT")
    accumulator = {}

    classifications = set()

    for datum in generated_data:
        current_value = get(datum["classification"], accumulator, 0)
        accumulator = aggregator(datum)

        classifications.add(datum["classification"])
        assert (accumulator[datum["classification"]] - current_value) == 1

    assert len(classifications ^ set(accumulator.keys())) == 0


@given(
    generated_data=generate_data()
)
def test_aggregate_properties_min(generated_data):
    """ Tests that the aggregate function produces a dict with the correct
        fields and values, and ensures that each iteration produces a
        dict with the value lower than or equal to the data point.
    """
    aggregator = aggregate("classification", "temperature", "MIN")
    accumulator = {}

    classifications = set()

    for datum in generated_data:

        # We should be able to handle NaNs.
        accumulator = aggregator(datum)

        # But we don't need to check the rest.
        if math.isnan(datum["temperature"]):
            continue

        classifications.add(datum["classification"])

        # Check that the accumulator is always less than or equal to the new
        # data point.
        assert accumulator[datum["classification"]] <= datum["temperature"]

    assert len(classifications ^ set(accumulator.keys())) == 0


@given(
    generated_data=generate_data()
)
def test_aggregate_properties_max(generated_data):
    """ Tests that the aggregate function produces a dict with the correct
        fields and values, and ensures that each iteration produces a dict with
        the aggregated value higher than or equal to the data point.
    """
    aggregator = aggregate("classification", "temperature", "MAX")
    accumulator = {}

    classifications = set()

    for datum in generated_data:

        # We should be able to handle NaNs.
        accumulator = aggregator(datum)

        if math.isnan(datum["temperature"]):
            continue

        classifications.add(datum["classification"])

        # Check that the accumulator is always greater than or equal to the new
        # data point.
        assert accumulator[datum["classification"]] >= datum["temperature"]

    # Check that the accumulator accumulated the correct group field values.
    assert len(classifications ^ set(accumulator.keys())) == 0


@given(
    generated_data=generate_data()
)
def test_aggregate_properties_mean(generated_data):
    """ Tests that the aggregate function produces a dict with the correct
        fields and values, and ensures that each iteration increments the total
        count in the accumulator.
    """
    aggregator = aggregate("classification", "temperature", "AVG")
    accumulator = {}

    classifications = set()

    for datum in generated_data:

        current_count = get_in(
            [datum["classification"], "count"],
            accumulator,
            0
        )

        # We should be able to handle NaNs.
        accumulator = aggregator(datum)

        if math.isnan(datum["temperature"]):
            continue

        classifications.add(datum["classification"])

        # Check that the accumulator is always incrementing the counter.
        new_count = get_in(
            [datum["classification"], "count"],
            accumulator,
            0
        )

        assert (new_count - current_count) == 1

    # Check that the accumulator accumulated the correct group field values.
    assert len(classifications ^ set(accumulator.keys())) == 0


@given(
    generated_data=generate_data()
)
def test_color_properties(generated_data):
    """ Tests that the color function returns a dict with the correct fields
        that applies the accumulator appropriately.
    """

    def transformer():
        return append("temperature")

    color_aggregator = color("classification", transformer)
    accumulator = {}

    classifications = set()

    for datum in generated_data:
        accumulator = color_aggregator(datum)

        classifications.add(datum["classification"])

    assert len(classifications ^ set(accumulator.keys())) == 0
