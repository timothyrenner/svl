class SvlSyntaxError(SyntaxError):
    def __str__(self):
        context, line, column = self.args
        return "{} at line {}, column {} \n\n {}".format(
            self.label,
            line,
            column,
            context
        )


class SvlMissingValue(SvlSyntaxError):
    label = "Missing value."


SVL_SYNTAX_ERRORS = {
    SvlMissingValue: [
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
        """HISTOGRAM bigfoot Y humidity STEP"""
        # TODO Missing split by value.
        # TODO Missing hole value.
    ]
}
