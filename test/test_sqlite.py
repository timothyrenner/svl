import pytest
import os
import pandas as pd

from pandas.testing import assert_frame_equal

from svl.sqlite import (
    _csv_to_sqlite_pandas,
    svl_to_sql_xy,
    get_svl_data
)


@pytest.fixture()
def test_file():
    current_dir = os.path.dirname(
        os.path.abspath(__file__)
    )
    test_file = os.path.join(
        current_dir,
        "test_datasets",
        "bigfoot_sightings.csv"
    )
    return test_file


@pytest.fixture()
def test_conn(test_file):
    # Obviously don't need the whole plot just the bit about the file.
    test_svl_datasets = {
        "bigfoot": test_file
    }

    conn = _csv_to_sqlite_pandas(test_svl_datasets)
    yield conn
    conn.close()


def test_csv_to_sqlite_pandas(test_file):
    """ Tests that the _csv_to_sqlite_pandas function loads the database with
        the correct values.
    """
    svl_datasets = {
        "bigfoot": test_file
    }

    truth = pd.read_csv(test_file)
    conn = _csv_to_sqlite_pandas(svl_datasets)
    answer = pd.read_sql_query("SELECT * FROM bigfoot", conn)

    assert_frame_equal(truth, answer)


def test_svl_to_sql_xy():
    """ Tests that the svl_to_sql_xy function returns the correct value when there
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

    truth_query = "SELECT latitude AS x, temperature_mid AS y FROM bigfoot"

    answer_query = svl_to_sql_xy(svl_plot)

    assert truth_query == answer_query


def test_svl_to_sql_xy_agg_x():
    """ Tests that the svl_to_sql_xy function returns the correct value when x is
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

    truth_query = "SELECT classification AS x, MAX(temperature) AS y " \
        "FROM bigfoot GROUP BY classification"

    answer_query = svl_to_sql_xy(svl_plot)

    assert truth_query == answer_query


def test_svl_to_sql_xy_agg_y():
    """ Tests that the svl_to_sql_xy function returns the correct value when
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

    truth_query = "SELECT AVG(temperature) AS x, classification AS y " \
        "FROM bigfoot GROUP BY classification"

    answer_query = svl_to_sql_xy(svl_plot)

    assert truth_query == answer_query


def test_svl_to_sql_xy_count():
    """ Tests that the svl_to_sql_xy function returns the correct value when
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

    truth_query = "SELECT classification AS x, COUNT(*) AS y "\
        "FROM bigfoot GROUP BY classification"

    answer_query = svl_to_sql_xy(svl_plot)

    assert truth_query == answer_query


def test_svl_to_sql_xy_temporal():
    """ Tests that the svl_to_sql_xy function returns the correct value when one
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

    truth_query = "SELECT STRFTIME('%Y', date) AS x, temperature AS y "\
        "FROM bigfoot"

    answer_query = svl_to_sql_xy(svl_plot)

    assert truth_query == answer_query


def test_svl_to_sql_xy_temporal_agg():
    """ Tests that the svl_to_sql_xy function returns the correct value when one
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
        "SELECT STRFTIME('%Y', date) AS x, COUNT(*) AS y FROM bigfoot "
        "GROUP BY STRFTIME('%Y', date)"
    )

    answer_query = svl_to_sql_xy(svl_plot)

    assert truth_query == answer_query


def test_svl_to_sql_xy_color():
    """ Tests that the svl_to_sql_xy function returns the correct value when
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

    truth_query = "SELECT date AS x, temperature AS y, "\
        "classification AS color FROM bigfoot"

    answer_query = svl_to_sql_xy(svl_plot)

    assert truth_query == answer_query


def test_svl_to_sql_xy_color_agg():
    """ Tests that the svl_to_sql_xy function returns the correct value when
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
        "SELECT STRFTIME('%Y', date) AS x, MAX(temperature) AS y, "
        "classification AS color FROM bigfoot "
        "GROUP BY STRFTIME('%Y', date), classification"
    )

    answer_query = svl_to_sql_xy(svl_plot)

    assert truth_query == answer_query


def test_get_svl_xy_data(test_conn):
    """ Tests that the get_svl_data function returns the correct value. """
    svl_plot = {
        "data": "bigfoot",
        "type": "line",
        "x": {
            "field": "date",
            "temporal": "YEAR"
        },
        "y": {
            "agg": "COUNT"
        }
    }

    answer = get_svl_data(svl_plot, test_conn)

    assert "x" in answer
    assert "y" in answer
    assert len(answer["x"]) == len(answer["y"])


def test_get_svl_xy_data_color(test_conn):
    """ Tests that the get_svl_data function returns the correct value when
        there's a color field.
    """
    svl_plot = {
        "data": "bigfoot",
        "type": "bar",
        "x": {
            "field": "date",
            "temporal": "YEAR"
        },
        "y": {
            "agg": "COUNT"
        },
        "color": {
            "field": "classification"
        }
    }

    answer = get_svl_data(svl_plot, test_conn)
    for color in ["Class A", "Class B"]:
        assert color in answer
        assert "x" in answer[color]
        assert "y" in answer[color]
        assert len(answer[color]["x"]) == len(answer[color]["y"])
