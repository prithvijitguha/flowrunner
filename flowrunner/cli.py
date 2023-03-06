"""Module for cli commands"""
import click
import inspect



@click.command()
@click.argument("filepath")
def hello(filepath):
    click.echo(filepath)

if __name__=="__main__":
    hello()



