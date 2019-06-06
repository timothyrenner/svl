try:
    import pandas as pd

    PANDAS = True
except ImportError:
    PANDAS = False

import sqlite3

TEMPORAL_CONVERTERS = {
    "YEAR": "STRFTIME('%Y', {})",
    "MONTH": "STRFTIME('%Y-%m', {})",
    "DAY": "STRFTIME('%Y-%m-%D', {})",
    "HOUR": "STRFTIME('%Y-%m-%DT%H', {})",
    "MINUTE": "STRFTIME('%Y-%m-%DT%H:%M', {})",
    "SECOND": "STRFTIME('%Y-%m-%DT%H:%M:%S', {})",
}


def _csv_to_sqlite_pandas(csv_filename, table_name, conn):
    """ Loads an SVL dataset from CSV to SQLite using pandas.

        Parameters
        -----------
        csv_filename : str
            The name of the CSV file with the data.
        table_name : str
            The name of the table to output.
    """
    pd.read_csv(csv_filename).to_sql(table_name, conn, index=False)


def _parquet_to_sqlite_pandas(parquet_filename, table_name, conn):
    """ Loads an SVL dataset from parquet to SQLite using pandas.

        Parameters
        ----------
        parquet_filename : str
            The name of the parquet file with the data.
        table_name : str
            The name of the table to output.
    """
    pd.read_parquet(parquet_filename).to_sql(table_name, conn, index=False)


def _get_field(svl_axis):
    if "transform" in svl_axis:
        return svl_axis["transform"]
    elif "temporal" in svl_axis:
        return TEMPORAL_CONVERTERS[svl_axis["temporal"]].format(
            svl_axis["field"]
        )
    elif "field" in svl_axis:
        return svl_axis["field"]
    else:
        return "*"


def file_to_sqlite(filename, table_name, conn):
    """ Loads SVL dataset from a file to SQLite.

        Uses pandas if available.

        Parameters
        ----------
        filename : str
            The file with the data.

        table_name : str
            The name of the destination table.

        conn : sqlite3.Connection
            The connection to the sqlite database.

    """
    if PANDAS:
        if filename.endswith("parquet"):
            return _parquet_to_sqlite_pandas(filename, table_name, conn)
        else:
            return _csv_to_sqlite_pandas(filename, table_name, conn)
    else:
        raise NotImplementedError("Haven't implement non-pandas csv->sqlite.")


def sqlite_table(sql_statement, table_name, conn):
    """ Creates an SVL dataset from a SQL query.

        Parameters
        ----------
        sql_statement : str
            The SQL query defining the table.

        table_name : str
            The name of the destination table.

        conn : sqlite3.Connection
            The connection to the sqlite database.
    """
    conn.execute("CREATE TABLE {} AS {};".format(table_name, sql_statement))


def create_datasets(svl_datasets):
    """ Creates the SVL datasets.

        Parameters
        ----------
        svl_datasets : dict
            The SVL dataset specifier.

        Returns
        -------
        conn : sqlite3.Connection
            The connection to the sqlite3 database.
    """
    conn = sqlite3.connect(":memory:")
    files = list(
        filter(lambda items: "file" in items[1], svl_datasets.items())
    )
    queries = list(
        filter(lambda items: "sql" in items[1], svl_datasets.items())
    )

    # Do the files first.
    for table_name, table_spec in files:
        file_to_sqlite(table_spec["file"], table_name, conn)

    # Now do the queries.
    for table_name, table_spec in queries:
        sqlite_table(table_spec["sql"], table_name, conn)

    return conn


def svl_to_sql_hist(svl_plot):
    """ Constructs a SQL query for histogram plots.

        Parameters
        -----------
        svl_plot : dict
            The SVL plot definition.

        Returns
        -------
        str
            The SQL query for the dataset required for the plot.
    """
    select_fields = []

    for axis in ["x", "y", "split_by"]:
        # Skip if the axis isn't in the plot.
        if axis not in svl_plot:
            continue

        field = _get_field(svl_plot[axis])
        select_fields.append("{} AS {}".format(field, axis))

    query = "SELECT {} FROM {}".format(
        ", ".join(select_fields), svl_plot["data"]
    )

    if "filter" in svl_plot:
        query = "{} WHERE {}".format(query, svl_plot["filter"])

    return query


def svl_to_sql_pie(svl_plot):
    """ Constructs a SQL query for pie charts.

        Parameters
        ----------
        svl_plot : dict
            The SVL plot definition.

        Returns
        -------
        str
            The SQL query for the dataset required for the plot.
    """
    query = "SELECT {} AS label, COUNT(*) AS value FROM {}".format(
        _get_field(svl_plot["axis"]), svl_plot["data"]
    )

    if "filter" in svl_plot:
        query = "{} WHERE {}".format(query, svl_plot["filter"])

    query = "{} GROUP BY {}".format(query, _get_field(svl_plot["axis"]))

    return query


def svl_to_sql_xy(svl_plot):
    """ Takes an SVL plot specification and produces a SQL query to retrieve
        the data.

        Parameters
        ----------
        svl_plot : dict
            The SVL plot specifier.

        Returns
        -------
        str
            The query to execute.
    """
    # TODO this is a very big function with a lot of redundant conditionals
    # Step 1: Process the selects.

    select_fields = []

    for axis in ["x", "y", "split_by", "color_by"]:

        # Skip if the axis isn't in the plot.
        if axis not in svl_plot:
            continue

        field = _get_field(svl_plot[axis])

        if "agg" in svl_plot[axis]:
            # NOTE: Split by axis will not take aggregations.
            select_fields.append(
                "{}({}) AS {}".format(svl_plot[axis]["agg"], field, axis)
            )
        else:
            select_fields.append("{} AS {}".format(field, axis))

    # Step 2: Process the aggregations.
    group_fields = []

    group_axis = None

    if "agg" in svl_plot["x"]:
        group_axis = "y"
    elif "agg" in svl_plot["y"]:
        group_axis = "x"

    if group_axis:
        group_fields.append(_get_field(svl_plot[group_axis]))

    split_by_field = "" if "split_by" not in svl_plot else "split_by"
    # Only add the split by to the group by if there's already a group axis.
    # Empty strings are falsey ... I mean Falsey.
    if group_axis and split_by_field:
        group_fields.append(_get_field(svl_plot["split_by"]))

    # NOTE: the color_by field cannot appear in a GROUP BY. If there's an
    # aggregation on x or y, then there must be an aggregation on color_by.

    # Step 3: Build the query.
    query = "SELECT {} FROM {}".format(
        ", ".join(select_fields), svl_plot["data"]
    )

    if "filter" in svl_plot:
        query = "{} WHERE {}".format(query, svl_plot["filter"])

    if group_axis:
        query = "{} GROUP BY {}".format(query, ", ".join(group_fields))

    # If there's a SPLIT BY and a sort, make sure to sort by the split by
    # field first, since each SPLIT BY value becomes it's own trace.
    sort_fields = []
    if split_by_field:
        sort_fields.append(split_by_field)

    if "sort" in svl_plot["x"]:
        query = "{} ORDER BY {} {}".format(
            query, ", ".join(sort_fields + ["x"]), svl_plot["x"]["sort"]
        )
    elif "sort" in svl_plot["y"]:
        query = "{} ORDER BY {} {}".format(
            query, ", ".join(sort_fields + ["y"]), svl_plot["y"]["sort"]
        )

    return query


def get_svl_data(svl_plot, conn):
    """ Obtains the data for the provided SVL plot from the SQLite database.

        Parameters
        ----------
        svl_plot : dict
            The SVL plot definition.

        conn : sqlite3.Connection
            The SQLite database connection. Must point to the database loaded
            with the SVL datasets.

        Returns
        -------
        dict
            The dataset required for the plot.
    """
    # Step 1: Create the query.
    # NOTE: Kind of annoying to touch this so many times - might be worth
    # refactoring a little bit so everything's in _one_ if statement.
    if svl_plot["type"] in {"line", "scatter", "bar"}:
        query = svl_to_sql_xy(svl_plot)
    elif svl_plot["type"] == "histogram":
        query = svl_to_sql_hist(svl_plot)
    elif svl_plot["type"] == "pie":
        query = svl_to_sql_pie(svl_plot)

    # Step 2: Execute the query and retrieve the results.
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute(query)
    # If this doesn't fit into memory we're hosed downstream anyway, so assume
    # it does :).
    data_list = cursor.fetchall()

    if len(data_list) == 0:
        # TODO Make this a different error? Might not matter.
        raise sqlite3.DatabaseError(
            "Encountered empty result set. Check filters or source data."
        )

    # Step 3: Convert the resulting list of sqlite rows into SVL data
    # structures.
    # NOTE: For now this structure corresponds _mostly_ to plotly's
    # traces, but since it's internal we can change it to something more
    # general later.
    # TODO There's probably a nice way to abstract the extraction to remove
    # TODO the branching logic.
    if svl_plot["type"] in {"line", "scatter", "bar"}:
        if "split_by" not in data_list[0].keys():
            svl_data = {k: [] for k in data_list[0].keys()}
            for row in data_list:
                # ! Yikes - four levels of nesting.
                for axis in row.keys():
                    svl_data[axis].append(row[axis])
        else:
            svl_data = {}
            for row in data_list:
                if row["split_by"] not in svl_data:
                    svl_data[row["split_by"]] = {"x": [], "y": []}
                svl_data[row["split_by"]]["x"].append(row["x"])
                svl_data[row["split_by"]]["y"].append(row["y"])
    elif svl_plot["type"] == "histogram":
        # Just one dimension for histograms.
        # Determine which axis it is.
        axis = "x" if "x" in svl_plot else "y"
        if "split_by" not in svl_plot:
            svl_data = {axis: []}
            for row in data_list:
                svl_data[axis].append(row[axis])
        else:
            svl_data = {}
            for row in data_list:
                if row["split_by"] not in svl_data:
                    svl_data[row["split_by"]] = {axis: []}
                svl_data[row["split_by"]][axis].append(row[axis])
    elif svl_plot["type"] == "pie":
        svl_data = {"labels": [], "values": []}
        for row in data_list:
            svl_data["labels"].append(row["label"])
            svl_data["values"].append(row["value"])
    return svl_data
