import pytest
import os
import pandas as pd

from pandas.testing import assert_frame_equal

from svl.sqlite import (
    _csv_to_sqlite_pandas,
    svl_to_sql_xy,
    svl_to_sql_hist,
    svl_to_sql_pie,
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


def test_svl_to_sql_hist():
    """ Tests that the svl_to_sql_hist function returns the correct value.
    """
    svl_plot = {
        "data": "bigfoot",
        "type": "histogram",
        "field": "temperature_mid",
        "bins": 25
    }

    truth_query = "SELECT temperature_mid AS x FROM bigfoot"

    answer_query = svl_to_sql_hist(svl_plot)

    assert truth_query == answer_query


def test_svl_to_sql_pie():
    """ Tests that the svl_to_sql_pie function returns the correct value.
    """
    svl_plot = {
        "data": "bigfoot",
        "field": "classification",
    }

    truth_query = \
        "SELECT classification AS label, COUNT(*) AS value FROM bigfoot"

    answer_query = svl_to_sql_pie(svl_plot)

    assert truth_query == answer_query


def test_svl_to_sql_xy():
    """ Tests that the svl_to_sql_xy function returns the correct value when
        there are no aggregations or colors.
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


def test_svl_to_sql_xy_split_by():
    """ Tests that the svl_to_sql_xy function returns the correct value when
        there's a split by field.
    """
    svl_plot = {
        "data": "bigfoot",
        "x": {
            "field": "date"
        },
        "y": {
            "field": "temperature"
        },
        "split_by": {
            "field": "classification"
        }
    }

    truth_query = "SELECT date AS x, temperature AS y, "\
        "classification AS split_by FROM bigfoot"

    answer_query = svl_to_sql_xy(svl_plot)

    assert truth_query == answer_query


def test_svl_to_sql_xy_split_by_agg():
    """ Tests that the svl_to_sql_xy function returns the correct value when
        there's a split by field and an aggregation.
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
        "split_by": {
            "field": "classification"
        }
    }

    truth_query = (
        "SELECT STRFTIME('%Y', date) AS x, MAX(temperature) AS y, "
        "classification AS split_by FROM bigfoot "
        "GROUP BY STRFTIME('%Y', date), classification"
    )

    answer_query = svl_to_sql_xy(svl_plot)

    assert truth_query == answer_query


def test_get_svl_data_xy(test_conn):
    """ Tests that the get_svl_data function returns the correct value for
        an xy plot.
    """
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


def test_get_svl_data_xy_split_by(test_conn):
    """ Tests that the get_svl_data function returns the correct value when
        there's a split by field for an xy plot.
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
        "split_by": {
            "field": "classification"
        }
    }

    answer = get_svl_data(svl_plot, test_conn)
    for split_by in ["Class A", "Class B"]:
        assert split_by in answer
        assert "x" in answer[split_by]
        assert "y" in answer[split_by]
        assert len(answer[split_by]["x"]) == len(answer[split_by]["y"])


def test_get_svl_data_histogram(test_conn):
    """ Tests that the get_svl_data function returns the correct data for
        histogram plots.
    """
    svl_plot = {
        "type": "histogram",
        "data": "bigfoot",
        "field": "temperature_mid",
        "bins": 25
    }

    answer = get_svl_data(svl_plot, test_conn)
    assert "x" in answer


def test_get_svl_data_pie(test_conn):
    """ Tests that the get_svl_data function returns the correct data for pie
        plots.
    """
    svl_plot = {
        "type": "pie",
        "data": "bigfoot",
        "field": "classification"
    }

    answer = get_svl_data(svl_plot, test_conn)
    assert "labels" in answer
    assert "values" in answer
    assert len(answer["labels"]) == len(answer["values"])
