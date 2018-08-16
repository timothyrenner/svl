import maya
import math

from toolz import curry, merge, identity, compose


def _convert_datetime(dt, snap):
    """ Takes a string, converts to a MayaDT object, snaps it, then returns
        an ISO string for plotly to format appropriately.
    """
    return maya.parse(dt).snap(snap).iso8601()


TEMPORAL_CONVERTERS = {
    "YEAR": curry(_convert_datetime)(snap="@y"),
    "MONTH": curry(_convert_datetime)(snap="@mon"),
    "DAY": curry(_convert_datetime)(snap="@d"),
    "HOUR": curry(_convert_datetime)(snap="@h"),
    "MINUTE": curry(_convert_datetime)(snap="@m"),
    "SECOND": curry(_convert_datetime)(snap="@s")
}


def transform(field, transformation, datum):
    # Replace the value in the datum with a transformation on the field.
    return merge(datum, {field: transformation(datum[field])})


def append(*fields):

    data = {}

    def _append(datum):
        for field in fields:

            # Initialize to an empty list if the field isn't present.
            if field not in data:
                data[field] = []

            # Append the values to the field.
            data[field].append(datum[field])

        return data

    return _append


def _mean(a, x):
    new_sum = a["sum"] + x
    new_count = a["count"] + 1
    new_avg = new_sum / new_count

    return {
        "sum": new_sum,
        "count": new_count,
        "avg": new_avg
    }


AGG_FUNCTIONS = {
    "COUNT": lambda a, x: a+1,
    "MIN": min,
    "MAX": max,
    "AVG": _mean
}

AGG_INITS = {
    "COUNT": 0,
    "MIN": math.inf,
    "MAX": -math.inf,
    "AVG": {"sum": 0, "count": 0}
}


def aggregate(group_field, agg_field, agg_func):

    aggregated_values = {}

    def _aggregate(datum):
        if datum[group_field] not in aggregated_values:
            aggregated_values[datum[group_field]] = AGG_INITS[agg_func]

        aggregated_values[datum[group_field]] = AGG_FUNCTIONS[agg_func](
            aggregated_values[datum[group_field]],
            datum[agg_field]
        )

        return aggregated_values

    return _aggregate


def color(color_field, transformer):

    # The values will hold the data.
    color_values = {}
    # The transformers hold the transformations of the fields underneath the
    # colors.
    color_transformers = {}

    def _color(datum):
        # If it's a new color, initialize a transformer for that color.
        if datum[color_field] not in color_values:
            color_transformers[datum[color_field]] = transformer()

        # Now apply that transformer to the data point under that color.
        color_values[datum[color_field]] = \
            color_transformers[datum[color_field]](datum)

        return color_values

    return _color


def plot_to_reducer(svl_plot):

    if svl_plot["type"] == "histogram":
        # Histograms are pretty easy - just append the one field.
        transformer = append(svl_plot["field"])
    else:
        # Non-histograms are a little more complicated.

        # Base transformer is the identity.
        transformer = identity

        # Step one is to construct the mappable transformations.

        # Apply the temporal transformations by composing them with the
        # transformer.
        if "temporal" in svl_plot["x"]:
            temporal_transform_x = curry(transform)(
                field="x",
                transformation=TEMPORAL_CONVERTERS[svl_plot["x"]["temporal"]]
            )
            transformer = compose(temporal_transform_x, transformer)

        if "temporal" in svl_plot["y"]:
            temporal_transform_y = curry(transform)(
                field="y",
                transformation=TEMPORAL_CONVERTERS[svl_plot["y"]["temporal"]]
            )
            transformer = compose(temporal_transform_y, transformer)

        # Step 2: Determine if it's an aggregation or appendation (?)and create
        # a delayed transformer.
        if ("agg" in svl_plot["x"]) or ("agg" in svl_plot["y"]):
            if "agg" in svl_plot["x"]:
                group_field = "y"
                agg_field = "x"
                agg_func = AGG_FUNCTIONS[svl_plot["x"]["agg"]]
            else:
                group_field = "x"
                agg_field = "y"
                agg_func = AGG_FUNCTIONS[svl_plot["y"]["agg"]]

            # Delay evaluation in case there's a color field.
            def delayed_transformer():
                return aggregate(
                    group_field,
                    agg_field,
                    agg_func
                )
        else:
            def delayed_transformer():
                return compose(
                    append(svl_plot["x"]["field"]),
                    append(svl_plot["y"]["field"])
                )

        # Step 3: Now determine if it's a color transformer or not. If not,
        # materialize the delayed transformer, otherwise build the color
        # transformer with the delayed transformer inside it.
        if "color" in svl_plot:
            # For color transformations, we need the function that generates
            # the transformers.
            transformer = compose(
                color(svl_plot["color"], delayed_transformer),
                transformer
            )
        else:
            # For non-aggregations we only need the one transformer, so call
            # the delayed function.
            transformer = compose(
                delayed_transformer(),
                transformer
            )

    return transformer


def construct_data(svl_plots, data):
    reducers = [plot_to_reducer(p) for p in svl_plots]
    constructed_data = [None]*len(reducers)

    for datum in data:
        # Apply each reducer to the datum, replacing previous values.
        for ii, reducer in enumerate(reducers):
            constructed_data[ii] = reducer(datum)

    return constructed_data
