import click
import svl
import webbrowser
import os
import sys
import sqlite3

from toolz import valfilter

from svl.layout import tree_to_grid
from svl.plotly import plotly_template, plotly_template_vars
from svl.sqlite import create_datasets, get_svl_data
from svl.plot_validators import validate_plot


def _extract_cli_datasets(datasets):
    return dict(map(lambda x: x.split("="), datasets))


@click.command()
@click.argument("svl_source", type=click.File('r'))
@click.option("--debug", is_flag=True)
@click.option(
    '--backend', '-b',
    type=click.Choice(['plotly', 'vega']),
    default='plotly'
)
@click.option(
    "--output-file", "-o",
    type=click.File("w"),
    default="visualization.html"
)
@click.option("--dataset", "-d", multiple=True)
@click.option("--no-browser", is_flag=True)
def cli(svl_source, debug, backend, output_file, dataset, no_browser):

    svl_string = svl_source.read()
    if debug:
        print(svl.parse_svl(svl_string, debug=True).pretty())
        return

    # Validate that the dataset args are in the correct form.
    for cds in dataset:
        if len(cds.split("=")) != 2:
            print("--dataset arg {} needs to be name=path".format(cds))
            sys.exit(1)

    # Extract the datasets from the CLI.
    cli_datasets = _extract_cli_datasets(dataset)

    try:
        svl_spec = svl.parse_svl(svl_string, **cli_datasets)
    except SyntaxError as e:
        print("Syntax error:")
        print("{}".format(e))
        sys.exit(1)

    # Validate that all of the files in the svl_spec["datasets"] exist.
    for _, dataset in svl_spec["datasets"].items():
        if ("file" in dataset) and (not os.path.exists(dataset["file"])):
            print("Dataset error: {} does not exist.".format(dataset["file"]))
            sys.exit(1)

    # The datasets must contain at least one file.
    if len(list(valfilter(lambda x: "file" in x, svl_spec["datasets"]))) == 0:
        print("Datasets needs at least one file.")
        sys.exit(1)

    svl_plots = [plot for plot in tree_to_grid(svl_spec)]

    # Validate that each plot points to a dataset.
    for plot in svl_plots:
        if plot["data"] not in svl_spec["datasets"]:
            existing_datasets = ", ".join(list(svl_spec["datasets"].keys()))
            print("Dataset {} is not in provided datasets {}.".format(
                plot["data"],
                existing_datasets
            ))
            sys.exit(1)

    # Create a connection to the sqlite database (eventually this will be
    # abstracted a little better but for now sqlite's all we've got).
    try:
        sqlite_conn = create_datasets(svl_spec["datasets"])
    except sqlite3.DatabaseError as e:
        print("Error loading data: {}.".format(e))
        sys.exit(1)

    for plot in svl_plots:
        ok, msg = validate_plot(plot)
        # TODO it would be nice to identify which plot failed.
        if not ok:
            print("Plot error:")
            print(msg)
            sys.exit(1)

    try:
        svl_plot_data = [get_svl_data(plot, sqlite_conn) for plot in svl_plots]
    except sqlite3.DatabaseError as e:
        print("Error processing plot data: {}.".format(e))
        sys.exit(1)

    # For now, plotly is the only choice.
    if backend == "plotly":
        template_vars = plotly_template_vars(
            svl_plots,
            svl_plot_data
        )
        template = plotly_template()

    else:
        print("Unable to use backend {} yet.".format(backend))
        sys.exit(1)

    output_file.write(template.render(**template_vars))

    if not no_browser:
        webbrowser.open(
            "file://{}".format(
                os.path.realpath(output_file.name)
            ),
            new=2
        )
