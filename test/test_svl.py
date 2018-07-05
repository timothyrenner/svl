from svl import parse_svl


def test_bar_chart():
    """ Tests that the parse_svl function returns the correct dictionary when
        given a bar chart.
    """

    chart_string = """
    DATASETS
        bigfoot "data/bigfoot_sightings.csv"
    BAR bigfoot
        X classification TYPE "nominal"
        Y AGGREGATE "count"
    """

    chart_dict_truth = {
        "$schema": "https://vega.github.io/schema/vega-lite/v2.0.json",
        "datasets": {
            "bigfoot": "data/bigfoot_sightings.csv"
        },
        "vconcat": [
            {
                "data": {"name": "bigfoot"},
                "mark": "bar",
                "encoding": {
                    "x": {"field": "classification", "type": "nominal"},
                    "y": {"aggregate": "count", "type": "quantitative"}
                }
            }
        ]
    }

    chart_dict_answer = parse_svl(chart_string)

    assert chart_dict_truth == chart_dict_answer


def test_concat():
    """ Tests that the parse_svl function returns the correct value when two
        plots are concatenated on the same line.
    """

    chart_string = """
    DATASETS
        bigfoot "data/bigfoot_sightings.csv"
    CONCAT (
        BAR bigfoot
            X classification TYPE "nominal"
            Y AGGREGATE "count"
        BAR bigfoot
            X temperature_mid BIN STEP 5
            Y AGGREGATE "count"
    )
    """

    chart_dict_truth = {
        "$schema": "https://vega.github.io/schema/vega-lite/v2.0.json",
        "datasets": {
            "bigfoot": "data/bigfoot_sightings.csv"
        },
        "vconcat": [{
            "hconcat": [
                {
                    "data": {"name": "bigfoot"},
                    "mark": "bar",
                    "encoding": {
                        "x": {"field": "classification", "type": "nominal"},
                        "y": {"aggregate": "count", "type": "quantitative"}
                    }
                }, {
                    "data": {"name": "bigfoot"},
                    "mark": "bar",
                    "encoding": {
                        "x": {"field": "temperature_mid", "bin": {"step": 5}},
                        "y": {"aggregate": "count", "type": "quantitative"}
                    }
                }
            ]
        }]
    }

    chart_dict_answer = parse_svl(chart_string)

    assert chart_dict_truth == chart_dict_answer


def test_histogram_step():
    assert True  # TODO: WOO TDD.


def test_histogram_nostep():
    assert True  # TODO: WOO TDD.
