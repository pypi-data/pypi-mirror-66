"""
Base module for completion functions
It includes all function used for autocomplete click options and arguments
"""
from click.core import Context
from jira.client import ResultList

from moic.cli import ISSUERS, global_settings, settings
from moic.cli.utils import get_project_boards
from moic.jira import JiraMoicInstance


def autocomplete_issuers(ctx: Context, args: list, incomplete: str) -> list:
    """
    Get autocompleted issuers list

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        incomplete (str): String input to autocomplete

    Returns:
       list: List available issuers autocompleted
    """
    return [issuer for issuer in ISSUERS if issuer.startswith(incomplete)]


def autocomplete_boards(ctx: Context, args: list, incomplete: str) -> list:
    """
    Get autocompleted boards list

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        incomplete (str): String input to autocomplete

    Returns:
       list: List available boards name
    """
    try:
        jira = JiraMoicInstance()
        boards = jira.session.boards(type="scrum")
        return [board.name for board in boards if board.name.lower().startswith(incomplete.lower())]
    except Exception:
        return []


def autocomplete_sprints(ctx: Context, args: list, incomplete: str) -> list:
    """
    Get autocompleted sprints list

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        incomplete (str): String input to autocomplete

    Returns:
       list: List available sprints name
    """
    try:
        jira = JiraMoicInstance()
        project = ctx.params["project"] if ctx.params["project"] else settings.get("default_project")
        if ctx.params["board"]:
            board = jira.session.boads(name=ctx.params["board"])
        else:
            board = get_project_boards(project)[0]
        sprints = jira.session.sprints(board.id)
        return [(sprint.id, sprint.name) for sprint in sprints]
    except Exception:
        return []


def autocomplete_contexts(ctx: Context, args: list, incomplete: str) -> list:
    """
    Get autocompleted contexts list from configuration

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        incomplete (str): String input to autocomplete

    Returns:
       list: List available issuersautocompleted
    """
    return [
        (context["name"], context["description"])
        for context in global_settings["contexts"]
        if context["name"].startswith(incomplete)
    ]


def autocomplete_users(ctx: Context, args: list, incomplete: str) -> ResultList:
    """
    Get Jira users list completion

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        incomplete (str): String input to autocomplete

    Returns:
        jira.client.ResultList: List of users corresponding to the incomplete input
    """
    try:
        jira = JiraMoicInstance()
        users = jira.session.search_users(incomplete)
        return [(user.name, user.displayName) for user in users]
    except Exception:
        return []


def autocomplete_priorities(ctx: Context, args: list, incomplete: str) -> list:
    """
    Get Jira priorities name list completion

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        incomplete (str): String input to autocomplete

    Returns:
        list: List of priorities name corresponding to the incomplete input
    """
    try:
        jira = JiraMoicInstance()
        return [priority.name for priority in jira.session.priorities() if incomplete in priority.name]
    except Exception:
        return []


def autocomplete_transitions(ctx: Context, args: list, incomplete: str) -> list:
    """
    Get Jira translations available for an issue

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        incomplete (str): String input to autocomplete

    Returns:
        list: List of translation names corresponding to the incomplete input
    """
    try:
        jira = JiraMoicInstance()
        issue_key = args[-1]
        issue = jira.session.issue(issue_key)
        transitions = jira.session.transitions(issue)
        return [(t["name"], t["to"]["description"]) for t in transitions if t["name"].startswith(incomplete)]
    except Exception:
        return []


def autocomplete_projects(ctx: Context, args: list, incomplete: str) -> list:
    """
    Get Jira projects list completion

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        incomplete (str): String input to autocomplete

    Returns:
        list: List of project names corresponding to the incomplete input
    """
    try:
        jira = JiraMoicInstance()
        projects = jira.session.projects()
        return [(p.key, p.name) for p in projects if incomplete.lower() in p.key.lower()]
    except Exception:
        return []


def autocomplete_issue_types(ctx: Context, args: list, incomplete: str) -> list:
    """
    Get Jira issue types list completion

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        incomplete (str): String input to autocomplete

    Returns:
        list: List of issue types names corresponding to the incomplete input
    """
    try:
        jira = JiraMoicInstance()
        issue_types = jira.session.issue_types()
        return [(i.name, i.description) for i in issue_types if incomplete.lower() in i.name.lower()]
    except Exception:
        return []
