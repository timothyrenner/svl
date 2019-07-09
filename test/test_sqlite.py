import pytest
import os
import pandas as pd
import sqlite3

from pandas.testing import assert_frame_equal

from svl.data_sources.sqlite import (
    _csv_to_sqlite_pandas,
    _parquet_to_sqlite_pandas,
    _get_field,
    file_to_sqlite,
    sqlite_table,
    create_datasets,
    svl_to_sql_xy,
    svl_to_sql_hist,
    svl_to_sql_pie,
    get_svl_data,
)


@pytest.fixture()
def test_csv_file():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_csv_file = os.path.join(
        current_dir, "test_datasets", "bigfoot_sightings.csv"
    )
    return test_csv_file


@pytest.fixture()
def test_parquet_file():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_parquet_file = os.path.join(
        current_dir, "test_datasets", "bigfoot_sightings.parquet"
    )
    return test_parquet_file


@pytest.fixture()
def test_conn(test_csv_file):
    # Obviously don't need the whole plot just the bit about the file.
    test_svl_datasets = {
        "bigfoot": {"file": test_csv_file},
        "recent_bigfoot": {
            "sql": "SELECT * FROM bigfoot WHERE date >= '2008-01-01'"
        },
    }

    conn = create_datasets(test_svl_datasets)
    yield conn
    conn.close()


def test_csv_to_sqlite_pandas(test_csv_file):
    """ Tests that the _csv_to_sqlite_pandas function loads the database with
        the correct values.
    """
    csv_filename = test_csv_file
    table_name = "bigfoot"
    conn = sqlite3.connect(":memory:")

    truth = pd.read_csv(test_csv_file)
    _csv_to_sqlite_pandas(csv_filename, table_name, conn)
    answer = pd.read_sql_query("SELECT * FROM bigfoot", conn)

    assert_frame_equal(truth, answer)


def test_parquet_to_sqlite_pandas(test_parquet_file):
    """ Tests that the _parquet_to_sqlite_pandas function loads the database
        with the correct values.
    """
    parquet_filename = test_parquet_file
    table_name = "bigfoot"
    conn = sqlite3.connect(":memory:")

    truth = pd.read_parquet(test_parquet_file)
    _parquet_to_sqlite_pandas(parquet_filename, table_name, conn)
    answer = pd.read_sql_query("SELECT * FROM bigfoot", conn)

    assert_frame_equal(truth, answer)


def test_get_field_transform():
    """ Tests that the _get_field function returns the correct value for an
        axis with a transform.
    """
    svl_axis = {"transform": "temperature_mid + 1"}

    truth = "temperature_mid + 1"

    answer = _get_field(svl_axis)

    assert truth == answer


def test_get_field_field():
    """ Tests that the _get_field function returns the correct value for an
        axis with a field.
    """
    svl_axis = {"field": "temperature_mid"}

    truth = "temperature_mid"

    answer = _get_field(svl_axis)

    assert truth == answer


def test_get_field_none():
    """ Tests that the _get_field function returns the correct value for an
        axis without a field or transform.
    """
    svl_axis = {"agg": "COUNT"}

    truth = "*"

    answer = _get_field(svl_axis)

    assert truth == answer


def test_get_field_temporal():
    """ Tests that the _get_field function returns the correct value for an
        axis with a temporal modifier.
    """
    svl_axis = {"field": "date", "temporal": "YEAR"}
    truth = "STRFTIME('%Y', date)"
    answer = _get_field(svl_axis)

    assert truth == answer


def test_file_to_sqlite_csv(test_csv_file):
    """ Tests that the file_to_sqlite function loads the database with the
        correct values when the file is a CSV file.
    """
    csv_filename = test_csv_file
    table_name = "bigfoot"
    conn = sqlite3.connect(":memory:")

    truth = pd.read_csv(test_csv_file)
    file_to_sqlite(csv_filename, table_name, conn)
    answer = pd.read_sql_query("SELECT * FROM bigfoot", conn)

    assert_frame_equal(truth, answer)


def test_file_to_sqlite_parquet(test_parquet_file):
    """ Tests that the file_to_sqlite function loads the database with the
        correct values when the file is a parquet file.
    """
    parquet_filename = test_parquet_file
    table_name = "bigfoot"
    conn = sqlite3.connect(":memory:")

    truth = pd.read_parquet(test_parquet_file)
    file_to_sqlite(parquet_filename, table_name, conn)
    answer = pd.read_sql_query("SELECT * FROM bigfoot", conn)

    assert_frame_equal(truth, answer)


def test_sqlite_table(test_csv_file):
    """ Tests that the sqlite_table function executes correctly.
    """
    conn = sqlite3.connect(":memory:")
    _csv_to_sqlite_pandas(test_csv_file, "bigfoot", conn)
    sqlite_table(
        "SELECT * FROM bigfoot WHERE date >= '2008-01-01'",
        "recent_bigfoot",
        conn,
    )

    truth = (
        pd.read_sql("SELECT * FROM bigfoot", conn)
        .query("date >= '2008-01-01'")
        .reset_index(drop=True)
    )
    answer = pd.read_sql("SELECT * FROM recent_bigfoot", conn)

    assert_frame_equal(truth, answer)


def test_create_datasets(test_csv_file):
    """ Tests that the create_datasets function returns the correct value.
    """
    svl_datasets = {
        "bigfoot": {"file": test_csv_file},
        "recent_bigfoot": {
            "sql": "SELECT * FROM bigfoot WHERE date >= '2008-01-01'"
        },
    }

    conn = create_datasets(svl_datasets)

    # Assert that the bigfoot dataset is correct.
    truth_bigfoot = pd.read_csv(test_csv_file)
    answer_bigfoot = pd.read_sql("SELECT * FROM bigfoot", conn)

    assert_frame_equal(truth_bigfoot, answer_bigfoot)

    # Assert that the recent_bigfoot dataset is correct.
    truth_recent_bigfoot = truth_bigfoot.query(
        "date >= '2008-01-01'"
    ).reset_index(drop=True)
    answer_recent_bigfoot = pd.read_sql("SELECT * FROM recent_bigfoot", conn)

    assert_frame_equal(truth_recent_bigfoot, answer_recent_bigfoot)


def test_svl_to_sql_hist():
    """ Tests that the svl_to_sql_hist function returns the correct value.
    """
    svl_plot = {
        "data": "bigfoot",
        "type": "histogram",
        "x": {"field": "temperature_mid"},
        "bins": 25,
    }

    truth_query = "SELECT temperature_mid AS x FROM bigfoot"

    answer_query = svl_to_sql_hist(svl_plot)

    assert truth_query == answer_query


def test_svl_to_sql_hist_filter():
    """ Tests that the svl_to_sql_hist function returns the correct value when
        there's a filter.
    """
    svl_plot = {
        "data": "bigfoot",
        "type": "histogram",
        "y": {"field": "temperature_mid"},
        "bins": 25,
        "filter": "temperature_mid <= 100",
    }

    truth_query = (
        "SELECT temperature_mid AS y FROM bigfoot "
        "WHERE temperature_mid <= 100"
    )

    answer_query = svl_to_sql_hist(svl_plot)

    assert truth_query == answer_query


def test_svl_to_sql_hist_split_by():
    """ Tests that the svl_to_sql_hist function returns the correct value when
        there's a split-by axis.
    """
    svl_plot = {
        "data": "bigfoot",
        "type": "histogram",
        "x": {"field": "temperature_mid"},
        "split_by": {"field": "classification"},
        "bins": 5,
    }

    truth_query = (
        "SELECT temperature_mid AS x, classification AS split_by "
        "FROM bigfoot"
    )

    answer_query = svl_to_sql_hist(svl_plot)

    assert truth_query == answer_query


def test_svl_to_sql_hist_split_by_temporal():
    """ Tests that the svl_to_sql_hist function returns the correct value when
        there's a split-by axis with a temporal modifier.
    """
    svl_plot = {
        "data": "bigfoot",
        "type": "histogram",
        "x": {"field": "temperature_mid"},
        "split_by": {"field": "date", "temporal": "YEAR"},
        "bins": 5,
    }

    truth_query = (
        "SELECT temperature_mid AS x, STRFTIME('%Y', date) AS split_by "
        "FROM bigfoot"
    )

    answer_query = svl_to_sql_hist(svl_plot)

    assert truth_query == answer_query


def test_svl_to_sql_hist_split_by_transform():
    """ Tests that the svl_to_sql_hist function returns the correct value when
        there's a split-by axis with a transform modifier.
    """
    svl_plot = {
        "data": "bigfoot",
        "type": "histogram",
        "x": {"field": "wind_speed"},
        "split_by": {
            "transform": "CASE WHEN 'temperature' > 90 THEN 'hot' ELSE "
            "'not_hot' END"
        },
    }
    truth_query = (
        "SELECT wind_speed AS x, "
        "CASE WHEN 'temperature' > 90 THEN 'hot' ELSE 'not_hot' END "
        "AS split_by FROM bigfoot"
    )
    answer_query = svl_to_sql_hist(svl_plot)
    assert truth_query == answer_query


def test_svl_to_sql_pie():
    """ Tests that the svl_to_sql_pie function returns the correct value.
    """
    svl_plot = {"data": "bigfoot", "axis": {"field": "classification"}}

    truth_query = (
        "SELECT classification AS label, COUNT(*) AS value FROM bigfoot "
        "GROUP BY classification"
    )

    answer_query = svl_to_sql_pie(svl_plot)

    assert truth_query == answer_query


def test_svl_to_sql_pie_filter():
    """ Tests that the svl_to_sql_pie function returns the correct value when
        a filter has been applied.
    """
    svl_plot = {
        "data": "bigfoot",
        "axis": {"field": "classification"},
        "filter": "date >= '1960-01-01'",
    }

    truth_query = (
        "SELECT classification AS label, COUNT(*) AS value FROM bigfoot "
        "WHERE date >= '1960-01-01' GROUP BY classification"
    )

    answer_query = svl_to_sql_pie(svl_plot)

    assert truth_query == answer_query


def test_svl_to_sql_xy():
    """ Tests that the svl_to_sql_xy function returns the correct value when
        there are no aggregations or split_bys.
    """
    svl_plot = {
        "data": "bigfoot",
        "x": {"field": "latitude"},
        "y": {"field": "temperature_mid"},
    }

    truth_query = "SELECT latitude AS x, temperature_mid AS y FROM bigfoot"

    answer_query = svl_to_sql_xy(svl_plot)

    assert truth_query == answer_query


def test_svl_to_sql_xy_filter():
    """ Tests that the svl_to_sql_xy function returns the correct value when
        there's a filter.
    """
    svl_plot = {
        "data": "bigfoot",
        "x": {"field": "latitude"},
        "y": {"field": "temperature_mid"},
        "filter": "latitude < 84",
    }

    truth_query = (
        "SELECT latitude AS x, temperature_mid AS y FROM bigfoot "
        "WHERE latitude < 84"
    )
    answer_query = svl_to_sql_xy(svl_plot)

    assert truth_query == answer_query


def test_svl_to_sql_xy_agg_x():
    """ Tests that the svl_to_sql_xy function returns the correct value when x is
        aggregated.
    """
    svl_plot = {
        "data": "bigfoot",
        "x": {"field": "classification"},
        "y": {"agg": "MAX", "field": "temperature"},
    }

    truth_query = (
        "SELECT classification AS x, MAX(temperature) AS y "
        "FROM bigfoot GROUP BY classification"
    )

    answer_query = svl_to_sql_xy(svl_plot)

    assert truth_query == answer_query


def test_svl_to_sql_xy_agg_y():
    """ Tests that the svl_to_sql_xy function returns the correct value when
        there's an aggregation on y and no aggregation on colors.
    """
    svl_plot = {
        "data": "bigfoot",
        "x": {"agg": "AVG", "field": "temperature"},
        "y": {"field": "classification"},
    }

    truth_query = (
        "SELECT AVG(temperature) AS x, classification AS y "
        "FROM bigfoot GROUP BY classification"
    )

    answer_query = svl_to_sql_xy(svl_plot)

    assert truth_query == answer_query


def test_svl_to_sql_xy_count():
    """ Tests that the svl_to_sql_xy function returns the correct value when
        one of the aggregations is a count.
    """
    svl_plot = {
        "data": "bigfoot",
        "x": {"field": "classification"},
        "y": {"agg": "COUNT"},
    }

    truth_query = (
        "SELECT classification AS x, COUNT(*) AS y "
        "FROM bigfoot GROUP BY classification"
    )

    answer_query = svl_to_sql_xy(svl_plot)

    assert truth_query == answer_query


def test_svl_to_sql_xy_temporal():
    """ Tests that the svl_to_sql_xy function returns the correct value when one
        of the fields has a temporal transformation.
    """
    svl_plot = {
        "data": "bigfoot",
        "x": {"field": "date", "temporal": "YEAR"},
        "y": {"field": "temperature"},
    }

    truth_query = (
        "SELECT STRFTIME('%Y', date) AS x, temperature AS y " "FROM bigfoot"
    )

    answer_query = svl_to_sql_xy(svl_plot)

    assert truth_query == answer_query


def test_svl_to_sql_xy_temporal_agg():
    """ Tests that the svl_to_sql_xy function returns the correct value when one
        field is a temporal transformation and the other is an aggregation.
    """
    svl_plot = {
        "data": "bigfoot",
        "x": {"field": "date", "temporal": "YEAR"},
        "y": {"agg": "COUNT"},
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
        "x": {"field": "date"},
        "y": {"field": "temperature"},
        "split_by": {"field": "classification"},
    }

    truth_query = (
        "SELECT date AS x, temperature AS y, "
        "classification AS split_by FROM bigfoot"
    )

    answer_query = svl_to_sql_xy(svl_plot)

    assert truth_query == answer_query


def test_svl_to_sql_xy_split_by_agg():
    """ Tests that the svl_to_sql_xy function returns the correct value when
        there's a split by field and an aggregation.
    """
    svl_plot = {
        "data": "bigfoot",
        "x": {"field": "date", "temporal": "YEAR"},
        "y": {"field": "temperature", "agg": "MAX"},
        "split_by": {"field": "classification"},
    }

    truth_query = (
        "SELECT STRFTIME('%Y', date) AS x, MAX(temperature) AS y, "
        "classification AS split_by FROM bigfoot "
        "GROUP BY STRFTIME('%Y', date), classification"
    )

    answer_query = svl_to_sql_xy(svl_plot)

    assert truth_query == answer_query


def test_svl_to_sql_xy_split_by_temporal():
    """ Tests that the svl_to_sql_xy function returns the correct value when
        there's a split by field with a temporal modifier.
    """
    svl_plot = {
        "data": "bigfoot",
        "x": {"field": "latitude"},
        "y": {"field": "temperature", "agg": "MAX"},
        "split_by": {"field": "date", "temporal": "YEAR"},
    }
    truth_query = (
        "SELECT latitude AS x, MAX(temperature) AS y, "
        "STRFTIME('%Y', date) AS split_by FROM bigfoot "
        "GROUP BY latitude, STRFTIME('%Y', date)"
    )
    answer_query = svl_to_sql_xy(svl_plot)

    assert truth_query == answer_query


def test_svl_to_sql_xy_split_by_transform():
    """ Tests that the svl_to_sql_xy function returns the correct value when
        there's a split by field with a transform modifier.
    """
    svl_plot = {
        "data": "bigfoot",
        "x": {"field": "date", "temporal": "YEAR"},
        "y": {"field": "latitude", "agg": "MAX"},
        "split_by": {
            "transform": "CASE WHEN temperature > 90 THEN 'hot' "
            "ELSE 'not_hot' END"
        },
    }
    truth_query = (
        "SELECT STRFTIME('%Y', date) AS x, MAX(latitude) AS y, "
        "CASE WHEN temperature > 90 THEN 'hot' ELSE 'not_hot' END AS split_by "
        "FROM bigfoot GROUP BY STRFTIME('%Y', date), "
        "CASE WHEN temperature > 90 THEN 'hot' ELSE 'not_hot' END"
    )
    answer_query = svl_to_sql_xy(svl_plot)

    assert truth_query == answer_query


def test_svl_to_sql_xy_sort_x():
    """ Tests that the svl_to_sql_xy function returns the correct value when
        there's a sort clause on x.
    """
    svl_plot = {
        "data": "bigfoot",
        "type": "line",
        "x": {"field": "latitude", "sort": "ASC"},
        "y": {"field": "temperature_mid", "agg": "AVG"},
    }

    truth_query = (
        "SELECT latitude AS x, AVG(temperature_mid) AS y "
        "FROM bigfoot "
        "GROUP BY latitude "
        "ORDER BY x ASC"
    )

    answer_query = svl_to_sql_xy(svl_plot)

    assert truth_query == answer_query


def test_svl_to_sql_xy_sort_y():
    """ Tests that the svl_to_sql_xy function returns the correct value when
        there's a sort clause on y.
    """
    svl_plot = {
        "data": "bigfoot",
        "type": "bar",
        "x": {"field": "classification"},
        "y": {"agg": "COUNT", "sort": "DESC", "field": "classification"},
    }

    truth_query = (
        "SELECT classification AS x, COUNT(classification) AS y "
        "FROM bigfoot "
        "GROUP BY classification "
        "ORDER BY y DESC"
    )

    answer_query = svl_to_sql_xy(svl_plot)

    assert truth_query == answer_query


def test_svl_to_sql_xy_sort_split_by():
    """ Tests that the svl_to_sql_xy function returns the correct value when
        there's a SORT and a SPLIT BY.
    """
    svl_plot = {
        "data": "bigfoot",
        "type": "line",
        "x": {"field": "latitude", "sort": "ASC"},
        "y": {"field": "temperature_mid", "agg": "AVG"},
        "split_by": {"field": "classification"},
    }

    truth_query = (
        "SELECT latitude AS x, AVG(temperature_mid) AS y, "
        "classification AS split_by "
        "FROM bigfoot "
        "GROUP BY latitude, classification "
        "ORDER BY split_by, x ASC"
    )

    answer_query = svl_to_sql_xy(svl_plot)

    assert truth_query == answer_query


def test_svl_to_sql_xy_color_by():
    """ Tests that the svl_to_sql_xy function returns the correct value when
        there's a COLOR BY.
    """
    svl_plot = {
        "data": "bigfoot",
        "type": "scatter",
        "x": {"field": "latitude"},
        "y": {"field": "temperature_mid"},
        "color_by": {"field": "humidity"},
    }

    truth_query = (
        "SELECT latitude AS x, temperature_mid AS y, humidity AS color_by "
        "FROM bigfoot"
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
        "x": {"field": "date", "temporal": "YEAR"},
        "y": {"agg": "COUNT"},
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
        "x": {"field": "date", "temporal": "YEAR"},
        "y": {"agg": "COUNT"},
        "split_by": {"field": "classification"},
    }

    answer = get_svl_data(svl_plot, test_conn)
    for split_by in ["Class A", "Class B"]:
        assert split_by in answer
        assert "x" in answer[split_by]
        assert "y" in answer[split_by]
        assert len(answer[split_by]["x"]) == len(answer[split_by]["y"])


def test_get_svl_data_xy_color_by(test_conn):
    """ Tests that the get_svl_data function returns the correct data for xy
        plots that have a color_by axis.
    """
    svl_plot = {
        "data": "bigfoot",
        "type": "bar",
        "x": {"field": "date", "temporal": "YEAR"},
        "y": {"agg": "COUNT"},
        "color_by": {"field": "temperature_mid", "agg": "AVG"},
    }
    answer = get_svl_data(svl_plot, test_conn)

    assert "x" in answer
    assert "y" in answer
    assert "color_by" in answer
    assert len(answer["x"]) == len(answer["y"])
    assert len(answer["x"]) == len(answer["color_by"])


def test_get_svl_data_histogram(test_conn):
    """ Tests that the get_svl_data function returns the correct data for
        histogram plots.
    """
    svl_plot = {
        "type": "histogram",
        "data": "bigfoot",
        "x": {"field": "temperature_mid"},
        "bins": 25,
    }

    answer = get_svl_data(svl_plot, test_conn)
    assert "x" in answer


def test_get_svl_data_histogram_split_by(test_conn):
    """ Tests that the get_svl_data function returns the correct data for
        histogram plots with a split-by axis.
    """
    svl_plot = {
        "type": "histogram",
        "data": "bigfoot",
        "y": {"field": "temperature_mid"},
        "split_by": {"field": "classification"},
    }

    answer = get_svl_data(svl_plot, test_conn)
    for split_by in ["Class A", "Class B"]:
        assert split_by in answer
        assert "y" in answer[split_by]


def test_get_svl_data_pie(test_conn):
    """ Tests that the get_svl_data function returns the correct data for pie
        plots.
    """
    svl_plot = {
        "type": "pie",
        "data": "bigfoot",
        "axis": {"field": "classification"},
    }

    answer = get_svl_data(svl_plot, test_conn)
    assert "labels" in answer
    assert "values" in answer
    assert len(answer["labels"]) == len(answer["values"])


def test_get_svl_data_empty_result_set(test_conn):
    """ Tests that the get_svl_data function raises a sqlite3.DatabaseError
        when there's an empty result set returned.
    """
    svl_plot = {
        "type": "pie",
        "data": "bigfoot",
        "axis": {"field": "classification"},
        "filter": "classification = 'D'",
    }

    with pytest.raises(sqlite3.DatabaseError):
        get_svl_data(svl_plot, test_conn)
