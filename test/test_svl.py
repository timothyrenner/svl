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
    assert False  # TODO: Implement.


def test_histogram():
    """ Tests that the histogram type is properly parsed.
    """
    assert False  # TODO: Implement.


def test_boxplot():
    """ Tests that the boxplot type is properly parsed.
    """
    assert False  # TODO: Implement.


def test_scatter():
    """ Tests that the scatter type is properly parsed.
    """
    assert False  # TODO: Implement.
