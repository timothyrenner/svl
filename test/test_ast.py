from svl.compiler.ast import parse_svl


def test_line_chart():
    """ Tests that the line chart type is properly parsed.
    """

    svl_string = """
    DATASETS
        bigfoot "data/bigfoot_sightings.csv"
    LINE bigfoot
        X date by year LABEL "Year"
        Y date COUNT LABEL "Number of Sightings"
        SPLIT BY classification
        TITLE "Bigfoot Sightings by Year and Classification"
        FILTER "date > '1990-01-01'"
    """

    parsed_svl_truth = {
        "datasets": {"bigfoot": {"file": "data/bigfoot_sightings.csv"}},
        "vcat": [
            {
                "type": "line",
                "data": "bigfoot",
                "title": "Bigfoot Sightings by Year and Classification",
                "x": {"field": "date", "temporal": "YEAR", "label": "Year"},
                "y": {
                    "agg": "COUNT",
                    "field": "date",
                    "label": "Number of Sightings",
                },
                "split_by": {"field": "classification"},
                "filter": "date > '1990-01-01'",
            }
        ],
    }

    parsed_svl = parse_svl(svl_string)

    assert parsed_svl_truth == parsed_svl


def test_bar_chart():
    """ Tests that the bar chart type is properly parsed.
    """
    svl_string = """
    DATASETS
        bigfoot "data/bigfoot_sightings.csv"
    BAR bigfoot
        X classification
        Y classification COUNT
    """

    parsed_svl_truth = {
        "datasets": {"bigfoot": {"file": "data/bigfoot_sightings.csv"}},
        "vcat": [
            {
                "data": "bigfoot",
                "type": "bar",
                "x": {"field": "classification"},
                "y": {"agg": "COUNT", "field": "classification"},
            }
        ],
    }

    parsed_svl_answer = parse_svl(svl_string)

    assert parsed_svl_truth == parsed_svl_answer


def test_histogram_step():
    """ Tests that the histogram type is properly parsed when the step size
        is specified.
    """
    svl_string = """
    DATASETS
        bigfoot "data/bigfoot_sightings.csv"
    HISTOGRAM bigfoot
        X temperature_mid
        STEP 5
    """

    parsed_svl_truth = {
        "datasets": {"bigfoot": {"file": "data/bigfoot_sightings.csv"}},
        "vcat": [
            {
                "data": "bigfoot",
                "type": "histogram",
                "x": {"field": "temperature_mid"},
                "step": 5,
            }
        ],
    }

    parsed_svl_answer = parse_svl(svl_string)

    assert parsed_svl_truth == parsed_svl_answer


def test_histogram_bins():
    """ Tests that the histogram type is properly parsed when the number of
        bins is given as an argument.
    """
    svl_string = """
    DATASETS
        bigfoot "data/bigfoot_sightings.csv"
    HISTOGRAM bigfoot
        TITLE "Bigfoot Sighting Humidity"
        BINS 25
        Y humidity LABEL "Humidity"
    """

    parsed_svl_truth = {
        "datasets": {"bigfoot": {"file": "data/bigfoot_sightings.csv"}},
        "vcat": [
            {
                "data": "bigfoot",
                "title": "Bigfoot Sighting Humidity",
                "type": "histogram",
                "y": {"field": "humidity", "label": "Humidity"},
                "bins": 25,
            }
        ],
    }

    parsed_svl_answer = parse_svl(svl_string)

    assert parsed_svl_truth == parsed_svl_answer


def test_histogram_split_by():
    """ Tests that the histogram type is properly parsed.
    """
    svl_string = """
    DATASETS
        bigfoot "data/bigfoot_sightings.csv"
    HISTOGRAM bigfoot
        X temperature_mid
        STEP 5
        SPLIT BY classification
    """

    parsed_svl_truth = {
        "datasets": {"bigfoot": {"file": "data/bigfoot_sightings.csv"}},
        "vcat": [
            {
                "data": "bigfoot",
                "type": "histogram",
                "x": {"field": "temperature_mid"},
                "step": 5,
                "split_by": {"field": "classification"},
            }
        ],
    }

    parsed_svl_answer = parse_svl(svl_string)

    assert parsed_svl_truth == parsed_svl_answer


def test_pie():
    """ Tests that the pie type is properly parsed.
    """
    svl_string = """
    DATASETS
        bigfoot "data/bigfoot_sightings.csv"
    PIE bigfoot
        TITLE "Bigfoot Sightings with Location"
        HOLE 0.3
        AXIS TRANSFORM "CASE WHEN latitude IS NULL THEN 'no_location'
            ELSE 'has_location' END"
    """

    transform_truth = """CASE WHEN latitude IS NULL THEN \'no_location\'
            ELSE \'has_location\' END"""
    parsed_svl_truth = {
        "datasets": {"bigfoot": {"file": "data/bigfoot_sightings.csv"}},
        "vcat": [
            {
                "data": "bigfoot",
                "title": "Bigfoot Sightings with Location",
                "type": "pie",
                "axis": {"transform": transform_truth},
                "hole": 0.3,
            }
        ],
    }

    parsed_svl_answer = parse_svl(svl_string)
    print(parsed_svl_answer["vcat"])

    assert parsed_svl_truth == parsed_svl_answer


def test_scatter():
    """ Tests that the scatter type is properly parsed.
    """
    svl_string = """
    DATASETS
        bigfoot "data/bigfoot_sightings.csv"
    SCATTER bigfoot
        X latitude
        Y temperature_mid
        SPLIT BY classification
    """

    parsed_svl_truth = {
        "datasets": {"bigfoot": {"file": "data/bigfoot_sightings.csv"}},
        "vcat": [
            {
                "data": "bigfoot",
                "type": "scatter",
                "x": {"field": "latitude"},
                "y": {"field": "temperature_mid"},
                "split_by": {"field": "classification"},
            }
        ],
    }

    parsed_svl_answer = parse_svl(svl_string)

    assert parsed_svl_truth == parsed_svl_answer


def test_case_insensitivity():
    """ Tests that language keywords are case insensitive.
    """
    svl_string = """
    DATASETS
        bigfoot "data/bigfoot_sightings.csv"
    bar bigfoot
        x classification
        y classification CoUnT
    """

    parsed_svl_truth = {
        "datasets": {"bigfoot": {"file": "data/bigfoot_sightings.csv"}},
        "vcat": [
            {
                "data": "bigfoot",
                "type": "bar",
                "x": {"field": "classification"},
                "y": {"agg": "COUNT", "field": "classification"},
            }
        ],
    }

    parsed_svl_answer = parse_svl(svl_string)

    assert parsed_svl_truth == parsed_svl_answer


def test_comment():
    """ Tests that comments are ignored.
    """
    svl_string = """
    DATASETS
        -- Time to go squatchin.
        bigfoot "data/bigfoot_sightings.csv"
    HISTOGRAM bigfoot
        X temperature_mid
        STEP 5 -- Every five degrees should be granular enough.
    """

    parsed_svl_truth = {
        "datasets": {"bigfoot": {"file": "data/bigfoot_sightings.csv"}},
        "vcat": [
            {
                "data": "bigfoot",
                "type": "histogram",
                "x": {"field": "temperature_mid"},
                "step": 5,
            }
        ],
    }

    parsed_svl_answer = parse_svl(svl_string)

    assert parsed_svl_truth == parsed_svl_answer


def test_concat():
    """ Tests that the concat function is correctly parsed and transformed.
    """
    svl_string = """
    DATASETS
        bigfoot "data/bigfoot_sightings.csv"
    CONCAT(
        SCATTER bigfoot
            X latitude
            Y temperature_mid
        BAR bigfoot
            X classification
            Y classification COUNT
    )
    """

    parsed_svl_truth = {
        "datasets": {"bigfoot": {"file": "data/bigfoot_sightings.csv"}},
        "vcat": [
            {
                "hcat": [
                    {
                        "data": "bigfoot",
                        "type": "scatter",
                        "x": {"field": "latitude"},
                        "y": {"field": "temperature_mid"},
                    },
                    {
                        "data": "bigfoot",
                        "type": "bar",
                        "x": {"field": "classification"},
                        "y": {"agg": "COUNT", "field": "classification"},
                    },
                ]
            }
        ],
    }

    parsed_svl_answer = parse_svl(svl_string)

    assert parsed_svl_truth == parsed_svl_answer


def test_implicit_vcat():
    """ Tests that the implicit vertical concatenation of parenthesized
        charts is correctly parsed and transformed.
    """

    svl_string = """
    DATASETS
        bigfoot "data/bigfoot_sightings.csv"
    (
        SCATTER bigfoot
            X latitude
            Y temperature_mid
        BAR bigfoot
            X classification
            Y classification COUNT
    )
    """

    parsed_svl_truth = {
        "datasets": {"bigfoot": {"file": "data/bigfoot_sightings.csv"}},
        "vcat": [
            {
                "vcat": [
                    {
                        "data": "bigfoot",
                        "type": "scatter",
                        "x": {"field": "latitude"},
                        "y": {"field": "temperature_mid"},
                    },
                    {
                        "data": "bigfoot",
                        "type": "bar",
                        "x": {"field": "classification"},
                        "y": {"agg": "COUNT", "field": "classification"},
                    },
                ]
            }
        ],
    }

    parsed_svl_answer = parse_svl(svl_string)

    assert parsed_svl_truth == parsed_svl_answer


def test_sql_dataset():
    """ Tests that SQL-defined datasets are parsed correctly.
    """
    svl_string = """
    DATASETS
        bigfoot "bigfoot_sightings.csv"
        recent_bigfoot_sightings SQL
            "SELECT * FROM bigfoot WHERE date >= '2008-01-01'"
    HISTOGRAM recent_bigfoot_sightings
        X temperature_mid
    """

    parsed_svl_truth = {
        "datasets": {
            "bigfoot": {"file": "bigfoot_sightings.csv"},
            "recent_bigfoot_sightings": {
                "sql": "SELECT * FROM bigfoot WHERE date >= '2008-01-01'"
            },
        },
        "vcat": [
            {
                "data": "recent_bigfoot_sightings",
                "type": "histogram",
                "x": {"field": "temperature_mid"},
            }
        ],
    }

    parsed_svl_answer = parse_svl(svl_string)

    assert parsed_svl_truth == parsed_svl_answer


def test_no_datasets():
    """ Tests that the parse_svl function returns the correct value when
        there's no DATASETS directive.
    """
    svl_string = """
    HISTOGRAM bigfoot
        X temperature_mid
        SPLIT BY classification
    """

    truth = {
        "datasets": {
            # A validator would catch this, but from a parsing perspective this
            # is valid.
        },
        "vcat": [
            {
                "data": "bigfoot",
                "type": "histogram",
                "x": {"field": "temperature_mid"},
                "split_by": {"field": "classification"},
            }
        ],
    }

    answer = parse_svl(svl_string)

    assert truth == answer


def test_with_kwargs():
    """ Tests that the parse_svl function returns the correct value when the
        kwargs are used.
    """
    svl_string = """
    HISTOGRAM bigfoot
        X temperature_mid
        SPLIT BY classification
    """

    truth = {
        "datasets": {"bigfoot": {"file": "bigfoot_sightings.csv"}},
        "vcat": [
            {
                "data": "bigfoot",
                "type": "histogram",
                "x": {"field": "temperature_mid"},
                "split_by": {"field": "classification"},
            }
        ],
    }

    answer = parse_svl(svl_string, bigfoot="bigfoot_sightings.csv")

    assert truth == answer


def test_sort():
    """ Tests that the parse_svl function returns the correct value with a
        SORT modifier on one axis.
    """
    svl_string = """
    DATASETS
        bigfoot "bigfoot_sightings.csv"
    BAR bigfoot
        X classification SORT ASC
        Y classification COUNT
    """

    truth = {
        "datasets": {"bigfoot": {"file": "bigfoot_sightings.csv"}},
        "vcat": [
            {
                "data": "bigfoot",
                "type": "bar",
                "x": {"field": "classification", "sort": "ASC"},
                "y": {"field": "classification", "agg": "COUNT"},
            }
        ],
    }

    answer = parse_svl(svl_string)

    assert truth == answer


def test_color_by():
    """ Tests that the parse_svl function can parse SVL with a COLOR BY.
    """
    svl_string = """
    DATASETS
        bigfoot "bigfoot_sightings.csv"
    LINE bigfoot
        X date BY YEAR
        Y report_id COUNT LABEL "Number of Sightings"
        COLOR BY temperature_mid AVG "Jet" LABEL "Average Temperature (F)"
    """

    truth = {
        "datasets": {"bigfoot": {"file": "bigfoot_sightings.csv"}},
        "vcat": [
            {
                "data": "bigfoot",
                "type": "line",
                "x": {"field": "date", "temporal": "YEAR"},
                "y": {
                    "field": "report_id",
                    "agg": "COUNT",
                    "label": "Number of Sightings",
                },
                "color_by": {
                    "field": "temperature_mid",
                    "agg": "AVG",
                    "color_scale": "Jet",
                    "label": "Average Temperature (F)",
                },
            }
        ],
    }

    answer = parse_svl(svl_string)

    assert truth == answer


def test_split_by_transform():
    """ Tests that the SPLIT BY directive with a TRANSFORM returns the
        correct value.
    """
    svl_string = """
    DATASETS
        bigfoot "bigfoot_sightings.csv"
    LINE bigfoot
        X date BY YEAR
        Y report_id COUNT
        SPLIT BY TRANSFORM
            "CASE WHEN temperature > 85 THEN 'hot' ELSE 'not_hot' END"
    """
    truth = {
        "datasets": {"bigfoot": {"file": "bigfoot_sightings.csv"}},
        "vcat": [
            {
                "data": "bigfoot",
                "type": "line",
                "x": {"field": "date", "temporal": "YEAR"},
                "y": {"field": "report_id", "agg": "COUNT"},
                "split_by": {
                    "transform": "CASE WHEN temperature > 85 THEN 'hot' "
                    "ELSE 'not_hot' END"
                },
            }
        ],
    }
    answer = parse_svl(svl_string)

    assert truth == answer


def test_split_by_temporal():
    """ Tests that the SPLIT BY directive with a TEMPORAL modifier returns
        the correct value.
    """
    svl_string = """
    DATASETS bigfoot "bigfoot_sightings.csv"
    BAR bigfoot
        X classification
        Y report_number COUNT
        SPLIT BY date BY YEAR
    """
    truth = {
        "datasets": {"bigfoot": {"file": "bigfoot_sightings.csv"}},
        "vcat": [
            {
                "data": "bigfoot",
                "type": "bar",
                "x": {"field": "classification"},
                "y": {"field": "report_number", "agg": "COUNT"},
                "split_by": {"field": "date", "temporal": "YEAR"},
            }
        ],
    }

    answer = parse_svl(svl_string)
    assert truth == answer


def test_split_by_label():
    """ Tests that the SPLIT BY directive with a LABEL modifier returns
        the correct value.
    """
    svl_string = """
    DATASETS bigfoot "bigfoot_sightings.csv"
    HISTOGRAM bigfoot
        X temperature
        SPLIT BY classification LABEL "Classification"
    """

    truth = {
        "datasets": {"bigfoot": {"file": "bigfoot_sightings.csv"}},
        "vcat": [
            {
                "data": "bigfoot",
                "type": "histogram",
                "x": {"field": "temperature"},
                "split_by": {
                    "field": "classification",
                    "label": "Classification",
                },
            }
        ],
    }

    answer = parse_svl(svl_string)
    assert truth == answer
