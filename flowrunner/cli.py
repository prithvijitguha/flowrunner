"""Module for cli commands"""
import click

@click.command()
@click.option('--validate', help='Validate Flow')
def validate_flow(flow):
    """Simple program that greets NAME for a total of COUNT times."""
    click.secho("Hello World")

if __name__ == '__main__':
    validate_flow()