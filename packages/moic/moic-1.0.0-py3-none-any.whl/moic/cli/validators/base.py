"""
Module for base Moic validator functions
"""
import click
from click.core import Context

from moic.jira import JiraMoicInstance


def validate_issue_key(ctx: Context, param: list, value: str) -> str:
    """
    Validate a given issue key to check if it exists in Jira

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        value (str): String input to validate

    Returns:
        str: Retrive the key if it's validated
    """
    try:
        if value:
            jira = JiraMoicInstance()
            issue = jira.session.issue(value)
            return issue.key
        else:
            return ""
    except Exception:
        raise click.BadParameter("Please provide a valide issue key")


def validate_project_key(ctx: Context, param: list, value: str) -> str:
    """
    Validate a given project key to check if it exists in Jira

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        value (str): String input to validate

    Returns:
        str: Retrive the key if it's validated
    """
    try:
        jira = JiraMoicInstance()
        project = jira.session.project(value)
        return project.key
    except Exception:
        raise click.BadParameter("Please provide a valide project key")


def validate_issue_type(ctx: Context, param: list, value: str) -> str:
    """
    Validate a given issue type name to check if it exists in Jira

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        value (str): String input to validate

    Returns:
        str: Retrive the name if it's validated
    """
    try:
        jira = JiraMoicInstance()
        issue_type = jira.session.issue_type(value)
        return issue_type.name
    except Exception:
        raise click.BadParameter("Please provide a valide issue type name")


def validate_priority(ctx, param, value):
    """
    Validate a given priority name to check if it exists in Jira

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        value (str): String input to validate

    Returns:
        str: Retrive the priority name if it's validated
    """
    try:
        jira = JiraMoicInstance()
        priority = [priority for priority in jira.session.priorities() if priority.name == value][0]
        return priority.name
    except Exception:
        raise click.BadParameter("Please provide a valide priority")


def validate_user(ctx, param, value):
    """
    Validate a given user name to check if it exists in Jira

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        value (str): String input to validate

    Returns:
        str: Retrive the user name if it's validated
    """
    try:
        if value:
            jira = JiraMoicInstance()
            user = jira.session.user(value)
            return user.name
        else:
            return ""
    except Exception:
        raise click.BadParameter("Please provide a valide user name")
