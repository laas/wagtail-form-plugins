from django.utils.html import format_html


def format_choices(choices: list, to_html: bool) -> str:
    """Build an html link poiting to a file url, or `-` if there is no url."""
    html_template = f"<ul>{''.join([f'<li>• {choice}</li>' for choice in choices])}</ul>"
    return format_html(html_template, choices=choices) if to_html else ", ".join(choices)
