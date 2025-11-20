"""A set of utility functions used in various places in the project."""

from django.utils.html import format_html


def format_choices(choices: list[str], *, in_html: bool) -> str:
    """Format a list of choices, into html or not."""
    if in_html:
        html_template = f"<ul>{''.join([f'<li>{choice}</li>' for choice in choices])}</ul>"
        return format_html(html_template, choices=choices)
    return "".join([f"\n  • {c}" for c in choices])
