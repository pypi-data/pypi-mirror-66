"""
Module for base Moic resources commands
"""
import click

from moic.cli import COLOR_MAP, console, global_settings
from moic.jira import JiraMoicInstance


# List Commands
# TODO: Add autocomplete on all commands
@click.group()
def list():
    """List projects, issue_types, priorities, status"""
    if not global_settings.get("current_context"):
        console.print("[yellow]No context defined yet[/yellow]")
        console.print("[grey]> Please run '[bold]moic context add[/bold]' to setup configuration[/grey]")
        console.line()
        exit(0)


@list.command()
def projects():
    """List Jira Projects"""
    jira = JiraMoicInstance()
    projects = jira.session.projects()
    for p in projects:
        console.print(
            f"[grey70]{p.name.ljust(20)}[/grey70] : [magenta]{p.key}[/magenta]", highlight=False,
        )


@list.command()
def issue_type():
    """List Jira Issue Type"""
    jira = JiraMoicInstance()
    issue_types = jira.session.issue_types()
    for i in issue_types:
        console.print(
            f"[grey70]{i.name.ljust(20)}[/grey70] : [green]{i.description}[/green]", highlight=False,
        )


@list.command()
def priorities():
    """List Jira Priorities"""
    jira = JiraMoicInstance()
    priorities = jira.session.priorities()
    for p in priorities:
        console.print(
            f"[grey70]{p.name.ljust(10)}[/grey70] : [green]{p.description}[/green]", highlight=False,
        )


@list.command()
def status():
    """List Jira status"""
    jira = JiraMoicInstance()
    statuses = jira.session.statuses()
    for s in statuses:
        color_name = COLOR_MAP[s.raw["statusCategory"]["colorName"]]
        console.print(
            f"[{color_name}]{s.name.ljust(25)}[/{color_name}] : [grey70]{s.description}[/grey70]", highlight=False,
        )
