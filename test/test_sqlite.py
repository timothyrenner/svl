import pytest
import os
import pandas as pd

from pandas.testing import assert_frame_equal

from svl.sqlite import (
    _csv_to_sqlite_pandas,
    svl_to_sql
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


def test_csv_to_sqlite_pandas(test_file):
    """ Tests that the _csv_to_sqlite_pandas function loads the database with
        the correct values.
    """
    svl_plot = {
        "datasets": {
            "bigfoot": test_file
        }
    }

    truth = pd.read_csv(test_file)
    conn = _csv_to_sqlite_pandas(svl_plot)
    answer = pd.read_sql_query("SELECT * FROM bigfoot", conn)

    assert_frame_equal(truth, answer)


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

    truth_query = "SELECT ? AS x, ? AS y FROM ?"

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

    truth_query = "SELECT ? AS x, MAX(?) AS y FROM ? GROUP BY ?"
    truth_variables = [
        "classification",
        "temperature",
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

    truth_query = "SELECT AVG(?) AS x, ? AS y FROM ? GROUP BY ?"
    truth_variables = [
        "temperature",
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

    truth_query = "SELECT ? AS x, COUNT(?) AS y FROM ? GROUP BY ?"
    truth_variables = [
        "classification",
        "*",
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

    truth_query = "SELECT STRFTIME('%Y', ?) AS x, ? AS y FROM ?"
    truth_variables = [
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
        "SELECT STRFTIME('%Y', ?) AS x, COUNT(?) AS y FROM ? "
        "GROUP BY STRFTIME('%Y', ?)"
    )
    truth_variables = [
        "date",
        "*",
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

    truth_query = "SELECT ? AS x, ? AS y, ? AS color FROM ?"
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
        "SELECT STRFTIME('%Y', ?) AS x, MAX(?) AS y, ? AS color FROM ? "
        "GROUP BY STRFTIME('%Y', ?), ?"
    )
    truth_variables = [
        "date",
        "temperature",
        "classification",
        "bigfoot",
        "date",
        "classification"
    ]

    answer_query, answer_variables = svl_to_sql(svl_plot)

    assert truth_query == answer_query
    assert truth_variables == answer_variables
