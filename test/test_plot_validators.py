from svl.plot_validators import (
    _validate_xy_plot_has_x_and_y,
    validate_plot
)


def test_validate_xy_plot_has_x_and_y_pass():
    """ Tests that the _validate_xy_plot_has_x_and_y function returns the
        correct value when the plot passes.
    """
    svl_plot = {
        "data": "dogman",
        "type": "scatter",
        "x": {
            "field": "latitude"
        },
        "y": {
            "field": "temperature"
        }
    }

    ok, message = _validate_xy_plot_has_x_and_y(svl_plot)

    truth_ok = True
    truth_message = "Valid."

    assert truth_ok == ok
    assert truth_message == message


def test_validate_xy_plot_has_x_and_y_fail():
    """ Tests that the _validate_xy_plot_has_x_and_y function returns the
        correct value when the plot fails.
    """
    svl_plot = {
        "data": "bigfoot",
        "type": "line",
        "x": {
            "field": "date",
            "temporal": "YEAR"
        }
    }

    ok, message = _validate_xy_plot_has_x_and_y(svl_plot)

    truth_ok = False
    truth_message = "XY plot does not have X and Y."

    assert truth_ok == ok
    assert truth_message == message


def test_validate_xy_plot_has_x_and_y_non_xy_plot():
    """ Tests that the _validate_xy_plot_has_x_and_y function returns the
        correct value when the plot is not an XY plot.
    """
    svl_plot = {
        "data": "bigfoot",
        "type": "histogram",
        "x": {
            "field": "wind_speed"
        }
    }

    ok, message = _validate_xy_plot_has_x_and_y(svl_plot)

    truth_ok = True
    truth_message = "Valid."

    assert truth_ok == ok
    assert truth_message == message


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


def test_validate_plot_fail():
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
