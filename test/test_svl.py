from svl import parse_svl


def test_line_chart():
    """ Tests that the line chart type is properly parsed.
    """

    svl_string = """
    DATASETS
        bigfoot "data/bigfoot_sightings.csv"
    LINE bigfoot
        X date BY YEAR
        Y COUNT
        COLOR classification
    """

    parsed_svl_truth = {
        "datasets": {
            "bigfoot": "data/bigfoot_sightings.csv"
        },
        "vcat": [{
            "type": "line",
            "data": "bigfoot",
            "x": {
                "field": "date",
                "temporal": "YEAR"
            },
            "y": {
                "agg": "COUNT"
            },
            "color": {
                "field": "classification"
            }
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
        Y COUNT
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
                "agg": "COUNT"
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
        humidity BINS 25
    """

    parsed_svl_truth = {
        "datasets": {
            "bigfoot": "data/bigfoot_sightings.csv"
        }, "vcat": [{
            "data": "bigfoot",
            "type": "histogram",
            "field": "humidity",
            "bins": 25
        }]
    }

    parsed_svl_answer = parse_svl(svl_string)

    assert parsed_svl_truth == parsed_svl_answer


def test_boxplot():
    """ Tests that the boxplot type is properly parsed.
    """
    svl_string = """
    DATASETS
        bigfoot "data/bigfoot_sightings.csv"
    BOXPLOT bigfoot
        X classification
        Y temperature_mid
    """

    parsed_svl_truth = {
        "datasets": {
            "bigfoot": "data/bigfoot_sightings.csv"
        },
        "vcat": [{
            "data": "bigfoot",
            "type": "boxplot",
            "x": {
                "field": "classification"
            },
            "y": {
                "field": "temperature_mid"
            }
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
        COLOR classification
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
            "color": {
                "field": "classification"
            }
        }]
    }

    parsed_svl_answer = parse_svl(svl_string)

    assert parsed_svl_truth == parsed_svl_answer
