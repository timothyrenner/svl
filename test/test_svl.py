from svl import parse_svl


def test_line_chart():
    """ Tests that the line chart type is properly parsed.
    """

    svl_string = """
    DATASETS
        bigfoot "data/bigfoot_sightings.csv"
    LINE bigfoot
        TITLE "Bigfoot Sightings by Year and Classification"
        X date BY YEAR LABEL "Year"
        Y COUNT date LABEL "Number of Sightings"
        SPLIT BY classification
        FILTER "date > '1990-01-01'"
    """

    parsed_svl_truth = {
        "datasets": {
            "bigfoot": "data/bigfoot_sightings.csv"
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
        Y COUNT classification
    """

    parsed_svl_truth = {
        "datasets": {
            "bigfoot": "data/bigfoot_sightings.csv"
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
        temperature_mid STEP 5
    """

    parsed_svl_truth = {
        "datasets": {
            "bigfoot": "data/bigfoot_sightings.csv"
        },
        "vcat": [{
            "data": "bigfoot",
            "type": "histogram",
            "field": "temperature_mid",
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
        humidity BINS 25 LABEL "Humidity"
    """

    parsed_svl_truth = {
        "datasets": {
            "bigfoot": "data/bigfoot_sightings.csv"
        }, "vcat": [{
            "data": "bigfoot",
            "title": "Bigfoot Sighting Humidity",
            "type": "histogram",
            "field": "humidity",
            "label": "Humidity",
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
        TITLE "Bigfoot Sightings by Classification"
        classification
        HOLE 0.3
    """

    parsed_svl_truth = {
        "datasets": {
            "bigfoot": "data/bigfoot_sightings.csv"
        },
        "vcat": [{
            "data": "bigfoot",
            "title": "Bigfoot Sightings by Classification",
            "type": "pie",
            "field": "classification",
            "hole": 0.3
        }]
    }

    parsed_svl_answer = parse_svl(svl_string)

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
            "bigfoot": "data/bigfoot_sightings.csv"
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
            Y COUNT classification
    )
    """

    parsed_svl_truth = {
        "datasets": {
            "bigfoot": "data/bigfoot_sightings.csv"
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
            Y COUNT classification
    )
    """

    parsed_svl_truth = {
        "datasets": {
            "bigfoot": "data/bigfoot_sightings.csv"
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
