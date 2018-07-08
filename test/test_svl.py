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
    """ Tests that the parse_svl function returns the correct dictionary when
        there's a histogram with a specified step.
    """
    chart_string = """
    DATASETS
        bigfoot "data/bigfoot_sightings.csv"
    BAR bigfoot
        X temperature_mid BIN STEP 5
        Y AGGREGATE "count"
    """

    chart_dict_truth = {
        "$schema": "https://vega.github.io/schema/vega-lite/v2.0.json",
        "datasets": {
            "bigfoot": "data/bigfoot_sightings.csv"
        },
        "vconcat": [{
            "data": {"name": "bigfoot"},
            "mark": "bar",
            "encoding": {
                "x": {"field": "temperature_mid", "bin": {"step": 5}},
                "y": {"aggregate": "count", "type": "quantitative"}
            }
        }]
    }

    chart_dict_answer = parse_svl(chart_string)

    assert chart_dict_truth == chart_dict_answer


def test_histogram_nostep():
    """ Tests that the parse_svl function returns the correct dictionary when
        there's a histogram with an unspecified bin width.
    """

    chart_string = """
    DATASETS
        bigfoot "data/bigfoot_sightings.csv"
    BAR bigfoot
        X temperature_mid BIN
        Y AGGREGATE "count"
    """

    chart_dict_truth = {
        "$schema": "https://vega.github.io/schema/vega-lite/v2.0.json",
        "datasets": {
            "bigfoot": "data/bigfoot_sightings.csv"
        },
        "vconcat": [{
            "data": {"name": "bigfoot"},
            "mark": "bar",
            "encoding": {
                "x": {"field": "temperature_mid", "bin": True},
                "y": {"aggregate": "count", "type": "quantitative"}
            }
        }]
    }

    chart_dict_answer = parse_svl(chart_string)

    assert chart_dict_truth == chart_dict_answer


def test_line_chart_temporal():
    """ Tests that the parse_svl function returns the correct value for
        line charts with temporal axes.
    """

    chart_string = """
    DATASETS
        bigfoot "data/bigfoot_sightings.csv"
    LINE bigfoot
        X date TYPE "temporal" TIMEUNIT "year"
        Y AGGREGATE "count"
    """

    chart_dict_truth = {
        "$schema": "https://vega.github.io/schema/vega-lite/v2.0.json",
        "datasets": {
            "bigfoot": "data/bigfoot_sightings.csv"
        },
        "vconcat": [{
            "data": {"name": "bigfoot"},
            "mark": "line",
            "encoding": {
                "x": {"field": "date", "type": "temporal", "timeUnit": "year"},
                "y": {"aggregate": "count", "type": "quantitative"}
            }
        }]
    }

    chart_dict_answer = parse_svl(chart_string)

    assert chart_dict_truth == chart_dict_answer
