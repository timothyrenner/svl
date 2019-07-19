import pytest

from svl.compiler.errors import (
    SvlSyntaxError,
    SvlMissingValue,
    SvlMissingParen,
    SvlTypeError,
    SvlUnsupportedDeclaration,
)
from svl.compiler.ast import parse_svl


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


def test_missing_split_by_value():
    """ Tests that the parse_svl function raises a SvlSyntaxError exception
        when there's a missing split by value.
    """
    svl_string = """
    DATASETS bigfoot "bigfoot.csv"
    HISTOGRAM bigfoot X temperature_mid SPLIT BY
    """

    # TODO Get a more specific exception here.
    with pytest.raises(SvlSyntaxError):
        parse_svl(svl_string)


def test_missing_hole_value():
    """ Tests that the parse_svl function raises a SvlSyntaxError exception
        when there's a missing HOLE value.
    """
    svl_string = """PIE bigfoot AXIS classification HOLE"""

    # TODO Get a more specific exception here.
    with pytest.raises(SvlSyntaxError):
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


def test_missing_close_paren_vcat():
    """ Tests that the parse_svl function raises a SvlSyntaxError exception
        when there's a missing close paren on a vcat.
    """
    svl_string = """
    (
        HISTOGRAM bigfoot X temperature_mid
        HISTOGRAM bigfoot Y temperature_high
    """

    # TODO Add a more specific exception here.
    with pytest.raises(SvlSyntaxError):
        parse_svl(svl_string)


def test_bins_with_non_number():
    """ Tests that the parse_svl function raises a SvlSyntaxError exception
        when there's a non-number in a BINS declaration.
    """
    svl_string = """
    DATASETS bigfoot "bigfoot.csv"
    HISTOGRAM bigfoot X temperature_mid BINS hi
    """

    # TODO Make exception more specific if possible.
    with pytest.raises(SvlSyntaxError):
        parse_svl(svl_string)


def test_step_with_non_number():
    """ Tests that the parse_svl function raises a SvlSyntaxError exception
        when there's a non-number in a STEP declaration.
    """
    svl_string = """
    DATASETS bigfoot "bigfoot.csv"
    HISTOGRAM bigfoot STEP "hello there" X temperature_mid
    """

    # TODO make exception more specific if possible.
    with pytest.raises(SvlSyntaxError):
        parse_svl(svl_string)


def test_color_scale_with_non_string():
    """ Tests that the parse_svl function raises a SvlSyntaxError exception
        when there's a non-string in a COLOR BY declaration.
    """
    svl_string = """
    DATASETS bigfoot "bigfoot.csv"
    SCATTER bigfoot X date BY DAY Y date COUNT COLOR BY humidity MAX 2.1
    """

    with pytest.raises(SvlSyntaxError):
        parse_svl(svl_string)


def test_transform_with_non_string():
    """ Tests that the parse_svl function raises a SvlSyntaxError exception
        when there's a non-string in a TRANSFORM declaration.
    """
    svl_string = """
    DATASETS bigfoot "bigfoot.csv"
    SCATTER bigfoot X TRANSFORM 1.2 Y temperature_mid
    """

    with pytest.raises(SvlSyntaxError):
        parse_svl(svl_string)


def test_hole_with_non_number():
    """ Tests that the parse_svl function raises a SvlTypeError exception
        when there's a non-number in a HOLE declaration.
    """
    svl_string = """
    DATASETS bigfoot "bigfoot.csv"
    PIE bigfoot HOLE hi AXIS classification
    """

    with pytest.raises(SvlTypeError):
        parse_svl(svl_string)


def test_filter_with_non_string():
    """ Tests that the parse_svl function raises a SvlSyntaxError exception
        when there's a non-string in a FILTER declaration.
    """
    svl_string = """
    DATASETS bigfoot "bigfoot.csv"
    LINE bigfoot
        X date BY YEAR
        Y date COUNT
        FILTER date
    """

    # TODO Make this exception more specific if possible
    with pytest.raises(SvlSyntaxError):
        parse_svl(svl_string)


def test_title_with_non_string():
    """ Tests that the parse_svl function raises a SvlSyntaxError exception
        when there's a non-string in a TITLE declaration.
    """
    svl_string = """
    DATASETS bigfoot "bigfoot.csv"
    LINE bigfoot
        X date BY YEAR
        TITLE 1
        Y date COUNT
        SPLIT BY classification
    """

    # TODO Make this exception more specific if possible.
    with pytest.raises(SvlSyntaxError):
        parse_svl(svl_string)


def test_label_with_non_string():
    """ Tests that the parse_svl function raises a SvlSyntaxError exception
        when there's a non-string in a LABEL declaration.
    """
    svl_string = """
    DATASETS bigfoot "bigfoot.csv"
    LINE bigfoot
        Y classification COUNT
        SPLIT BY classification
        X date BY YEAR LABEL 1.2
    """

    # TODO Make this exception more specific if possible.
    with pytest.raises(SvlSyntaxError):
        parse_svl(svl_string)


def test_dataset_file_with_non_string():
    """ Tests that the parse_svl function raises a SvlSyntaxError exception
        when there's a non-string in a DATASETS file declaration.
    """
    svl_string = """
    DATASETS bigfoot 3
    LINE bigfoot X date BY YEAR Y date COUNT
    """

    # TODO Make this exception more specific if possible.
    with pytest.raises(SvlSyntaxError):
        parse_svl(svl_string)


def test_dataset_sql_with_non_string():
    """ Tests that the parse_svl function raises a SvlSyntaxError exception
        when there's a non-string in a DATASETS SQL declaration.
    """
    svl_string = """
    DATASETS
        bigfoot "bigfoot.csv"
        bigfoot_with_location SQL 3
    PIE bigfoot_with_location AXIS has_location
    """

    # TODO Make this exception more specific if possible.
    with pytest.raises(SvlSyntaxError):
        parse_svl(svl_string)


def test_temporal_with_invalid_specifier():
    """ Tests that the parse_svl function raises a SvlSyntaxError exception
        when there's an invalid temporal specifier.
    """
    svl_string = """
    DATASETS bigfoot "bigfoot.csv"
    LINE bigfoot Y temporal BY NOPE X classification COUNT
    """

    # TODO Make this exception more specific if possible.
    with pytest.raises(SvlSyntaxError):
        parse_svl(svl_string)


def test_invalid_aggregation():
    """ Tests that the parse_svl function raises a SvlSyntaxError
        exception when there's an invalid aggregation function.
    """
    svl_string = """
    DATASETS bigfoot "bigfoot.csv"
        LINE bigfoot X date BY YEAR Y temperature_mid ARGMIN
    """

    # TODO Make this exception more specific if possible.
    with pytest.raises(SvlSyntaxError):
        parse_svl(svl_string)


def test_invalid_sort():
    """ Tests that the parse_svl function raises a SvlInvalidSort error when
        there's an invalid SORT argument.
    """
    svl_string = """
    DATASETS bigfoot "bigfoot.csv"
    LINE bigfoot X date SORT OOPS Y classification COUNT
    """

    with pytest.raises(SvlSyntaxError):
        parse_svl(svl_string)


def test_bins_on_non_histogram():
    """ Tests that the parse_svl function raises a SvlUnsupportedDeclaration
        exception when there's a BINS declaration on a non-histogram chart.
    """
    svl_string = """
    Datasets bigfoot "bigfoot.csv"
    LINE bigfoot X date BY YEAR Y classification COUNT BINS 40
    """

    with pytest.raises(SvlUnsupportedDeclaration):
        parse_svl(svl_string)


def test_step_on_non_histogram():
    """ Tests that the parse_svl function raises a SvlUnsupportedDeclaration
        exception when there's a STEP declaration on a non-histogram chart.
    """
    svl_string = """
    datasets bigfoot "bigfoot.csv"
    BAR bigfoot X classification Y classification COUNT STEP 0.1
    """

    with pytest.raises(SvlUnsupportedDeclaration):
        parse_svl(svl_string)


def test_hole_on_non_pie():
    """ Tests that the parse_svl function raises a SvlUnsupportedDeclaration
        exception when there's a HOLE declaration on a non-pie chart.
    """
    svl_string = """
    datasets bigfoot "bigfoot.csv"
    SCATTER bigfoot X latitude Y temperature_mid HOLE 0.2
    """

    with pytest.raises(SvlUnsupportedDeclaration):
        parse_svl(svl_string)


def test_dimension_on_pie():
    """ Tests that the parse_svl function raises a SvlUnsupportedDeclaration
        exception when there's a dimension declared for a pie chart.
    """
    svl_string = """
    DATASETS bigfoot "bigfoot.csv"
    PIE bigfoot X classification
    """

    with pytest.raises(SvlUnsupportedDeclaration):
        parse_svl(svl_string)


def test_color_by_on_wrong_chart():
    """ Tests that the parse_svl function raises a SvlSyntaxError
        exception when there's a color by declared for a non-xy chart.
    """
    svl_string = """
    DATASETS bigfoot "bigfoot.csv"
    PIE bigfoot AXIS classification COLOR BY humidity
    """

    # TODO Make this exception more specific if possible.
    with pytest.raises(SvlSyntaxError):
        parse_svl(svl_string)
