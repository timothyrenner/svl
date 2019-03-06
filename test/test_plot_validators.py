from svl.plot_validators import validate_plot


def test_validate_plot_pass():
    """ Tests that the validate_plot function returns the correct value when
        the plot passes.
    """
    svl_plot = {
        "type": "histogram",
        "data": "bigfoot",
        "y": {
            "field": "humidity"
        }
    }

    ok, message = validate_plot(svl_plot)

    truth_ok = True
    truth_message = ""

    assert truth_ok == ok
    assert truth_message == message


def test_validate_plot_xy_must_have_x_and_y():
    """ Tests that the validate_plot function returns the correct value when
        the plot fails.
    """
    svl_plot = {
        "type": "bar",
        "data": "bigfoot",
        "x": {
            "field": "classification"
        }
    }

    ok, message = validate_plot(svl_plot)

    truth_ok = False
    truth_message = "XY plot does not have X and Y."

    assert truth_ok == ok
    assert truth_message == message


def test_validate_plot_histogram_cannot_have_step_and_bins():
    """ Tests that the validate_plot function returns the correct value when
        the plot is a histogram that has a STEP and BINS declaration.
    """
    svl_plot = {
        "type": "histogram",
        "data": "bigfoot",
        "x": {
            "field": "wind_speed"
        },
        "step": 10,
        "bins": 100
    }

    ok, message = validate_plot(svl_plot)

    truth_ok = False
    truth_message = "Histogram cannot have STEP and BINS."

    assert truth_ok == ok
    assert truth_message == message


def test_validate_plot_xy_cannot_have_aggs_on_x_and_y():
    """ Tests that the validate_Plot function returns the correct value when
        the plot is an XY plot that has an agg on X and Y.
    """
    svl_plot = {
        "type": "scatter",
        "data": "bigfoot",
        "x": {
            "field": "latitude",
            "agg": "MAX"
        },
        "y": {
            "field": "humidity",
            "agg": "MIN"
        }
    }

    ok, message = validate_plot(svl_plot)

    truth_ok = False
    truth_message = "XY plot cannot have an aggregation on X and Y."

    assert truth_ok == ok
    assert truth_message == message


def test_validate_plot_histogram_and_pie_cannot_have_aggs():
    """ Tests that the validate_plot function returns the correct value when
        the plot is a histogram or pie chart with an aggregation.
    """
    svl_plot = {
        "type": "pie",
        "data": "bigfoot",
        "axis": {
            "field": "classification",
            "agg": "COUNT"
        }
    }

    ok, message = validate_plot(svl_plot)

    truth_ok = False
    truth_message = "Histograms and pie charts cannot have aggregations."

    assert truth_ok == ok
    assert truth_message == message


def test_validate_plot_histogram_and_pie_cannot_have_temporals():
    """ Tests that the validate_plot function returns the correct value when
        the plot is a histogram or pie chart with a temporal axis.
    """
    svl_plot = {
        "type": "histogram",
        "data": "bigfoot",
        "x": {
            "field": "date",
            "temporal": "YEAR"
        }
    }

    ok, message = validate_plot(svl_plot)

    truth_ok = False
    truth_message = "Histograms and pie charts cannot have temporal axes."

    assert truth_ok == ok
    assert truth_message == message


def test_validate_plot_histogram_cannot_have_x_and_y():
    """ Tests that the validate_plot function returns the correct value when
        the plot is a histogram with x and y.
    """
    svl_plot = {
        "type": "histogram",
        "data": "bigfoot",
        "x": {
            "field": "humidity"
        },
        "y": {
            "field": "wind_speed"
        }
    }

    ok, message = validate_plot(svl_plot)

    truth_ok = False
    truth_message = "Histograms can have X or Y, not both."

    assert truth_ok == ok
    assert truth_message == message


def test_validate_plot_histogram_must_have_x_or_y():
    """ Tests that the validate_plot function returns the correct value when
        the plot is a histogram without an X or Y.
    """
    svl_plot = {
        "type": "histogram",
        "data": "bigfoot",
        "bins": 10
    }

    ok, message = validate_plot(svl_plot)

    truth_ok = False
    truth_message = "Histograms must have an X or Y."

    assert truth_ok == ok
    assert truth_message == message


def test_validate_plot_pie_must_have_axis():
    """ Tests that the validate_plot function returns the correct value when
        the plot is a pie chart without an AXIS.
    """
    svl_plot = {
        "type": "pie",
        "data": "bigfoot",
        "hole": 0.3
    }

    ok, message = validate_plot(svl_plot)

    truth_ok = False
    truth_message = "Pie charts must have an axis."

    assert truth_ok == ok
    assert truth_message == message


def test_validate_plot_cannot_sort_on_both_axes():
    """ Tests that the validate_plot function returns the correct value when
        the plot has sort on X and Y.
    """
    svl_plot = {
        "type": "line",
        "data": "bigfoot",
        "x": {
            "field": "date",
            "temporal": "YEAR",
            "sort": "DESC"
        }, "y": {
            "field": "classification",
            "agg": "COUNT",
            "sort": "ASC"
        }
    }

    ok, message = validate_plot(svl_plot)

    truth_ok = False
    truth_message = "Cannot sort by two axes."

    assert truth_ok == ok
    assert truth_message == message


def test_validate_plot_hole_not_between_zero_and_one():
    """ Tests that the validate_plot function returns the correct value when
        the plot has a HOLE that's not between zero and one.
    """
    svl_plot = {
        "type": "pie",
        "data": "bigfoot",
        "axis": {
            "field": "has_location"
        },
        "hole": 1.2
    }

    ok, message = validate_plot(svl_plot)

    truth_ok = False
    truth_message = "HOLE must be between zero and one."

    assert truth_ok == ok
    assert truth_message == message
