from pathlib import Path
import click
from jinja2 import Environment, FileSystemLoader


@click.group()
def cli():
    """Komodo Stack Generator CLI"""
    pass


@cli.command()
def stacks():
    """Render the stacks.toml template"""
    # Get the templates directory
    template_dir = Path(__file__).parent.parent.parent / "templates"
    
    # Set up Jinja environment
    env = Environment(loader=FileSystemLoader(template_dir))
    
    # Load and render the template
    template = env.get_template("stacks.toml")
    rendered = template.render()
    
    # Output to stdout
    click.echo(rendered)


if __name__ == "__main__":
    cli()
