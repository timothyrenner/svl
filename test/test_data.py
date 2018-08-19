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


def test_plot_to_reducer_temporal_y_min_x():
    """ Tests that the plot_to_reducer function returns the correct value
        when there's a temporal transformation on y and a min aggregation
        on x.
    """
    svl_plot = {
        "type": "bar",
        "x": {
            "agg": "MIN",
            "field": "price"
        },
        "y": {
            "temporal": "YEAR",
            "field": "date"
        }
    }

    data = [
        {"date": "2017-08-14", "price": 2.05},
        {"date": "2018-09-14", "price": 3.51},
        {"date": "2018-10-12", "price": 3.45}
    ]

    reducer = plot_to_reducer(svl_plot)

    assert reducer(data[0]) == {"2017-01-01T00:00:00Z": 2.05}
    assert reducer(data[1]) == {
        "2017-01-01T00:00:00Z": 2.05,
        "2018-01-01T00:00:00Z": 3.51
    }
    assert reducer(data[2]) == {
        "2017-01-01T00:00:00Z": 2.05,
        "2018-01-01T00:00:00Z": 3.45
    }


def test_plot_to_reducer_color_append_x_append_y():
    """ Tests that the plot_to_reducer function returns the correct value when
        there's a color field and append aggregators for x and y.
    """
    svl_plot = {
        "type": "scatter",
        "x": {
            "field": "latitude"
        },
        "y": {
            "field": "temperature"
        },
        "color": {
            "field": "classification"
        }
    }

    data = [
        {
            "latitude": 0.1,
            "temperature": 84.3,
            "classification": "A"
        }, {
            "latitude": 24.1,
            "temperature": 94.2,
            "classification": "B"
        }, {
            "latitude": 94.1,
            "temperature": -10.4,
            "classification": "A"
        }
    ]

    reducer = plot_to_reducer(svl_plot)

    assert reducer(data[0]) == {
        "A": {
            "latitude": [0.1],
            "temperature": [84.3]
        }
    }
    assert reducer(data[1]) == {
        "A": {
            "latitude": [0.1],
            "temperature": [84.3]
        },
        "B": {
            "latitude": [24.1],
            "temperature": [94.2]
        }
    }
    assert reducer(data[2]) == {
        "A": {
            "latitude": [0.1, 94.1],
            "temperature": [84.3, -10.4]
        },
        "B": {
            "latitude": [24.1],
            "temperature": [94.2]
        }
    }


def test_plot_to_reducer_color_group_x_max_y():
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
            "field": "state"
        },
        "color": {
            "field": "classification"
        }
    }

    data = [
        {"classification": "A", "state": "TX", "temperature": 85.0},
        {"classification": "B", "state": "LA", "temperature": 93.1},
        {"classification": "B", "state": "LA", "temperature": 81.2},
        {"classification": "B", "state": "TX", "temperature": 102.4}
    ]

    reducer = plot_to_reducer(svl_plot)

    assert reducer(data[0]) == {"A": {"TX": 85.0}}
    assert reducer(data[1]) == {
        "A": {"TX": 85.0},
        "B": {"LA": 93.1}
    }
    assert reducer(data[2]) == {
        "A": {"TX": 85.0},
        "B": {"LA": 93.1}
    }
    assert reducer(data[3]) == {
        "A": {"TX": 85.0},
        "B": {"TX": 102.4, "LA": 93.1}
    }


def test_plot_to_reducer_temporal_color_group_x_mean_y():
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

    data = [
        {"date": "2018-08-01", "classification": "A", "temperature": 100},
        {"date": "2017-10-01", "classification": "B", "temperature": 50},
        {"date": "2017-06-01", "classification": "A", "temperature": 100},
        {"date": "2018-03-21", "classification": "B", "temperature": 50},
        {"date": "2018-12-31", "classification": "A", "temperature": 50},
        {"date": "2018-01-01", "classification": "B", "temperature": 25},
        {"date": "2017-04-24", "classification": "A", "temperature": 75},
        {"date": "2017-06-12", "classification": "B", "temperature": 100}
    ]

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


def test_construct_data():
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

    data = [
        {"date": "2018-08-01", "classification": "A", "temperature": 100},
        {"date": "2017-10-01", "classification": "B", "temperature": 50},
        {"date": "2017-06-01", "classification": "A", "temperature": 100},
        {"date": "2018-03-21", "classification": "B", "temperature": 50},
        {"date": "2018-12-31", "classification": "A", "temperature": 50},
        {"date": "2018-01-01", "classification": "B", "temperature": 25},
        {"date": "2017-04-24", "classification": "A", "temperature": 75},
        {"date": "2017-06-12", "classification": "B", "temperature": 100}
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
