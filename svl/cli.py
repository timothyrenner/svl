import click
import svl
import csv
import webbrowser
import os

from toolz import groupby

from svl.layout import tree_to_grid
from svl.data import construct_data
from svl.plotly import plotly_template, plotly_template_vars


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
@click.option("--no-browser", is_flag=True)
def cli(svl_source, debug, backend, output_file, no_browser):

    svl_string = svl_source.read()

    if debug:
        print(svl.parse_svl(svl_string, debug=True).pretty())
        return

    svl_spec = svl.parse_svl(svl_string)

    # Produce a dictionary mapping the name of the dataset to an iterator
    # against that dataset.
    datasets = {
        dataset: csv.DictReader(
            open(svl_spec["datasets"][dataset], "r")
        )
        for dataset in svl_spec["datasets"].keys()
    }

    # Convert the SVL spec into a list of dictionaries, and group that list
    # by the "data" field. Produces a dictionary mapping the dataset to a
    # list of plots attributed to that dataset.
    svl_plots = groupby("data", tree_to_grid(svl_spec))

    # Need to read the datasets one at a time for each plot it applies to.
    # Produces a dictionary mapping the dataset to a list of SVL data specs
    # for each plot attributed to that dataset.
    svl_plot_datasets = {
        dataset: construct_data(svl_plots[dataset], datasets[dataset])
        for dataset in svl_plots.keys()
    }

    # Now flatten everything into two lists - one for the plots and the other
    # for the data. There's probably a more "functional" way to do this.
    svl_plots_flat = []
    svl_plot_data_flat = []
    for dataset in svl_plots.keys():

        assert len(svl_plots[dataset]) == len(svl_plot_datasets[dataset])

        for plot, data in zip(svl_plots[dataset], svl_plot_datasets[dataset]):
            svl_plots_flat.append(plot)
            svl_plot_data_flat.append(data)

    # For now, plotly is the only choice.
    if backend == "plotly":
        template_vars = plotly_template_vars(
            svl_plots_flat,
            svl_plot_data_flat
        )
        template = plotly_template()

    else:
        print("Unable to use backend {} yet.".format(backend))
        return

    output_file.write(template.render(**template_vars))

    if not no_browser:
        webbrowser.open(
            "file://{}".format(
                os.path.realpath(output_file.name)
            ),
            new=2
        )
