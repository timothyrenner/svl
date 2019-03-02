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


class SvlMissingParen(SvlSyntaxError):
    label = "Missing paren."


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
        # TODO Missing split by value.
        # TODO Missing hole value.
        # Missing TRANSFORM value.
        """LINE bigfoot X TRANSFORM Y classification COUNT""",
        # Missing COLOR BY value.
        """BAR bigfoot X classification Y classification COUNT COLOR BY""",
        # Missing FILTER value.
        """PIE bigfoot AXIS has_location FILTER """,
        # Missing SORT value.
        """BAR bigfoot X classification Y classification COUNT SORT"""
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
        # TODO Missing close paren on vcat.
    ]
}
