import pytest

from svl.errors import SvlMissingValue
from svl.svl import parse_svl


def test_missing_dataset_definition():
    """ Tests that the parse_svl function raises a SvlMissingValue
        exception when there's a missing dataset definition.
    """
    svl_string = """
    DATASETS
        bigfoot
    BAR bigfoot
        X classification
        Y classification COUNT
    """

    with pytest.raises(SvlMissingValue):
        parse_svl(svl_string)


def test_missing_dataset_label():
    """ Tests that the parse_svl function raises a SvlMissingValue
        exception when there's a missing dataset label on a plot.
    """
    svl_string = "HISTOGRAM X temperature"

    with pytest.raises(SvlMissingValue):
        parse_svl(svl_string)


def test_missing_axis_specifier():
    """ Tests that the parse_svl function raises a SvlMissingValue exception
        when there's a missing specifier for an axis.
    """
    svl_string = """
    DATASETS
        bigfoot "bigfoot_sightings.csv"
    PIE bigfoot AXIS LABEL "With Location"
    """

    with pytest.raises(SvlMissingValue):
        parse_svl(svl_string)


def test_missing_axis_field():
    """ Tests that the parse_svl function raises a SvlMissingValue exception
        when there's a missing field specified for an axis, but the axis
        contains an axis option.
    """
    svl_string = """
        BAR bigfoot X LABEL "Classification" Y classification COUNT
    """

    with pytest.raises(SvlMissingValue):
        parse_svl(svl_string)


def test_missing_title_value():
    """ Tests that the parse_svl function raises a SvlMissingValue exception
        when there's a missing title value.
    """
    svl_string = """
    LINE bigfoot X date BY YEAR Y classification COUNT TITLE
    """

    with pytest.raises(SvlMissingValue):
        parse_svl(svl_string)
