"""
Moic cli definition base module
"""
import click

from moic.cli import MoicInstance, global_settings, settings
from moic.cli.config import context
from moic.cli.fun import rabbit
from moic.cli.issue import issue
from moic.cli.resources import list
from moic.cli.sprint import sprint
from moic.cli.template import template
from moic.cli.utils import check_instance_is_up, version


@click.group()
def cli():
    """
    Main MOIC cli command group
    """
    if settings.get("type") == "jira":
        check_instance_is_up()


# Register sub command
cli.add_command(template)
cli.add_command(context)
cli.add_command(issue)
cli.add_command(list)
cli.add_command(sprint)
cli.add_command(rabbit)
cli.add_command(version)


def run():
    """
    Run the cli application
    """
    cli()


if __name__ == "__main__":
    """
    Main method of the module
    """
    cli()
