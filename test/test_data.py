from svl.data import (
    _convert_datetime,
    _mean,
    transform,
    append,
    aggregate,
    color,
    plot_to_reducer
)


def test_convert_datetime():
    """ Tests that the convert_datetime function returns the correct value.
    """

    dt = "2018-08-14"
    snap = "@mon"

    truth = "2018-08-01T00:00:00Z"

    answer = _convert_datetime(dt, snap=snap)

    assert truth == answer


def test_transform():
    """ Tests that the transform function returns the correct value.
    """

    field = "time"

    def transformation(x):
        return x+1

    datum = {"time": 1, "id": 2}

    truth = {"time": 2, "id": 2}
    answer = transform(field, transformation, datum)

    assert truth == answer


def test_append():
    """ Tests that the append function returns the correct value.
    """
    data = [
        {
            "x": 1,
            "y": 1
        }, {
            "x": 2,
            "y": 2
        }, {
            "x": 3,
            "y": 3
        }
    ]

    appender = append("x", "y")

    assert appender(data[0]) == {"x": [1], "y": [1]}
    assert appender(data[1]) == {"x": [1, 2], "y": [1, 2]}
    assert appender(data[2]) == {"x": [1, 2, 3], "y": [1, 2, 3]}


def test_mean():
    """ Tests that the _mean function returns the correct value.
    """
    a = {"sum": 10, "count": 4}
    x = 10

    truth = {"sum": 20, "count": 5, "avg": 4}
    answer = _mean(a, x)

    assert truth == answer


def test_aggregate_count():
    """ Tests that the aggregate function returns the correct value.
    """
    group_field = "x"
    agg_field = "y"
    agg_func = "COUNT"

    data = [
        {
            "x": "a",
            "y": 1
        }, {
            "x": "a",
            "y": 5
        }, {
            "x": "b",
            "y": 10
        }
    ]

    aggregator = aggregate(group_field, agg_field, agg_func)

    assert aggregator(data[0]) == {"a": 1}
    assert aggregator(data[1]) == {"a": 2}
    assert aggregator(data[2]) == {"a": 2, "b": 1}


def test_aggregate_min():
    """ Tests that the aggregate function returns the correct value for the
        minimum aggregation function.
    """
    group_field = "y"
    agg_field = "x"
    agg_func = "MIN"

    data = [
        {
            "x": 1,
            "y": "a"
        }, {
            "x": -1,
            "y": "a"
        }, {
            "x": -5,
            "y": "b"
        }
    ]

    aggregator = aggregate(group_field, agg_field, agg_func)

    assert aggregator(data[0]) == {"a": 1}
    assert aggregator(data[1]) == {"a": -1}
    assert aggregator(data[2]) == {"a": -1, "b": -5}


def test_aggregate_max():
    """ Tests that the aggregate function returns the correct value when the
        aggregator function is max.
    """
    group_field = "x"
    agg_field = "y"
    agg_func = "MAX"

    data = [
        {
            "x": "a",
            "y": -1
        }, {
            "x": "a",
            "y": 1
        }, {
            "x": "b",
            "y": -10
        }
    ]

    aggregator = aggregate(group_field, agg_field, agg_func)

    assert aggregator(data[0]) == {"a": -1}
    assert aggregator(data[1]) == {"a": 1}
    assert aggregator(data[2]) == {"a": 1, "b": -10}


def test_aggregate_avg():
    """ Tests that the aggregate function returns the correct value when the
        aggregator is average.
    """
    group_field = "x"
    agg_field = "y"
    agg_func = "AVG"

    data = [
        {
            "x": "a",
            "y": 5
        }, {
            "x": "a",
            "y": 15
        }, {
            "x": "b",
            "y": 5
        }
    ]

    aggregator = aggregate(group_field, agg_field, agg_func)

    assert aggregator(data[0]) == {
        "a": {
            "sum": 5,
            "count": 1,
            "avg": 5
        }
    }
    assert aggregator(data[1]) == {
        "a": {
            "sum": 20,
            "count": 2,
            "avg": 10
        }
    }
    assert aggregator(data[2]) == {
        "a": {
            "sum": 20,
            "count": 2,
            "avg": 10
        }, "b": {
            "sum": 5,
            "count": 1,
            "avg": 5
        }
    }


def test_color():
    """ Tests that the color function returns the correct value.
    """
    color_field = "z"

    def transformer():
        return append("x", "y")

    data = [
        {
            "x": "a",
            "y": 1,
            "z": "X"
        }, {
            "x": "a",
            "y": 2,
            "z": "Y"
        }, {
            "x": "b",
            "y": 1,
            "z": "X"
        }
    ]

    color_transformer = color(color_field, transformer)

    assert color_transformer(data[0]) == {
        "X": {
            "x": ["a"],
            "y": [1]
        }
    }
    assert color_transformer(data[1]) == {
        "X": {
            "x": ["a"],
            "y": [1]
        },
        "Y": {
            "x": ["a"],
            "y": [2]
        }
    }
    assert color_transformer(data[2]) == {
        "X": {
            "x": ["a", "b"],
            "y": [1, 1]
        },
        "Y": {
            "x": ["a"],
            "y": [2]
        }
    }


def test_plot_to_reducer_histogram():
    """ Tests that the plot_to_reducer function returns the correct value
        for histogram plots.
    """
    svl_plot = {
        "type": "histogram",
        "field": "x"
    }

    data = [
        {"x": 1},
        {"x": -1},
        {"x": 2}
    ]

    reducer = plot_to_reducer(svl_plot)

    assert reducer(data[0]) == {"x": [1]}
    assert reducer(data[1]) == {"x": [1, -1]}
    assert reducer(data[2]) == {"x": [1, -1, 2]}


def test_plot_to_reducer_temporal_x_count_y():
    """ Tests that the plot_to_reducer function returns the correct value
        when there's a temporal transformation on x and a count aggregation
        on y.
    """
    svl_plot = {
        "type": "line",
        "x": {
            "field": "time",
            "temporal": "MONTH"
        },
        "y": {
            "agg": "COUNT",
            "field": "time"
        }
    }

    data = [
        {"time": "2018-08-01", "id": 1},
        {"time": "2018-10-02", "id": 2},
        {"time": "2018-08-04", "id": 3}
    ]

    reducer = plot_to_reducer(svl_plot)

    assert reducer(data[0]) == {"2018-08-01T00:00:00Z": 1}
    assert reducer(data[1]) == {
        "2018-08-01T00:00:00Z": 1,
        "2018-10-01T00:00:00Z": 1
    }
    assert reducer(data[2]) == {
        "2018-08-01T00:00:00Z": 2,
        "2018-10-01T00:00:00Z": 1
    }
