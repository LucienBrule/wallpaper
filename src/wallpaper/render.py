import os
import cairosvg
import click
import random

def generate_static_svg(output_svg_path: str, width=5120, height=1440, density_factor=2):
    """
    Generate a static squircle SVG with precomputed positions.
    """
    squircle_size = 25 / density_factor  # Smaller squircles
    margin_ratio = 4  # Controls margin between squircles
    grid_size = squircle_size * margin_ratio
    taskbar_height = 25  # Taskbar height
    margin_from_taskbar = 5  # Extra spacing below taskbar

    # Correct margin logic for both sides
    side_offset = (width % grid_size) / 2
    margin_top = taskbar_height + margin_from_taskbar if squircle_size > taskbar_height else taskbar_height

    dark_colors = ["#585b70", "#45475a", "#313244"]
    bright_colors = ["#f5c2e7", "#cba6f7", "#f38ba8", "#eba0ac", "#fab387", "#f9e2af",
                     "#a6e3a1", "#94e2d5", "#89dceb", "#74c7ec", "#89b4fa", "#b4befe", "#cdd6f4"]

    color_ratio = 0.75  # % of dark colors vs bright colors

    svg_content = f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg" style="background-color:#0a0a0e;">
      <defs>
        <rect id="squircle" width="{squircle_size}" height="{squircle_size}" rx="3" ry="3"/>
        <filter id="noise" x="-20%" y="-20%" width="140%" height="140%">
          <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" result="noise"/>
          <feColorMatrix type="matrix" values="
            1 0 0 0 0
            0 1 0 0 0
            0 0 1 0 0
            0 0 0 0.4 0
          " result="noised"/>
        </filter>
      </defs>
      <g filter="url(#noise)">
    '''

    # Generate static squircles with balanced left and right alignment
    for x in range(int(side_offset), width - int(side_offset), int(grid_size / density_factor)):
        for y in range(margin_top, height, int(grid_size / density_factor)):
            color = random.choice(dark_colors) if random.random() < color_ratio else random.choice(bright_colors)
            svg_content += f'<use href="#squircle" x="{x}" y="{y}" fill="{color}"/>\n'

    svg_content += "</g>\n</svg>"

    with open(output_svg_path, "w", encoding="utf-8") as svg_file:
        svg_file.write(svg_content)

    return output_svg_path

def render_svg_to_png(svg_path: str, output_dir: str):
    """
    Convert an SVG file to PNG and save it in the output directory.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_path = os.path.join(output_dir, os.path.basename(svg_path).replace(".svg", ".png"))

    try:
        with open(svg_path, "r", encoding="utf-8") as svg_file:
            svg_content = svg_file.read()
        cairosvg.svg2png(bytestring=svg_content.encode(), write_to=output_path)
        click.echo(f"Rendered PNG saved to: {output_path}")
    except Exception as e:
        click.echo(f"Error rendering SVG: {e}", err=True)

    return output_path