from svl.sqlite import svl_to_sql


def test_svl_to_sql():
    """ Tests that the svl_to_sql function returns the correct value when there
        are no aggregations or colors.
    """
    svl_plot = {
        "data": "bigfoot",
        "x": {
            "field": "latitude"
        },
        "y": {
            "field": "temperature_mid"
        }
    }

    truth_query = "SELECT ?, ? FROM ?"

    truth_variables = ["latitude", "temperature_mid", "bigfoot"]

    answer_query, answer_variables = svl_to_sql(svl_plot)

    assert truth_query == answer_query
    assert truth_variables == answer_variables


def test_svl_to_sql_agg_x():
    """ Tests that the svl_to_sql function returns the correct value when x is
        aggregated.
    """
    svl_plot = {
        "data": "bigfoot",
        "x": {
            "field": "classification"
        },
        "y": {
            "agg": "MAX",
            "field": "temperature"
        }
    }

    truth_query = "SELECT ?, MAX(?) AS ? FROM ? GROUP BY ?"
    truth_variables = [
        "classification",
        "temperature",
        "max_temperature",
        "bigfoot",
        "classification"
    ]

    answer_query, answer_variables = svl_to_sql(svl_plot)

    assert truth_query == answer_query
    assert truth_variables == answer_variables


def test_svl_to_sql_agg_y():
    """ Tests that the svl_to_sql function returns the correct value when
        there's an aggregation on y and no aggregation on colors.
    """
    svl_plot = {
        "data": "bigfoot",
        "x": {
            "agg": "AVG",
            "field": "temperature"
        },
        "y": {
            "field": "classification"
        }
    }

    truth_query = "SELECT AVG(?) AS ?, ? FROM ? GROUP BY ?"
    truth_variables = [
        "temperature",
        "avg_temperature",
        "classification",
        "bigfoot",
        "classification"
    ]

    answer_query, answer_variables = svl_to_sql(svl_plot)

    assert truth_query == answer_query
    assert truth_variables == answer_variables


def test_svl_to_sql_count():
    """ Tests that the svl_to_sql function returns the correct value when
        one of the aggregations is a count.
    """
    svl_plot = {
        "data": "bigfoot",
        "x": {
            "field": "classification"
        },
        "y": {
            "agg": "COUNT"
        }
    }

    truth_query = "SELECT ?, COUNT(?) AS ? FROM ? GROUP BY ?"
    truth_variables = [
        "classification",
        "*",
        "count_points",
        "bigfoot",
        "classification"
    ]

    answer_query, answer_variables = svl_to_sql(svl_plot)

    assert truth_query == answer_query
    assert truth_variables == answer_variables


def test_svl_to_sql_temporal():
    """ Tests that the svl_to_sql function returns the correct value when one
        of the fields has a temporal transformation.
    """
    svl_plot = {
        "data": "bigfoot",
        "x": {
            "field": "date",
            "temporal": "YEAR"
        },
        "y": {
            "field": "temperature"
        }
    }

    truth_query = "SELECT STRFTIME('%Y', ?) AS ?, ? FROM ?"
    truth_variables = [
        "date",
        "date",
        "temperature",
        "bigfoot"
    ]

    answer_query, answer_variables = svl_to_sql(svl_plot)

    assert truth_query == answer_query
    assert truth_variables == answer_variables


def test_svl_to_sql_temporal_agg():
    """ Tests that the svl_to_sql function returns the correct value when one
        field is a temporal transformation and the other is an aggregation.
    """
    svl_plot = {
        "data": "bigfoot",
        "x": {
            "field": "date",
            "temporal": "YEAR"
        },
        "y": {
            "agg": "COUNT"
        }
    }

    truth_query = (
        "SELECT STRFTIME('%Y', ?) AS ?, COUNT(?) AS ? FROM ? "
        "GROUP BY STRFTIME('%Y', ?)"
    )
    truth_variables = [
        "date",
        "date",
        "*",
        "count_points",
        "bigfoot",
        "date"
    ]

    answer_query, answer_variables = svl_to_sql(svl_plot)

    assert truth_query == answer_query
    assert truth_variables == answer_variables


def test_svl_to_sql_color():
    """ Tests that the svl_to_sql function returns the correct value when
        there's a color field.
    """
    svl_plot = {
        "data": "bigfoot",
        "x": {
            "field": "date"
        },
        "y": {
            "field": "temperature"
        },
        "color": {
            "field": "classification"
        }
    }

    truth_query = "SELECT ?, ?, ? FROM ?"
    truth_variables = [
        "date",
        "temperature",
        "classification",
        "bigfoot"
    ]

    answer_query, answer_variables = svl_to_sql(svl_plot)

    assert truth_query == answer_query
    assert truth_variables == answer_variables


def test_svl_to_sql_color_agg():
    """ Tests that the svl_to_sql function returns the correct value when
        there's a color field and an aggregation.
    """
    svl_plot = {
        "data": "bigfoot",
        "x": {
            "field": "date",
            "temporal": "YEAR"
        },
        "y": {
            "field": "temperature",
            "agg": "MAX"
        },
        "color": {
            "field": "classification"
        }
    }

    truth_query = (
        "SELECT STRFTIME('%Y', ?) AS ?, MAX(?) AS ?, ? FROM ? "
        "GROUP BY STRFTIME('%Y', ?), ?"
    )
    truth_variables = [
        "date",
        "date",
        "temperature",
        "max_temperature",
        "classification",
        "bigfoot",
        "date",
        "classification"
    ]

    answer_query, answer_variables = svl_to_sql(svl_plot)

    assert truth_query == answer_query
    assert truth_variables == answer_variables
