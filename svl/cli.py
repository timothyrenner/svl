import click
import svl


@click.command()
@click.argument("svl_source", type=click.File('r'))
def cli(svl_source):

    svl_string = svl_source.read()

    print(svl.parse_svl(svl_string).pretty())
