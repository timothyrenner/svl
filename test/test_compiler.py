import pytest
import os

from jinja2 import Environment, BaseLoader

from svl.compiler.compiler import _extract_additional_datasets, svl
from svl.compiler.errors import (
    SvlSyntaxError,
    SvlMissingFileError,
    SvlPlotError,
    SvlDataLoadError,
    SvlDataProcessingError,
)


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
JINJA_ENV = Environment(loader=BaseLoader)


@pytest.fixture
def svl_source():
    """ Self cleaning fixture for rendering an SVL script template into a file
        to be called from a subprocess. Returns a factory that produces
        rendered template locations and also renders the template.
    """
    svl_script_template = JINJA_ENV.from_string(
        """
    DATASETS
        bigfoot "{{ test_dir }}/test_datasets/bigfoot_sightings.csv"

    HISTOGRAM bigfoot
        X temperature_mid BINS 25
    """
    )

    return svl_script_template.render(test_dir=CURRENT_DIR)


def test_extract_additional_datasets():
    """ Tests that the _extract_additional_datasets function returns the
        correct value.
    """
    datasets = ["bigfoot=datasets/bigfoot.csv", "dogman=datasets/dogman.csv"]
    truth = {
        "bigfoot": "datasets/bigfoot.csv",
        "dogman": "datasets/dogman.csv",
    }
    answer = _extract_additional_datasets(datasets)
    assert truth == answer


def test_svl(svl_source):
    """ Tests that the svl function works when the script is correct.
    """
    svl(svl_source)


def test_svl_datasets(svl_source):
    """ Tests that the svl function works when additional datasets are
        specified.
    """
    svl(
        svl_source,
        datasets=[
            "bigfoot={}/test_datasets/bigfoot_sightings.csv".format(
                CURRENT_DIR
            )
        ],
    )


def test_svl_debug(svl_source):
    """ Tests that the svl function works when the debug option is specified.
    """
    answer = svl(svl_source, debug=True)
    assert "<" not in answer


def test_svl_offline_js(svl_source):
    """ Tests that the svl function works when the offline_js option is
        specified.
    """
    svl(svl_source, offline_js=True)


def test_svl_dataset_error(svl_source):
    """ Tests that the svl function raises a ValueError when the additional
        datasets are incorrectly specified.
    """
    with pytest.raises(ValueError, match="name=path"):
        svl(
            svl_source,
            datasets=[
                "bigfoot:{}/test_datasets/bigfoot_sightings.csv".format(
                    CURRENT_DIR
                )
            ],
        )


def test_svl_syntax_error(svl_source):
    """ Tests that the svl function raises a SvlSyntaxError when there is a
        syntax error in the source.
    """
    svl_source = """{}
    LINE bigfoot X X date BY YEAR Y report_number COUNT
    """.format(
        svl_source
    )
    with pytest.raises(SvlSyntaxError, match="Syntax error"):
        svl(svl_source)


def test_svl_missing_file_error(svl_source):
    """ Tests that the svl function raises a SvlMissingFileError when there is
        a missing file.
    """
    with pytest.raises(SvlMissingFileError, match="File"):
        svl(svl_source, datasets=["ufos={}/test_datasets/ufo_sightings.csv"])


def test_svl_plot_error(svl_source):
    """ Tests that the svl function raises a SvlPlotError when there is an
        error in a plot specification.
    """
    svl_source = """{}
    LINE bigfoot X date BY YEAR TITLE "Annual Bigfoot Sightings"
    """.format(
        svl_source
    )
    with pytest.raises(SvlPlotError, match="Plot error:"):
        svl(svl_source)


def test_svl_data_load_error():
    """ Tests that the svl function raises a SvlDataLoadError when there's an
        incorrectly specified SQL dataset.
    """
    svl_source = """
    DATASETS
        bigfoot "{}/test_datasets/bigfoot_sightings.csv"
        bigfoot_failure SQL "SELECT date FROM bigfoots"

    HISTOGRAM bigfoot
        X temperature_mid BINS 25
    """.format(
        CURRENT_DIR
    )

    with pytest.raises(SvlDataLoadError, match="Error loading data"):
        svl(svl_source)


def test_svl_data_processing_error():
    """ Tests that the svl function raises a SvlDataProcessingError when there
        is an incorrectly specified custom SQL statement in the plot.
    """
    svl_source = """
    DATASETS
        bigfoot "{}/test_datasets/bigfoot_sightings.csv"
    LINE bigfoot
        X date by year label "year"
        Y date count label "number of sightings"
        SPLIT BY classification
        FILTER "daet > 1990-01-01"
    """.format(
        CURRENT_DIR
    )
    with pytest.raises(
        SvlDataProcessingError, match="Error processing plot data"
    ):
        svl(svl_source)


def test_svl_not_implemented_error(svl_source):
    """ Tests that the svl function raises a NotImplementedError when the
        selected backend has not been implemented.
    """
    with pytest.raises(NotImplementedError, match="Unable to use"):
        svl(svl_source, backend="vega")
