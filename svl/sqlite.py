from toolz import get_in

TEMPORAL_CONVERTERS = {
    "YEAR": "STRFTIME('%Y', ?)",
    "MONTH": "STRFTIME('%Y-%m', ?)",
    "DAY": "STRFTIME('%Y-%m-%D', ?)",
    "HOUR": "STRFTIME('%Y-%m-%DT%H', ?)",
    "MINUTE": "STRFTIME('%Y-%m-%DT%H:%M', ?)",
    "SECOND": "STRFTIME('%Y-%m-%DT%H:%M:%S', ?)"
}


def svl_to_sql(svl_plot):
    # TODO: Definitely docstring this.
    # Step 1: Process the selects.

    select_variables = []
    select_fields = []

    for axis in ["x", "y", "color"]:

        # Skip if the axis isn't in the plot.
        if axis not in svl_plot:
            continue

        # Select variables for use in the .fetchall( .. ) call.
        # These need to be in the same order as the ?'s appear in the queries.
        select_variables.append(get_in([axis, "field"], svl_plot, "*"))

        if "temporal" in svl_plot[axis]:
            select_fields.append("{} AS ?".format(
                TEMPORAL_CONVERTERS[svl_plot[axis]["temporal"]]
            ))
            # This one needs an extra variable, but we know there's a field
            # present this time.
            select_variables.append(svl_plot[axis]["field"])
        elif "agg" in svl_plot[axis]:
            # NOTE: Color axis will not take aggregations. This needs to be
            # implemented though.
            select_fields.append("{}(?) AS ?".format(
                svl_plot[axis]["agg"]
            ))
            # This one needs an extra variable.
            select_variables.append(
                "_".join([
                    svl_plot[axis]["agg"].lower(),
                    get_in([axis, "field"], svl_plot, "points")
                ])
            )
        else:
            select_fields.append("?")

    # Step 2: Process the aggregations.
    group_variables = []
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
            TEMPORAL_CONVERTERS[svl_plot[group_axis]["temporal"]]
        )
        group_variables.append(svl_plot[group_axis]["field"])
    elif group_axis:
        group_fields.append("?")
        group_variables.append(svl_plot[group_axis]["field"])

    # Only add the color to the group by if there's already a group axis.
    if group_axis and ("color" in svl_plot):
        group_fields.append("?")
        group_variables.append(svl_plot["color"]["field"])

    # Step 3: Build the query.
    query = "SELECT {} FROM ?".format(
        ", ".join(select_fields)
    )

    if group_axis:
        query = "{} GROUP BY {}".format(
            query,
            ", ".join(group_fields)
        )

    return query, (select_variables + [svl_plot["data"]] + group_variables)
