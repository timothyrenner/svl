class SvlSyntaxError(SyntaxError):
    """ Base class for SVL syntax errors.
    """

    label = "Syntax error"

    def __str__(self):
        context, line, column = self.args
        return "{} at line {}, column {} \n\n {}".format(
            self.label, line, column, context
        )


class SvlMissingValue(SvlSyntaxError):
    """ Missing values (i.e. missing field or dataset declarations).
    """

    label = "Missing value"


class SvlMissingParen(SvlSyntaxError):
    """ Missing or mismatched parens.
    """

    label = "Missing paren"


class SvlTypeError(SvlSyntaxError):
    """ Incorrect type for declarations with numeric stuff.
    """

    label = "Incorrect type"


class SvlInvalidTimeUnit(SvlSyntaxError):
    """ Invalid or unsupported temporal unit declarations.
    """

    label = "Time unit invalid or unsupported"


class SvlUnsupportedDeclaration(SvlSyntaxError):
    """ Declaration unsupported for the chart type (i.e. BINS on a line chart).
    """

    label = "Invalid declaration for this chart type"


class SvlInvalidAggregation(SvlSyntaxError):
    """ Aggregation function is not supported.
    """

    label = "Aggregation invalid or not supported"


class SvlInvalidSort(SvlSyntaxError):
    """ Invalid specifier for sorting.
    """

    label = "Sort can only be ASC or DESC"


SVL_SYNTAX_ERRORS = {
    SvlMissingValue: [
        # Missing label.
        """DATASETS "bigfoot.csv" LINE bigfoot X date Y temperature""",
        # Missing file or SQL specifier.
        "DATASETS bigfoot LINE bigfoot X date Y temperature",
        # Missing dataset specifier for plot.
        "DATASETS bigfoot SCATTER X latitude Y temperature",
        # Missing dataset specifier for plot without DATASETS.
        "BAR X classification Y classification COUNT",
        # Missing axis specifier.
        """DATASETS bigfoot "bigfoot.csv" PIE bigfoot AXIS TITLE "a" """,
        # Missing axis field.
        """LINE bigfoot X LABEL "x" Y temperature""",
        # Missing title.
        """PIE bigfoot AXIS has_location TITLE """,
        # Missing label value.
        """HISTOGRAM bigfoot X temperature_mid LABEL""",
        # Missing bin value.
        """HISTOGRAM bigfoot Y temperature_mid BINS""",
        # Missing step value.
        """HISTOGRAM bigfoot Y humidity STEP""",
        # ! Missing split by value.
        # ! Missing hole value.
        # Missing TRANSFORM value.
        """LINE bigfoot X TRANSFORM Y classification COUNT""",
        # Missing COLOR BY value.
        """BAR bigfoot X classification Y classification COUNT COLOR BY""",
        # Missing FILTER value.
        """PIE bigfoot AXIS has_location FILTER """,
        # Missing SORT value.
        """BAR bigfoot X classification Y classification COUNT SORT""",
    ],
    SvlMissingParen: [
        # Missing open paren on CONCAT.
        """CONCAT
                LINE bigfoot X date BY YEAR Y report_number COUNT
                HISTOGRAM bigfoot X temperature_mid
            )
        """,
        # Missing open paren on vcat.
        """
            LINE bigfoot X date BY YEAR Y report_number COUNT
            HISTOGRAM bigfoot X temperature_mid
        )
        """,
        # Missing close paren on CONCAT.
        """CONCAT(
            LINE bigfoot X date BY YEAR Y report_number COUNT
            HISTOGRAM bigfoot X temperature_mid
        """
        # ! Missing close paren on vcat.
    ],
    SvlTypeError: [
        # HOLE with non-number
        """PIE bigfoot AXIS classification HOLE "hi there" """
        # ! BINS with non-number
        # ! STEP with non-number
        # ! COLOR SCALE with non-string
        # ! TRANSFORM with non-string
        # ! FILTER with non-string
        # ! TITLE with non-string
        # ! LABEL with non-string
        # ! DATASET file with non-string
        # ! DATASET SQL with non-string
    ],
    SvlInvalidTimeUnit: [
        # ! TEMPORAL with invalid time unit.
    ],
    SvlInvalidAggregation: [
        # ! Aggregation with invalid function.
    ],
    SvlInvalidSort: [
        # SORT with invalid ASC / DESC.
        """BAR bigfoot X classification Y classification COUNT SORT DESCCCCC"""
    ],
    SvlUnsupportedDeclaration: [
        # BINS on a non-histogram chart.
        """BAR bigfoot X classification Y classification COUNT BINS 30""",
        # STEP on a non-histogram chart.
        """LINE bigfoot X date BY YEAR Y classification COUNT STEP 0.1""",
        # HOLE on a non-pie chart.
        """HISTOGRAM bigfoot Y humidity HOLE 0.9""",
        # Dimension of a pie chart.
        """PIE bigfoot X latitude"""
        # ! COLOR BY on a histogram or pie chart.
    ],
}


class SvlMissingFileError(Exception):
    """ A file specified as a dataset in the SVL program does not exist.
    """

    pass


class SvlMissingDatasetError(Exception):
    """ A dataset specified in an SVL plot is not in the dataset specifiers for
        the program.
    """

    pass


class SvlDataLoadError(Exception):
    """ An error occurred loading the dataset.
    """

    pass


class SvlPlotError(Exception):
    """ A plot is incorrectly specified.
    """

    pass


class SvlDataProcessingError(Exception):
    """ An error occurred processing the dataset.
    """

    pass
