import os
import click
import subprocess

from cookiecutter.main import cookiecutter

# for creating new components from react
DASH_COMPONENT_BOILERPLATE_URL = "https://github.com/plotly/dash-component-boilerplate.git"

TEMPLATES = {
    'hello-dash': 'C:/Users/adkin/Code Projects/dash-cli/.cookiecutters/dash_cookiecutter/',
    'sql-extractor': 'TBD'
}


@click.group()
def create():
    """
    Create apps and add components
    """
    pass


@click.command()
@click.option("--version", '-v', default="1.11.0", help="The version of dash you'd like to use")
@click.option("--replace", is_flag=True, help="overwrite project w/ same name")
@click.option("--output", '-o', default='.', help="specify where the output should go")
@click.option("--no-venv", is_flag=True, help="disables virtual env creation")
@click.option("--venv-name", default='venv', help="name of the virtual env")
@click.option("--python", default='python', help="target interpreter for which to create a virtual")
@click.option("--proxy", default=None, help="target interpreter for which to create a virtual")
@click.option("--template", '-t', type=click.Choice(TEMPLATES), show_choices=True, prompt=True, help="selects a template to use")
@click.argument("name")
def new(name, version, replace, output, venv_name, python, proxy, no_venv, template):
    """
    creates the layout for a dash app
    """

    click.echo(f'Creating {name} with dash=={version}\n')

    cookiecutter(
        template=TEMPLATES[template],
        extra_context={'project_slug': name, 'dash_version': version},
        no_input=True,
        output_dir=output,
        overwrite_if_exists=replace
    )

    if no_venv:
        return

    venv_command = f'virtualenv --python={python} {os.path.join(name, venv_name)}'
    sp = subprocess.run(venv_command)

    click.echo(sp.stdout)

    scripts_folder = 'Scripts' if os.name == 'nt' else 'bin'
    pip_script = os.path.join('.', name, venv_name, scripts_folder, 'pip')
    pip_command = f'{pip_script} install {"--proxy="+proxy if proxy else ""} -r {os.path.join(".", name, "requirements.txt")}'

    click.echo(f'installing dependencies\n')

    sp = subprocess.run(pip_command)
    click.echo(sp.stdout)

    click.echo('to start your app, use \n')
    click.echo(f'$ cd {name}')
    activate = os.path.join(".", venv_name, scripts_folder, "activate")
    windows_cmd = f'$ {activate}'
    linux_cmd = f'$ source {activate}'
    click.echo(windows_cmd if os.name == 'nt' else linux_cmd)
    click.echo('$ dash run\n')


@click.command()
@click.option("--interactive/--static", default=True, help="This will skip generating a callbacks template")
@click.argument("name")
def component(name, interactive):
    """
    adds a component to your dash app
    """
    click.echo(f'Creating componet {name} with callbacks={interactive}')
    raise NotImplementedError()
    cookiecutter(template=DASH_COMPONENT_BOILERPLATE_URL)


@click.command()
@click.argument("name")
def page(name):
    """
    adds another route to your app
    """
    click.echo(f'Creating page {name}')
    raise NotImplementedError()


create.add_command(new)
create.add_command(component)
create.add_command(page)
