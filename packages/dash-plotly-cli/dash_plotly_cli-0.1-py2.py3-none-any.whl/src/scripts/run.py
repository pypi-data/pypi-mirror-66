import os
import click
import subprocess


@click.command()
def run():
    """
    Run dash apps
    """

    from src import app

    app.run_server(debug=True)
