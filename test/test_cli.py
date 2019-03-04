import subprocess
import pytest
import os

from jinja2 import Environment, FileSystemLoader

from svl.cli import _extract_cli_datasets


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SVL_SCRIPT_TEMPLATE_DIR = os.path.join(CURRENT_DIR, "test_scripts")
JINJA_ENV = Environment(loader=FileSystemLoader(SVL_SCRIPT_TEMPLATE_DIR))


@pytest.fixture
def svl_script_template():
    """ Self cleaning fixture for rendering an SVL script template into a file
        to be called from a subprocess. Returns a factory that produces
        rendered template locations and also renders the template.
    """
    # Define the script path out of scope of the enclosing function so the
    # path can be removed after the test.
    # It's a list in case the enclosed function is called more than once.
    rendered_script_paths = []

    def _svl_script_template(script_template_name):
        # Load the jinja template for the SVL script.
        script_template = JINJA_ENV.get_template(script_template_name)
        # Inject the test directory.
        rendered_script = script_template.render(test_dir=CURRENT_DIR)
        # Create the path to write the temporary file to.
        rendered_script_path = os.path.join(
            SVL_SCRIPT_TEMPLATE_DIR,
            # Name it something _a little_ different.
            "_{}".format(script_template_name)
        )
        # Add it to the cleanup list.
        rendered_script_paths.append(rendered_script_path)

        # Write the rendered script.
        with open(rendered_script_path, 'w') as f:
            f.write(rendered_script + "\n")

        return rendered_script_path

    yield _svl_script_template

    # Clean up by killing the rendered template.
    for path in rendered_script_paths:
        os.remove(path)


@pytest.fixture
def output_path():
    """ Self cleaning fixture that produces the visualization output path.
    """
    # This is what gets written / deleted by each test.
    output_path = os.path.join(CURRENT_DIR, "test_viz.html")

    yield output_path

    os.remove(output_path)


def test_extract_cli_datasets():
    """ Tests that the _extract_cli_datasets function returns the correct
        value.
    """
    datasets = (
        "bigfoot=bigfoot_sightings.csv",
        "mothman=mothman_sightings.parquet"
    )

    truth = {
        "bigfoot": "bigfoot_sightings.csv",
        "mothman": "mothman_sightings.parquet"
    }

    answer = _extract_cli_datasets(datasets)

    assert truth == answer


def test_histogram_cli_debug(svl_script_template):
    """ Tests that the command line interface works correctly on the test
        dataset for histogram plots when debug is turned on.
    """
    # NOTE: Hard coded file paths aren't the greatest. It's fixable here but
    # not in the SVL script at this time.
    subprocess.run([
        "svl",
        # This function renders and grabs the file name of the rendered SVL
        # template for the test. Fixture cleans it up.
        svl_script_template("histogram.svl"),
        "--backend", "plotly",
        "--no-browser",
        "--debug"
    ], check=True)


def test_histogram_cli_plotly(svl_script_template, output_path):
    """ Tests that the command line interface works correctly on the test
        dataset for histogram plots.
    """
    # NOTE: Hard coded file paths aren't the greatest. It's fixable here but
    # not in the SVL script at this time.
    subprocess.run([
        "svl",
        svl_script_template("histogram.svl"),
        "--output-file", output_path,
        "--backend", "plotly",
        "--no-browser"
    ], check=True)


def test_histogram_cli_no_datasets(output_path):
    """ Tests that the command line interface works correctly on the test
        dataset for histogram plots when the test dataset is passed in via
        command line.
    """
    subprocess.run([
        "svl",
        # NOTE Don't need the template here because there are no templated
        # parts here.
        "{}/test_scripts/histogram_no_datasets.svl".format(CURRENT_DIR),
        "--dataset",
        "bigfoot={}/test_datasets/bigfoot_sightings.csv".format(CURRENT_DIR),
        "--output-file", output_path,
        "--backend", "plotly",
        "--no-browser"
    ], check=True)


def test_cli_syntax_error():
    """ Tests that the command line interface correctly exits 1 with the proper
        error message when there's a syntax error in the script.
    """
    completed = subprocess.run([
        "svl",
        "{}/test_scripts/invalid_syntax.svl".format(CURRENT_DIR),
        "--no-browser"
    ], check=False, stdout=subprocess.PIPE)

    assert completed.returncode == 1
    assert "Syntax error" in str(completed.stdout)


def test_cli_unsupported_backend(svl_script_template):
    """ Tests that the command line interface correctly exits 1 with the proper
        error message when the backend selected is unsupported.
    """
    completed = subprocess.run([
        "svl",
        svl_script_template("histogram.svl"),
        "--no-browser",
        "--backend", "vega"
    ], check=False, stdout=subprocess.PIPE)

    assert completed.returncode == 1
    assert "Unable to use backend vega yet." in str(completed.stdout)
