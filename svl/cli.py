import click
import json
import webbrowser
import os
import csv

import svl

from jinja2 import Environment, PackageLoader, select_autoescape

from toolz import get, valmap, assoc

# Set up the template for HTML output.
env = Environment(
    loader=PackageLoader("svl", "templates"),
    autoescape=select_autoescape(["html"])
)
template = env.get_template("index.html")


def slurp_csv(filename):
    # TODO: Add a fields argument to only pull out specified fields.
    with open(filename, 'r') as f:
        return [l for l in csv.DictReader(f)]


def inject_dataset(visualization_spec):
    # TODO: Extract the fields that only exist in the dataset.
    datasets = get("datasets", visualization_spec, {})
    return assoc(
        visualization_spec,
        "datasets",
        valmap(slurp_csv, datasets)
    )


@click.command()
@click.argument("svl_source", type=click.File('r'))
@click.option(
    "--output-file", "-o",
    type=click.File('w'),
    default="visualization.html"
)
def cli(svl_source, output_file):
    svl_string = svl_source.read()
    parsed_spec = svl.parse_svl(svl_string)

    # Replace the dataset file with the dataset values.
    vega_lite = inject_dataset(parsed_spec)

    # TODO: Walk the tree and determine what the widths should _actually_ be.

    output_file.write(
        template.render(vis=vega_lite)
    )

    output_path = os.path.realpath(output_file.name)
    webbrowser.open("file://{}".format(output_path), new=2)
    # print(svl.parse_svl(svl_string, debug=True).pretty())