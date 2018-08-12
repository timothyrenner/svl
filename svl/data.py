import maya

from toolz import curry
from statistics import mean


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


AGG_FUNCTIONS = {
    "COUNT": len,
    "MIN": min,
    "MAX": max,
    "AVG": mean
}
