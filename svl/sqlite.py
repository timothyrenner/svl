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
    "SECOND": "STRFTIME('%Y-%m-%DT%H:%M:%S', {})"
}


def _csv_to_sqlite_pandas(svl_datasets):
    """ Loads SVL datasets from CSV to SQLite using pandas.

        Parameters
        -----------
        svl_datasets : dict
            The SVL dataset definitions.

        Returns
        -------
        sqlite3.Connection
            The connection to the in-memory SQLite database.
    """
    conn = sqlite3.connect(":memory:")
    for table_name, csv_filename in svl_datasets.items():
        pd.read_csv(csv_filename).to_sql(table_name, conn, index=False)
    return conn


def _get_field(svl_axis):
    if "transform" in svl_axis:
        return svl_axis["transform"]
    elif "field" in svl_axis:
        return svl_axis["field"]
    else:
        return "*"


def csv_to_sqlite(svl_datasets):
    """ Loads SVL datasets from CSV to SQLite.

        Uses pandas if available.

        Parameters
        ----------
        svl_datasets : dict
            The SVL dataset definitions.

        Returns
        -------
        sqlite3.Connection
            The connection to the in-memory SQLite database.
    """
    if PANDAS:
        return _csv_to_sqlite_pandas(svl_datasets)
    else:
        raise NotImplementedError("Haven't implement non-pandas csv->sqlite.")


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
    query = "SELECT {} AS x FROM {}".format(
        _get_field(svl_plot["axis"]),
        svl_plot["data"]
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
        _get_field(svl_plot["axis"]),
        svl_plot["data"]
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
    # Step 1: Process the selects.

    select_fields = []

    for axis in ["x", "y", "split_by"]:

        # Skip if the axis isn't in the plot.
        if axis not in svl_plot:
            continue

        field = _get_field(svl_plot[axis])

        if "temporal" in svl_plot[axis]:
            select_fields.append("{} AS {}".format(
                TEMPORAL_CONVERTERS[svl_plot[axis]["temporal"]].format(field),
                axis
            ))
        elif "agg" in svl_plot[axis]:
            # NOTE: Split by axis will not take aggregations.
            select_fields.append("{}({}) AS {}".format(
                svl_plot[axis]["agg"],
                field,
                axis
            ))
        else:
            select_fields.append("{} AS {}".format(field, axis))

    # Step 2: Process the aggregations.
    group_fields = []

    group_axis = None

    if "agg" in svl_plot["x"]:
        group_axis = "y"
    elif "agg" in svl_plot["y"]:
        group_axis = "x"

    if group_axis and ("temporal" in svl_plot[group_axis]):
        # The temporal transformation needs to be applied again in the
        # GROUP BY clause if it's in the main SELECT.
        group_fields.append(
            TEMPORAL_CONVERTERS[svl_plot[group_axis]["temporal"]].format(
                _get_field(svl_plot[group_axis])
            )
        )
    elif group_axis:
        group_fields.append(_get_field(svl_plot[group_axis]))

    # Only add the split by to the group by if there's already a group axis.
    if group_axis and ("split_by" in svl_plot):
        group_fields.append(svl_plot["split_by"]["field"])

    # Step 3: Build the query.
    query = "SELECT {} FROM {}".format(
        ", ".join(select_fields),
        svl_plot["data"]
    )

    if "filter" in svl_plot:
        query = "{} WHERE {}".format(query, svl_plot["filter"])

    if group_axis:
        query = "{} GROUP BY {}".format(
            query,
            ", ".join(group_fields)
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

    # Step 3: Convert the resulting list of sqlite rows into SVL data
    # structures.
    # NOTE: For now this structure corresponds directly to plotly's
    # traces, but since it's internal we can change it to something more
    # general later.
    # TODO: There's probably a nice way to abstract the extraction to remove
    # the branching logic.
    if svl_plot["type"] in {"line", "scatter", "bar"}:
        if "split_by" not in data_list[0].keys():
            svl_data = {"x": [], "y": []}
            for row in data_list:
                svl_data["x"].append(row["x"])
                svl_data["y"].append(row["y"])
        else:
            svl_data = {}
            for row in data_list:
                if row["split_by"] not in svl_data:
                    svl_data[row["split_by"]] = {"x": [], "y": []}
                svl_data[row["split_by"]]["x"].append(row["x"])
                svl_data[row["split_by"]]["y"].append(row["y"])
    elif svl_plot["type"] == "histogram":
        # Just one dimension for histograms.
        svl_data = {"x": []}
        for row in data_list:
            svl_data["x"].append(row["x"])
    elif svl_plot["type"] == "pie":
        svl_data = {
            "labels": [],
            "values": []
        }
        for row in data_list:
            svl_data["labels"].append(row["label"])
            svl_data["values"].append(row["value"])
    return svl_data
