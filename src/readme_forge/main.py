import click
import questionary
from jinja2 import Environment, FileSystemLoader
import os
import json

@click.command()
def forge():
    """
    A CLI tool to generate beautiful and effective READMEs.
    """
    """
    A CLI tool to generate beautiful and effective READMEs.
    """
    click.echo("Welcome to readme-forge!")

    config_path = "readme-forge.json"
    context = {}

    if os.path.exists(config_path):
        if questionary.confirm("A 'readme-forge.json' file was found. Do you want to load answers from it?").ask():
            with open(config_path, "r") as f:
                context = json.load(f)
            click.echo("Loaded answers from readme-forge.json")

    # If context is empty, or user wants to overwrite, ask questions
    if not context:
        context = {
            "project_name": questionary.text("What is the name of your project?").ask(),
            "project_description": questionary.text("Enter a short description of your project:").ask(),
            "license": questionary.select(
                "Choose a license for your project:",
                choices=["MIT", "Apache 2.0", "GPLv3", "BSD 3-Clause", "None"],
            ).ask(),
            "github_username": questionary.text("What is your GitHub username?").ask(),
            "installation_instructions": questionary.text(
                "Enter the installation instructions (e.g., pip install myproject):"
            ).ask(),
            "usage_instructions": questionary.text(
                "Enter the usage instructions:",
                multiline=True
            ).ask(),
        }
        # Save the context
        with open(config_path, "w") as f:
            json.dump(context, f, indent=4)
        click.echo(f"Your answers have been saved to {config_path} for future use.")

    # Setup Jinja2 environment
    # The template is in the same directory as the script
    template_dir = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("README_TEMPLATE.md")

    # Render the template
    rendered_readme = template.render(context)

    # Write the rendered README to a file
    output_path = "README.md"
    with open(output_path, "w") as f:
        f.write(rendered_readme)

    click.echo(f"\\nSuccessfully generated {output_path}!")

    return output_path


if __name__ == "__main__":
    forge()
