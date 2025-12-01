"""
readme-forge: A powerful tool to generate beautiful and effective READMEs.

This module provides both CLI and TUI interfaces for generating README files.
"""

import click
import questionary
from jinja2 import Environment, FileSystemLoader
import os
import json
from typing import Dict, Any, Optional, List

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint

from .templates import (
    get_template_names,
    get_template_descriptions,
    render_template,
    get_section_names,
)
from .git_utils import detect_git_info, detect_project_type, get_suggested_context
from .badges import (
    generate_badges_from_preset,
    badges_to_markdown,
    get_presets,
    BADGE_PRESETS,
)
from .licenses import (
    get_license_names,
    generate_license_text,
    save_license_file,
    get_license_badge_name,
)

console = Console()

# Configuration file name
CONFIG_FILE = "readme-forge.json"


def print_banner():
    """Print the application banner."""
    banner = """
[bold blue]╦═╗╔═╗╔═╗╔╦╗╔╦╗╔═╗  ╔═╗╔═╗╦═╗╔═╗╔═╗[/bold blue]
[bold blue]╠╦╝║╣ ╠═╣ ║║║║║║╣   ╠╣ ║ ║╠╦╝║ ╦║╣ [/bold blue]
[bold blue]╩╚═╚═╝╩ ╩═╩╝╩ ╩╚═╝  ╚  ╚═╝╩╚═╚═╝╚═╝[/bold blue]
[dim]Generate beautiful READMEs with ease[/dim]
    """
    console.print(Panel(banner, border_style="blue"))


def display_git_info(git_info) -> None:
    """Display detected git information."""
    if not git_info.is_git_repo:
        console.print("[yellow]Not a git repository. Manual input required.[/yellow]")
        return

    table = Table(title="Detected Git Information", show_header=True)
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")

    if git_info.project_name:
        table.add_row("Project Name", git_info.project_name)
    if git_info.github_username:
        table.add_row("GitHub Username", git_info.github_username)
    if git_info.remote_url:
        table.add_row("Remote URL", git_info.remote_url)
    if git_info.default_branch:
        table.add_row("Default Branch", git_info.default_branch)
    if git_info.license_type:
        table.add_row("License", git_info.license_type)
    if git_info.languages:
        table.add_row("Languages", ", ".join(git_info.languages))
    if git_info.contributors:
        table.add_row("Contributors", ", ".join(git_info.contributors[:5]))

    console.print(table)


def display_templates() -> None:
    """Display available templates."""
    table = Table(title="Available Templates", show_header=True)
    table.add_column("Template", style="cyan")
    table.add_column("Description", style="white")

    for name, desc in get_template_descriptions().items():
        table.add_row(name, desc)

    console.print(table)


def collect_project_info(
    git_info=None,
    suggested_context: Dict = None
) -> Dict[str, Any]:
    """Collect project information interactively."""
    context = suggested_context or {}

    console.print("\n[bold]Project Information[/bold]")
    console.print("[dim]Press Enter to accept suggested values (shown in brackets)[/dim]\n")

    # Project name
    default_name = context.get("project_name", "")
    project_name = Prompt.ask(
        "Project name",
        default=default_name if default_name else None
    )
    context["project_name"] = project_name

    # Description
    default_desc = context.get("project_description", "")
    description = Prompt.ask(
        "Project description",
        default=default_desc if default_desc else None
    )
    context["project_description"] = description

    # GitHub username
    default_username = context.get("github_username", "")
    github_username = Prompt.ask(
        "GitHub username",
        default=default_username if default_username else None
    )
    context["github_username"] = github_username

    # Author info
    author_name = Prompt.ask("Author name", default=github_username)
    context["author_name"] = author_name

    author_email = Prompt.ask("Author email (optional)", default="")
    if author_email:
        context["author_email"] = author_email

    # License selection
    licenses = get_license_names() + ["None"]
    default_license = context.get("license", "MIT")

    license_choice = questionary.select(
        "Choose a license:",
        choices=licenses,
        default=default_license if default_license in licenses else "MIT"
    ).ask()
    context["license"] = license_choice

    return context


def collect_installation_info(context: Dict) -> Dict[str, Any]:
    """Collect installation and usage information."""
    console.print("\n[bold]Installation & Usage[/bold]\n")

    # Installation instructions
    default_install = f"pip install {context.get('project_name', 'package')}"
    installation = Prompt.ask(
        "Installation command",
        default=default_install
    )
    context["installation_instructions"] = installation

    # Usage instructions
    console.print("[dim]Enter usage instructions (press Enter twice to finish):[/dim]")
    usage = questionary.text(
        "Usage instructions:",
        multiline=True
    ).ask()
    context["usage_instructions"] = usage or f"{context.get('project_name', 'package')} --help"

    # Code language for syntax highlighting
    code_lang = questionary.select(
        "Primary code language:",
        choices=["python", "bash", "javascript", "typescript", "go", "rust", "java", "other"]
    ).ask()
    context["code_language"] = code_lang

    return context


def collect_features(context: Dict) -> Dict[str, Any]:
    """Collect project features."""
    console.print("\n[bold]Features[/bold]")
    console.print("[dim]Enter your project features (one per line, empty line to finish):[/dim]\n")

    features = []
    while True:
        feature = Prompt.ask("Feature (or Enter to finish)", default="")
        if not feature:
            break
        features.append(feature)

    if features:
        context["features"] = features

    return context


def select_template() -> str:
    """Let user select a template."""
    console.print("\n[bold]Template Selection[/bold]\n")
    display_templates()

    template_names = get_template_names()
    template = questionary.select(
        "Choose a template:",
        choices=template_names,
        default="standard"
    ).ask()

    return template


def select_badges(context: Dict) -> Dict[str, Any]:
    """Let user select badges."""
    console.print("\n[bold]Badge Selection[/bold]")

    presets = list(BADGE_PRESETS.keys())
    preset = questionary.select(
        "Choose a badge preset:",
        choices=["none"] + presets,
        default="github_standard"
    ).ask()

    if preset != "none":
        badges = generate_badges_from_preset(
            preset,
            username=context.get("github_username", ""),
            repo=context.get("project_name", ""),
            package=context.get("project_name", ""),
            license=get_license_badge_name(context.get("license", "MIT")),
        )
        context["badges"] = badges_to_markdown(badges)

    return context


def generate_readme(context: Dict, template_name: str, output_path: str = "README.md") -> str:
    """Generate the README file."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Generating README...", total=None)

        # Render the template
        rendered = render_template(template_name, context)

        # Write to file
        with open(output_path, "w") as f:
            f.write(rendered)

        progress.update(task, completed=True)

    return output_path


def preview_readme(content: str) -> None:
    """Show a preview of the generated README."""
    console.print("\n[bold]README Preview[/bold]\n")
    console.print(Panel(Markdown(content), border_style="green"))


def save_config(context: Dict, path: str = CONFIG_FILE) -> None:
    """Save configuration to file."""
    # Remove non-serializable items
    serializable = {k: v for k, v in context.items() if isinstance(v, (str, int, float, bool, list, dict))}

    with open(path, "w") as f:
        json.dump(serializable, f, indent=2)

    console.print(f"[green]Configuration saved to {path}[/green]")


def load_config(path: str = CONFIG_FILE) -> Optional[Dict]:
    """Load configuration from file."""
    if not os.path.exists(path):
        return None

    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        console.print(f"[yellow]Warning: Could not load config: {e}[/yellow]")
        return None


@click.group()
@click.version_option(version="0.2.0", prog_name="readme-forge")
def cli():
    """readme-forge: Generate beautiful READMEs with ease."""
    pass


@cli.command()
@click.option("--output", "-o", default="README.md", help="Output file path")
@click.option("--template", "-t", default=None, help="Template to use")
@click.option("--config", "-c", default=CONFIG_FILE, help="Configuration file")
@click.option("--no-git", is_flag=True, help="Skip git detection")
@click.option("--preview", "-p", is_flag=True, help="Preview before saving")
def generate(output: str, template: str, config: str, no_git: bool, preview: bool):
    """Generate a README file interactively."""
    print_banner()

    context = {}

    # Try to load existing config
    existing_config = load_config(config)
    if existing_config:
        if Confirm.ask("Found existing configuration. Load it?", default=True):
            context = existing_config
            console.print("[green]Loaded existing configuration[/green]")

    # Detect git info
    git_info = None
    if not no_git and not context:
        with console.status("[bold blue]Detecting git information..."):
            git_info = detect_git_info()

        if git_info.is_git_repo:
            display_git_info(git_info)
            suggested = get_suggested_context(git_info, detect_project_type())
            context.update(suggested)

    # Collect project info if not loaded from config
    if not context or Confirm.ask("Update project information?", default=not bool(context)):
        context = collect_project_info(git_info, context)
        context = collect_installation_info(context)
        context = collect_features(context)

    # Select template
    if not template:
        template = select_template()

    # Select badges
    context = select_badges(context)

    # Generate README
    readme_content = render_template(template, context)

    # Preview if requested
    if preview:
        preview_readme(readme_content)
        if not Confirm.ask("Save this README?", default=True):
            console.print("[yellow]README generation cancelled[/yellow]")
            return

    # Save README
    output_path = generate_readme(context, template, output)
    console.print(f"\n[bold green]Successfully generated {output_path}![/bold green]")

    # Save config
    if Confirm.ask("Save configuration for future use?", default=True):
        save_config(context, config)

    # Offer to generate license file
    if context.get("license") and context["license"] != "None":
        if Confirm.ask(f"Generate LICENSE file ({context['license']})?", default=True):
            author = context.get("author_name", context.get("github_username", ""))
            if save_license_file(context["license"], author):
                console.print("[green]LICENSE file generated![/green]")
            else:
                console.print("[yellow]Could not generate LICENSE file[/yellow]")


@cli.command()
def tui():
    """Launch the interactive TUI interface."""
    try:
        from .tui import ReadmeForgeApp
        app = ReadmeForgeApp()
        app.run()
    except ImportError as e:
        console.print(f"[red]TUI dependencies not installed: {e}[/red]")
        console.print("Install with: pip install readme-forge[tui]")


@cli.command()
def templates():
    """List available templates."""
    print_banner()
    display_templates()


@cli.command()
@click.argument("template_name", default="standard")
def sections(template_name: str):
    """Show sections for a template."""
    print_banner()
    section_names = get_section_names(template_name)

    if not section_names:
        console.print(f"[red]Template '{template_name}' not found[/red]")
        return

    table = Table(title=f"Sections in '{template_name}' template")
    table.add_column("#", style="dim")
    table.add_column("Section", style="cyan")

    for i, name in enumerate(section_names, 1):
        table.add_row(str(i), name)

    console.print(table)


@cli.command()
def licenses():
    """List available licenses."""
    print_banner()

    table = Table(title="Available Licenses")
    table.add_column("License", style="cyan")
    table.add_column("SPDX ID", style="green")

    from .licenses import LICENSES
    for license_id, info in LICENSES.items():
        table.add_row(info["name"], info["spdx_id"])

    console.print(table)


@cli.command()
@click.argument("license_id")
@click.option("--author", "-a", default="Your Name", help="Copyright holder name")
@click.option("--output", "-o", default="LICENSE", help="Output file path")
def license(license_id: str, author: str, output: str):
    """Generate a LICENSE file."""
    print_banner()

    if save_license_file(license_id, author, output):
        console.print(f"[green]Generated {output} ({license_id})[/green]")
    else:
        console.print(f"[red]License '{license_id}' not found[/red]")
        console.print("Use 'readme-forge licenses' to see available licenses")


@cli.command()
def info():
    """Show detected project information."""
    print_banner()

    with console.status("[bold blue]Analyzing project..."):
        git_info = detect_git_info()
        project_type = detect_project_type()

    display_git_info(git_info)

    console.print(f"\n[bold]Detected Project Type:[/bold] [cyan]{project_type}[/cyan]")


# Legacy command for backward compatibility
@click.command()
def forge():
    """Legacy command - use 'readme-forge generate' instead."""
    console.print("[yellow]Note: 'forge' is deprecated. Use 'readme-forge generate' instead.[/yellow]\n")
    ctx = click.Context(generate)
    ctx.invoke(generate)


if __name__ == "__main__":
    cli()
