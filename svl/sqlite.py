try:
    import pandas as pd
    PANDAS = True
except ImportError:
    PANDAS = False

import sqlite3

from toolz import get

TEMPORAL_CONVERTERS = {
    "YEAR": "STRFTIME('%Y', {})",
    "MONTH": "STRFTIME('%Y-%m', {})",
    "DAY": "STRFTIME('%Y-%m-%D', {})",
    "HOUR": "STRFTIME('%Y-%m-%DT%H', {})",
    "MINUTE": "STRFTIME('%Y-%m-%DT%H:%M', {})",
    "SECOND": "STRFTIME('%Y-%m-%DT%H:%M:%S', {})"
}


def _csv_to_sqlite_pandas(svl_datasets):
    conn = sqlite3.connect(":memory:")
    for table_name, csv_filename in svl_datasets.items():
        pd.read_csv(csv_filename).to_sql(table_name, conn, index=False)
    return conn


def csv_to_sqlite(svl_datasets):
    if PANDAS:
        return _csv_to_sqlite_pandas(svl_datasets)
    else:
        raise NotImplementedError("Haven't implement non-pandas csv->sqlite.")


def svl_to_sql(svl_plot):
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

    for axis in ["x", "y", "color"]:

        # Skip if the axis isn't in the plot.
        if axis not in svl_plot:
            continue

        field = get("field", svl_plot[axis], "*")

        if "temporal" in svl_plot[axis]:
            select_fields.append("{} AS {}".format(
                TEMPORAL_CONVERTERS[svl_plot[axis]["temporal"]].format(field),
                axis
            ))
        elif "agg" in svl_plot[axis]:
            # NOTE: Color axis will not take aggregations. This needs to be
            # implemented though.
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
                svl_plot[group_axis]["field"]
            )
        )
    elif group_axis:
        group_fields.append(svl_plot[group_axis]["field"])

    # Only add the color to the group by if there's already a group axis.
    if group_axis and ("color" in svl_plot):
        group_fields.append(svl_plot["color"]["field"])

    # Step 3: Build the query.
    query = "SELECT {} FROM {}".format(
        ", ".join(select_fields),
        svl_plot["data"]
    )

    if group_axis:
        query = "{} GROUP BY {}".format(
            query,
            ", ".join(group_fields)
        )

    return query


def get_svl_data(svl_plot, conn):
    # Step 1: Create the query.
    query = svl_to_sql(svl_plot)

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
    if "color" not in data_list[0].keys():
        svl_data = {"x": [], "y": []}
        for row in data_list:
            svl_data["x"].append(row["x"])
            svl_data["y"].append(row["y"])
    else:
        svl_data = {}
        for row in data_list:
            if row["color"] not in svl_data:
                svl_data[row["color"]] = {"x": [], "y": []}
            svl_data[row["color"]]["x"].append(row["x"])
            svl_data[row["color"]]["y"].append(row["y"])
    return svl_data