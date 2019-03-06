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
