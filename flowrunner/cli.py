"""Module for cli commands"""
import click
import inspect

@click.command()
@click.argument('filename')
def test(filename):
    """Print FILENAME."""
    click.echo(filename)


if __name__=="__main__":
    test()


