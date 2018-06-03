import click
import json
import webbrowser
import os
import csv

import svl

from jinja2 import Environment, PackageLoader, select_autoescape
from toolz import get, valmap, assoc, thread_first, dissoc
from math import floor

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


def inject_width(view, width):
    if 'vconcat' in view:
        # For columns, inject the current width to all sub-views.
        return assoc(view, "vconcat", [
            inject_width(v, width) for v in view["vconcat"]
        ])
    elif 'hconcat' in view:
        # For rows, inject (1/n) * current width to all sub-views.
        return assoc(view, "hconcat", [
            inject_width(v, floor(
                (width/len(view["hconcat"]))*0.95
                ))
            for v in view["hconcat"]
        ])
    else:
        # Otherwise just inject the width as a field.
        return assoc(view, "width", width)

@click.command()
@click.argument("svl_source", type=click.File('r'))
@click.option(
    "--output-file", "-o",
    type=click.File('w'),
    default="visualization.html"
)
@click.option(
    "--debug",
    is_flag=True
)
@click.option(
    "--no-browser",
    is_flag=True
)
@click.option(
    "--no-datasets",
    is_flag=True
)
def cli(svl_source, output_file, debug, no_browser, no_datasets):
    svl_string = svl_source.read()

    if debug:
        print(svl.parse_svl(svl_string, debug=True).pretty())
    else:
        parsed_spec = svl.parse_svl(svl_string)

        # Add data + dimension to the vega lite spec.
        vega_lite = thread_first(
            parsed_spec,
            inject_dataset,
            (inject_width, 1200)
        )

        output_file.write(
            template.render(vis=vega_lite)
        )

        if no_browser:
            if no_datasets:
                vega_lite = dissoc(vega_lite, "datasets")
            print(json.dumps(vega_lite))
        else:
            output_path = os.path.realpath(output_file.name)
            webbrowser.open("file://{}".format(output_path), new=2)
        