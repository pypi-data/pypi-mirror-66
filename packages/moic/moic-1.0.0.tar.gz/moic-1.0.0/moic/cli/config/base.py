"""
Module for base Moic configuration commands
"""
import click

from moic.cli import CONF_DIR, ISSUERS, CustomSettings, MoicInstance, console, global_settings, settings
from moic.cli.completion import autocomplete_contexts, autocomplete_issuers
from moic.jira import JiraMoicInstance


@click.group()
def context():
    """
    Command to list, add and delete configuration contexts
    """
    if not global_settings.get("contexts"):
        MoicInstance()
    pass


@context.command()
def list():
    """
    List existing contexts
    """
    contexts = global_settings.get("contexts")
    if not contexts:
        console.print("[yellow]No context defined yet[/yellow]")
        console.print("[grey]> Please run '[bold]moic context add[/bold]' to setup configuration[/grey]")
        console.line()
        exit(0)
    for ctx in contexts:
        context_color = "green" if ctx.get("name") == global_settings.get("current_context") else "blue"
        prefix = "✓" if ctx.get("name") == global_settings.get("current_context") else "•"
        console.print(
            f"[{context_color}]{prefix} {ctx.get('name').ljust(20)}[/]: [grey70]{ctx.get('description')}[/grey70]"
        )


@context.command()
@click.argument("issuer", type=click.STRING, autocompletion=autocomplete_issuers)
@click.option("--name", type=click.STRING, default=None, help="The context name")
@click.option("--description", type=click.STRING, default=None, help="The context description")
def add(issuer, name, description):
    """
    Add a new context in the configuration
    """
    if issuer not in ISSUERS:
        console.print(f"[yellow]unsupported issuer {issuer}[/]")

    name = click.prompt("name") if not name else name
    if not name:
        name = f"default-{issuer}"
    if not description:
        description = click.prompt("description", default=f"{issuer} default context")

    if name in [ctx["name"] for ctx in global_settings.get("contexts")]:
        console.print(f"[red]Context '{name}' already definded[/red]")
        exit(1)

    if issuer == "jira":
        jmi = JiraMoicInstance()
        context = jmi.add_context(force=True)
        context["name"] = name
        context["description"] = description
        config = {"default": {"contexts": [context]}}
        jmi.update_config(config)
        # Reload configuration
        CustomSettings.reload()
        jmi.set_current_context(name)
        CustomSettings.reload()
        set_agile = click.confirm("Would you like to configure Jira Agile")
        if set_agile:
            JiraMoicInstance().configure_agile(project=context["default_project"], force=True)
        console.print(f"[grey70] > Configuration stored in {CONF_DIR}/config.yaml[/grey70]")


@context.command()
@click.argument("context_name", type=click.STRING, autocompletion=autocomplete_contexts)
def set(context_name):
    """
    Set the current context to use
    """
    MoicInstance().set_current_context(context_name)
    console.print(f"Context swithed to [green]{context_name}[/green]")


@context.command()
@click.argument("context_name", type=click.STRING, autocompletion=autocomplete_contexts)
def delete(context_name):
    """
    Delete the given context
    """
    MoicInstance().delete_context(context_name)
    console.print(f"Context [red]{context_name}[/red] deleted")
