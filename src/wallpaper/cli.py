import click
from wallpaper.render import render_svg_to_png, generate_static_svg
import os
@click.group()
def cli():
    """Wallpaper rendering CLI."""
    pass

@click.command()
@click.option('--output', '-o', type=click.Path(), required=True, help="Directory to save the rendered output.")
@click.option('--width', default=5120, help="Width of the wallpaper.")
@click.option('--height', default=1440, help="Height of the wallpaper.")
@click.option('--density', default=2, help="Density factor for the grid.")
def render(output, width, height, density):
    """
    Generate a static SVG and render it as PNG.
    """
    svg_path = os.path.join(output, "wallpaper.svg")

    click.echo(f"Generating SVG at: {svg_path}...")
    generate_static_svg(svg_path, width, height, density)

    click.echo("Rendering PNG...")
    render_svg_to_png(svg_path, output)

cli.add_command(render)

if __name__ == "__main__":
    cli()