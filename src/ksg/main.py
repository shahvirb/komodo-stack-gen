from jinja2 import Environment, FileSystemLoader, Template
from pathlib import Path
import click
import os
import functools


def get_template(filename: str) -> Template:
    template_dir = Path(__file__).parent.parent.parent / "templates"
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(filename)
    return template


def cli_options(f):
    """Decorator to add common options to CLI commands"""

    @click.argument(
        "directory",
        type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    )
    @click.option(
        "--template", default="single.toml", help="Template file to use for rendering"
    )
    @click.option(
        "--server-name",
        default=None,
        help="Override server name (defaults to HOSTNAME or COMPUTERNAME env var)",
    )
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)

    return wrapper


@click.group()
def cli():
    """Komodo Stack Generator CLI"""
    pass


@cli.command()
@cli_options
def stacks(directory, template, server_name):
    """
    Generate all the stack configurations from a parent directory.

    DIRECTORY: parent directory containing all the stack-* dirs
    """
    # Resolve directory to absolute path
    absolute_dir = directory.resolve()

    # Get all level 1 child directories that start with "stack-"
    for child_dir in absolute_dir.iterdir():
        if child_dir.is_dir() and child_dir.name.startswith("stack-"):
            single.callback(child_dir, template, server_name)


@cli.command()
@cli_options
def single(directory, template, server_name):
    """
    Generate a single stack configuration from a directory.

    DIRECTORY: directory containing the single stack files
    """
    dir_path = Path(directory).resolve()
    stack_name = dir_path.name

    # Use provided server_name or fall back to environment variables
    if server_name is None:
        server_name = os.environ.get("HOSTNAME") or os.environ.get(
            "COMPUTERNAME", "localhost"
        )

    # If any files with .tpl extension exist, set op_unpack to True
    op_unpack = bool(list(dir_path.rglob("*.tpl")))

    # Check if .git directory exists
    has_git = bool(list(dir_path.glob(".git")))

    template = get_template(template)
    rendered = template.render(
        stack_name=stack_name,
        server_name=server_name,
        op_unpack=op_unpack,
        has_git=has_git,
    )

    click.echo(rendered)


if __name__ == "__main__":
    cli()
