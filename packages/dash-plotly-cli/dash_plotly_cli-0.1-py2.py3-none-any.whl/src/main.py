import click

from .scripts import *


@click.group()
def cli():
    pass


cli.add_command(create)
cli.add_command(run)
