import click
import svl
import json


@click.command()
@click.argument("svl_source", type=click.File('r'))
@click.option("--debug", is_flag=True)
def cli(svl_source, debug):

    svl_string = svl_source.read()

    if debug:
        print(svl.parse_svl(svl_string, debug=True).pretty())
    else:
        print(json.dumps(svl.parse_svl(svl_string), indent=4, sort_keys=True))
