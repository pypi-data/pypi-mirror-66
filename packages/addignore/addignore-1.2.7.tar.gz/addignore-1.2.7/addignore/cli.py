import os
import click
import requests
from .utils import prepare_path, save_list_and_cache, write_to, get_result
from .help import BRANDING

prepare_path()


# @click.group()
@click.command()
@click.argument('ignore', required=False)
@click.version_option(message=BRANDING)
@click.option('-a', '--listall', help='Get all available terms', default=False, is_flag=True)
# @click.pass_context
def cli(listall, ignore):
    """ AzatAI Addignore Automation tool. Searches for a proper .gitignore file for your project and adds to the
        local .gitignore file.
        Search for operating systems, IDEs, languages and other environmental terms. Use ',' to separate multiple items.
        Usage: addignore python """
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    # ctx.ensure_object(dict)
    prepare_path()
    if ignore:
        here = os.getcwd()
        file_path = os.path.join(here, '.gitignore')
        write_to(get_result(ignore), file_path, mode='file')
    elif not ignore and listall:
        click.secho(save_list_and_cache())
    else:
        with click.get_current_context() as context:
            click.echo(context.get_help())


# @cli.command()
# @click.pass_context
# def list(ctx):
#     """Prints all the available results."""
#     click.secho('Hello')


if __name__ == '__main__':
    cli()
