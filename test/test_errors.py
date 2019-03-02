import pytest

from svl.errors import SvlMissingValue, SvlMissingParen
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


def test_missing_dataset_name():
    """ Tests that the parse_svl function raises a SvlMissingValue
        exception when there's a missing dataset name.
    """
    svl_string = """
    DATASETS
        "bigfoot.csv"
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


def test_missing_label_value():
    """ Tests that the parse_svl function raises a SvlMissingValue exception
        when there's a missing label value.
    """
    svl_string = """
    DATASETS
        bigfoot "bigfoot.csv"
    SCATTER bigfoot
        X date BY YEAR LABEL
        Y report_number COUNT
        SPLIT BY classification
    """

    with pytest.raises(SvlMissingValue):
        parse_svl(svl_string)


def test_missing_bins_value():
    """ Tests that the parse_svl function raises a SvlMissingValue exception
        when there's a missing bins value.
    """
    svl_string = """
    DATASETS
        bigfoot "bigfoot.csv"
    HISTOGRAM bigfoot
        X humidity BINS LABEL "Humidity"
    """

    with pytest.raises(SvlMissingValue):
        parse_svl(svl_string)


def test_missing_step_value():
    """ Tests that the parse_svl function raises a SvlMissingValue exception
        when there's a missing step value.
    """
    svl_string = """
    DATASETS bigfoot "bigfoot.csv"
    HISTOGRAM bigfoot STEP X moon_phase
    """

    with pytest.raises(SvlMissingValue):
        parse_svl(svl_string)


def test_missing_transform_value():
    """ Tests that the parse_svl function raises a SvlMissingValue exception
        when there's a missing transform value.
    """
    svl_string = """
    DATASETS bigfoot "bigfoot.csv"
    SCATTER bigfoot X latitude Y TRANSFORM
    """

    with pytest.raises(SvlMissingValue):
        parse_svl(svl_string)


def test_missing_color_by_value():
    """ Tests that the parse_svl function raises a SvlMissingValue exception
        when there's a missing color by value.
    """
    svl_string = """
    DATASETS bigfoot "bigfoot.csv"
    SCATTER bigfoot X latitude Y temperature_mid COLOR BY
    """

    with pytest.raises(SvlMissingValue):
        parse_svl(svl_string)


def test_missing_filter_value():
    """ Tests that the parse_svl function raises a SvlMissingValue exception
        when there's a missing filter value.
    """
    svl_string = """
    DATASETS bigfoot "bigfoot.csv"
    LINE bigfoot X date BY YEAR Y report_number COUNT FILTER
    """

    with pytest.raises(SvlMissingValue):
        parse_svl(svl_string)


def test_missing_sort_value():
    """ Tests that the parse_svl function raises a SvlMissingValue exception
        when there's a missing sort value.
    """
    svl_string = """
    DATASETS bigfoot "bigfoot.csv"
    BAR bigfoot X classification SORT Y classification COUNT
    """

    with pytest.raises(SvlMissingValue):
        parse_svl(svl_string)


def test_missing_open_paren():
    """ Tests that the parse_svl function raises a SvlMissingValue exception
        when there's a missing open paren.
    """
    svl_string = """
    DATASETS bigfoot "bigfoot.csv"
    CONCAT
        SCATTER bigfoot X latitude Y temperature_mid
        PIE bigfoot AXIS classification
    )
    """

    with pytest.raises(SvlMissingParen):
        parse_svl(svl_string)


def test_missing_open_paren_vcat():
    """ Tests that the parse_svl function raises a SvlMissingValue exception
        when there's a missing open paren on a vcat.
    """
    svl_string = """
    DATASETS bigfoot "bigfoot.csv"
        SCATTER bigfoot X latitude Y temperature_mid
        PIE bigfoot AXIS classification HOLE 0.2
    )
    """

    with pytest.raises(SvlMissingParen):
        parse_svl(svl_string)


def test_missing_close_paren():
    """ Tests that the parse_svl function raises a SvlMissingValue exception
        when there's a missing close paren on a concat.
    """
    svl_string = """
    DATASETS bigfoot "bigfoot.csv"
    CONCAT(
        HISTOGRAM bigfoot X temperature_mid
        HISTOGRAM bigfoot X temperature_high
    """

    with pytest.raises(SvlMissingParen):
        parse_svl(svl_string)
