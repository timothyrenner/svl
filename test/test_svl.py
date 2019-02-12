from svl import parse_svl


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
        "datasets": {
            "bigfoot": {
                "file": "data/bigfoot_sightings.csv"
            }
        },
        "vcat": [{
            "type": "line",
            "data": "bigfoot",
            "title": "Bigfoot Sightings by Year and Classification",
            "x": {
                "field": "date",
                "temporal": "YEAR",
                "label": "Year"
            },
            "y": {
                "agg": "COUNT",
                "field": "date",
                "label": "Number of Sightings"
            },
            "split_by": {
                "field": "classification"
            },
            "filter": "date > '1990-01-01'"
        }]
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
        "datasets": {
            "bigfoot": {
                "file": "data/bigfoot_sightings.csv"
            }
        },
        "vcat": [{
            "data": "bigfoot",
            "type": "bar",
            "x": {
                "field": "classification"
            },
            "y": {
                "agg": "COUNT",
                "field": "classification"
            }
        }]
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
        AXIS temperature_mid
        STEP 5
    """

    parsed_svl_truth = {
        "datasets": {
            "bigfoot": {
                "file": "data/bigfoot_sightings.csv"
            }
        },
        "vcat": [{
            "data": "bigfoot",
            "type": "histogram",
            "axis": {
                "field": "temperature_mid"
            },
            "step": 5
        }]
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
        AXIS humidity LABEL "Humidity"
    """

    parsed_svl_truth = {
        "datasets": {
            "bigfoot": {
                "file": "data/bigfoot_sightings.csv"
            }
        }, "vcat": [{
            "data": "bigfoot",
            "title": "Bigfoot Sighting Humidity",
            "type": "histogram",
            "axis": {
                "field": "humidity",
                "label": "Humidity"
            },
            "bins": 25
        }]
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
        "datasets": {
            "bigfoot": {
                "file": "data/bigfoot_sightings.csv"
            }
        },
        "vcat": [{
            "data": "bigfoot",
            "title": "Bigfoot Sightings with Location",
            "type": "pie",
            "axis": {
                "transform": transform_truth
            },
            "hole": 0.3
        }]
    }

    parsed_svl_answer = parse_svl(svl_string)
    print(parsed_svl_answer['vcat'])

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
        "datasets": {
            "bigfoot": {
                "file": "data/bigfoot_sightings.csv"
            }
        },
        "vcat": [{
            "data": "bigfoot",
            "type": "scatter",
            "x": {
                "field": "latitude"
            },
            "y": {
                "field": "temperature_mid"
            },
            "split_by": {
                "field": "classification"
            }
        }]
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
        "datasets": {
            "bigfoot": {
                "file": "data/bigfoot_sightings.csv"
            }
        },
        "vcat": [{
            "data": "bigfoot",
            "type": "bar",
            "x": {
                "field": "classification"
            },
            "y": {
                "agg": "COUNT",
                "field": "classification"
            }
        }]
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
        AXIS temperature_mid
        STEP 5 -- Every five degrees should be granular enough.
    """

    parsed_svl_truth = {
        "datasets": {
            "bigfoot": {
                "file": "data/bigfoot_sightings.csv"
            }
        },
        "vcat": [{
            "data": "bigfoot",
            "type": "histogram",
            "axis": {
                "field": "temperature_mid"
            },
            "step": 5
        }]
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
        "datasets": {
            "bigfoot": {
                "file": "data/bigfoot_sightings.csv"
            }
        },
        "vcat": [{
            "hcat": [
                {
                    "data": "bigfoot",
                    "type": "scatter",
                    "x": {"field": "latitude"},
                    "y": {"field": "temperature_mid"}
                }, {
                    "data": "bigfoot",
                    "type": "bar",
                    "x": {"field": "classification"},
                    "y": {"agg": "COUNT", "field": "classification"}
                }
            ]
        }]
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
        "datasets": {
            "bigfoot": {
                "file": "data/bigfoot_sightings.csv"
            }
        },
        "vcat": [{
            "vcat": [
                {
                    "data": "bigfoot",
                    "type": "scatter",
                    "x": {"field": "latitude"},
                    "y": {"field": "temperature_mid"}
                }, {
                    "data": "bigfoot",
                    "type": "bar",
                    "x": {"field": "classification"},
                    "y": {"agg": "COUNT", "field": "classification"}
                }
            ]
        }]
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
        AXIS temperature_mid
    """

    parsed_svl_truth = {
        "datasets": {
            "bigfoot": {
                "file": "bigfoot_sightings.csv"
            },
            "recent_bigfoot_sightings": {
                "sql": "SELECT * FROM bigfoot WHERE date >= '2008-01-01'"
            }
        },
        "vcat": [{
            "data": "recent_bigfoot_sightings",
            "type": "histogram",
            "axis": {
                "field": "temperature_mid"
            }
        }]
    }

    parsed_svl_answer = parse_svl(svl_string)

    assert parsed_svl_truth == parsed_svl_answer
