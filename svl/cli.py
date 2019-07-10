import click
import webbrowser
import os
import sys

from svl import svl
from svl.compiler.errors import (
    SvlSyntaxError,
    SvlMissingFileError,
    SvlMissingDatasetError,
    SvlDataLoadError,
    SvlPlotError,
    SvlDataProcessingError,
)


def _extract_cli_datasets(datasets):
    return dict(map(lambda x: x.split("="), datasets))


@click.command()
@click.argument("svl_source", type=click.File("r"))
@click.option("--debug", is_flag=True)
@click.option(
    "--backend", "-b", type=click.Choice(["plotly", "vega"]), default="plotly"
)
@click.option(
    "--output-file", "-o", type=click.File("w"), default="visualization.html"
)
@click.option("--dataset", "-d", multiple=True)
@click.option("--no-browser", is_flag=True)
@click.option("--offline-js", is_flag=True)
def cli(
    svl_source, debug, backend, output_file, dataset, no_browser, offline_js
):

    svl_source = svl_source.read()

    try:
        rendered_plots = svl(
            svl_source,
            backend=backend,
            datasets=dataset,
            offline_js=offline_js,
            debug=debug,
        )
    except ValueError as e:
        print("Dataset specification error:")
        print(e)
        sys.exit(1)
    except SvlSyntaxError as e:
        print("Syntax error:")
        print(e)
        sys.exit(1)
    except SvlMissingFileError as e:
        print("Missing file error:")
        print(e)
        sys.exit(1)
    except SvlMissingDatasetError as e:
        print("Missing dataset error:")
        print(e)
        sys.exit(1)
    except SvlPlotError as e:
        print("Plot error:")
        print(e)
        sys.exit(1)
    except SvlDataLoadError as e:
        print("Data load error:")
        print(e)
        sys.exit(1)
    except SvlDataProcessingError as e:
        print("Data processing error:")
        print(e)
        sys.exit(1)
    except NotImplementedError as e:
        print("Not implemented error:")
        print(e)
        sys.exit(1)

    output_file.write(rendered_plots)

    if not no_browser:
        webbrowser.open(
            "file://{}".format(os.path.realpath(output_file.name)), new=2
        )
