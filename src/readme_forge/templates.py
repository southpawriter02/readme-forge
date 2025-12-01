"""
Template management for readme-forge.
Provides multiple README templates for different project types.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class TemplateSection:
    """Represents a section in a README template."""
    name: str
    title: str
    content: str
    optional: bool = True
    order: int = 0

@dataclass
class Template:
    """Represents a complete README template."""
    name: str
    description: str
    project_types: List[str]
    sections: List[TemplateSection]


# Default sections that can be included in any template
DEFAULT_SECTIONS = {
    "header": TemplateSection(
        name="header",
        title="",
        content="""# {{ project_name }}

{% if badges %}
{{ badges }}
{% endif %}

{{ project_description }}
""",
        optional=False,
        order=0
    ),
    "features": TemplateSection(
        name="features",
        title="Features",
        content="""## Features

{% if features %}
{% for feature in features %}
- {{ feature }}
{% endfor %}
{% else %}
- Feature 1
- Feature 2
- Feature 3
{% endif %}
""",
        optional=True,
        order=10
    ),
    "demo": TemplateSection(
        name="demo",
        title="Demo",
        content="""## Demo

{% if demo_gif %}
![Demo]({{ demo_gif }})
{% endif %}

{% if demo_url %}
[Live Demo]({{ demo_url }})
{% endif %}
""",
        optional=True,
        order=15
    ),
    "prerequisites": TemplateSection(
        name="prerequisites",
        title="Prerequisites",
        content="""## Prerequisites

{% if prerequisites %}
{% for prereq in prerequisites %}
- {{ prereq }}
{% endfor %}
{% else %}
Before you begin, ensure you have the following installed:
- Python 3.8 or higher
{% endif %}
""",
        optional=True,
        order=20
    ),
    "installation": TemplateSection(
        name="installation",
        title="Installation",
        content="""## Installation

{% if installation_instructions %}
```bash
{{ installation_instructions }}
```
{% else %}
```bash
pip install {{ project_name }}
```
{% endif %}
""",
        optional=False,
        order=30
    ),
    "usage": TemplateSection(
        name="usage",
        title="Usage",
        content="""## Usage

{% if usage_instructions %}
```{{ code_language|default('bash') }}
{{ usage_instructions }}
```
{% else %}
```bash
{{ project_name }} --help
```
{% endif %}

{% if usage_examples %}
### Examples

{% for example in usage_examples %}
#### {{ example.title }}

```{{ example.language|default('bash') }}
{{ example.code }}
```

{% endfor %}
{% endif %}
""",
        optional=False,
        order=40
    ),
    "api_reference": TemplateSection(
        name="api_reference",
        title="API Reference",
        content="""## API Reference

{% if api_docs_url %}
For detailed API documentation, visit [API Docs]({{ api_docs_url }}).
{% else %}
### Core Functions

| Function | Description |
|----------|-------------|
| `function_name()` | Description of function |

{% endif %}
""",
        optional=True,
        order=50
    ),
    "configuration": TemplateSection(
        name="configuration",
        title="Configuration",
        content="""## Configuration

{% if config_file %}
Create a `{{ config_file }}` file in your project root:

```{{ config_format|default('json') }}
{{ config_example|default('{}') }}
```
{% endif %}

{% if env_vars %}
### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
{% for var in env_vars %}
| `{{ var.name }}` | {{ var.description }} | {{ var.default|default('None') }} |
{% endfor %}
{% endif %}
""",
        optional=True,
        order=55
    ),
    "roadmap": TemplateSection(
        name="roadmap",
        title="Roadmap",
        content="""## Roadmap

{% if roadmap_items %}
{% for item in roadmap_items %}
- [{% if item.done %}x{% else %} {% endif %}] {{ item.title }}
{% endfor %}
{% else %}
- [x] Initial release
- [ ] Add more features
- [ ] Write comprehensive documentation
{% endif %}

See the [open issues](https://github.com/{{ github_username }}/{{ project_name }}/issues) for a full list of proposed features and known issues.
""",
        optional=True,
        order=60
    ),
    "contributing": TemplateSection(
        name="contributing",
        title="Contributing",
        content="""## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

{% if contributing_file %}
Please read [CONTRIBUTING.md]({{ contributing_file }}) for details on our code of conduct and the process for submitting pull requests.
{% endif %}
""",
        optional=True,
        order=70
    ),
    "testing": TemplateSection(
        name="testing",
        title="Testing",
        content="""## Testing

{% if test_command %}
```bash
{{ test_command }}
```
{% else %}
```bash
pytest
```
{% endif %}

{% if coverage_command %}
### Coverage

```bash
{{ coverage_command }}
```
{% endif %}
""",
        optional=True,
        order=65
    ),
    "license": TemplateSection(
        name="license",
        title="License",
        content="""## License

{% if license and license != 'None' %}
This project is licensed under the {{ license }} License - see the [LICENSE](LICENSE) file for details.
{% else %}
This project is provided as-is without any license.
{% endif %}
""",
        optional=False,
        order=80
    ),
    "contact": TemplateSection(
        name="contact",
        title="Contact",
        content="""## Contact

{% if author_name %}{{ author_name }}{% else %}Your Name{% endif %}{% if author_email %} - {{ author_email }}{% endif %}

{% if twitter_handle %}
Twitter: [@{{ twitter_handle }}](https://twitter.com/{{ twitter_handle }})
{% endif %}

Project Link: [https://github.com/{{ github_username }}/{{ project_name }}](https://github.com/{{ github_username }}/{{ project_name }})
""",
        optional=True,
        order=90
    ),
    "acknowledgments": TemplateSection(
        name="acknowledgments",
        title="Acknowledgments",
        content="""## Acknowledgments

{% if acknowledgments %}
{% for ack in acknowledgments %}
- {{ ack }}
{% endfor %}
{% else %}
- Thanks to all contributors
{% endif %}
""",
        optional=True,
        order=100
    ),
    "toc": TemplateSection(
        name="toc",
        title="Table of Contents",
        content="""## Table of Contents

{{ table_of_contents }}
""",
        optional=True,
        order=5
    ),
}


# Project type specific templates
TEMPLATES: Dict[str, Template] = {
    "python_library": Template(
        name="python_library",
        description="Template for Python libraries and packages",
        project_types=["library", "package", "module"],
        sections=[
            DEFAULT_SECTIONS["header"],
            DEFAULT_SECTIONS["toc"],
            DEFAULT_SECTIONS["features"],
            DEFAULT_SECTIONS["prerequisites"],
            DEFAULT_SECTIONS["installation"],
            DEFAULT_SECTIONS["usage"],
            DEFAULT_SECTIONS["api_reference"],
            DEFAULT_SECTIONS["configuration"],
            DEFAULT_SECTIONS["testing"],
            DEFAULT_SECTIONS["roadmap"],
            DEFAULT_SECTIONS["contributing"],
            DEFAULT_SECTIONS["license"],
            DEFAULT_SECTIONS["contact"],
            DEFAULT_SECTIONS["acknowledgments"],
        ]
    ),
    "cli_tool": Template(
        name="cli_tool",
        description="Template for command-line interface tools",
        project_types=["cli", "command-line", "terminal"],
        sections=[
            DEFAULT_SECTIONS["header"],
            DEFAULT_SECTIONS["toc"],
            DEFAULT_SECTIONS["features"],
            DEFAULT_SECTIONS["demo"],
            DEFAULT_SECTIONS["prerequisites"],
            DEFAULT_SECTIONS["installation"],
            DEFAULT_SECTIONS["usage"],
            DEFAULT_SECTIONS["configuration"],
            DEFAULT_SECTIONS["roadmap"],
            DEFAULT_SECTIONS["contributing"],
            DEFAULT_SECTIONS["license"],
            DEFAULT_SECTIONS["contact"],
        ]
    ),
    "web_app": Template(
        name="web_app",
        description="Template for web applications",
        project_types=["web", "webapp", "website", "frontend", "backend"],
        sections=[
            DEFAULT_SECTIONS["header"],
            DEFAULT_SECTIONS["toc"],
            DEFAULT_SECTIONS["features"],
            DEFAULT_SECTIONS["demo"],
            DEFAULT_SECTIONS["prerequisites"],
            DEFAULT_SECTIONS["installation"],
            DEFAULT_SECTIONS["usage"],
            DEFAULT_SECTIONS["configuration"],
            DEFAULT_SECTIONS["api_reference"],
            DEFAULT_SECTIONS["testing"],
            DEFAULT_SECTIONS["roadmap"],
            DEFAULT_SECTIONS["contributing"],
            DEFAULT_SECTIONS["license"],
            DEFAULT_SECTIONS["contact"],
            DEFAULT_SECTIONS["acknowledgments"],
        ]
    ),
    "api": Template(
        name="api",
        description="Template for REST APIs and backend services",
        project_types=["api", "rest", "backend", "service", "microservice"],
        sections=[
            DEFAULT_SECTIONS["header"],
            DEFAULT_SECTIONS["toc"],
            DEFAULT_SECTIONS["features"],
            DEFAULT_SECTIONS["prerequisites"],
            DEFAULT_SECTIONS["installation"],
            DEFAULT_SECTIONS["usage"],
            DEFAULT_SECTIONS["api_reference"],
            DEFAULT_SECTIONS["configuration"],
            DEFAULT_SECTIONS["testing"],
            DEFAULT_SECTIONS["roadmap"],
            DEFAULT_SECTIONS["contributing"],
            DEFAULT_SECTIONS["license"],
            DEFAULT_SECTIONS["contact"],
        ]
    ),
    "minimal": Template(
        name="minimal",
        description="A minimal README template",
        project_types=["minimal", "simple", "basic"],
        sections=[
            DEFAULT_SECTIONS["header"],
            DEFAULT_SECTIONS["installation"],
            DEFAULT_SECTIONS["usage"],
            DEFAULT_SECTIONS["license"],
        ]
    ),
    "standard": Template(
        name="standard",
        description="A standard README template suitable for most projects",
        project_types=["standard", "default", "general"],
        sections=[
            DEFAULT_SECTIONS["header"],
            DEFAULT_SECTIONS["toc"],
            DEFAULT_SECTIONS["features"],
            DEFAULT_SECTIONS["prerequisites"],
            DEFAULT_SECTIONS["installation"],
            DEFAULT_SECTIONS["usage"],
            DEFAULT_SECTIONS["roadmap"],
            DEFAULT_SECTIONS["contributing"],
            DEFAULT_SECTIONS["license"],
            DEFAULT_SECTIONS["contact"],
            DEFAULT_SECTIONS["acknowledgments"],
        ]
    ),
}


def get_template(template_name: str) -> Optional[Template]:
    """Get a template by name."""
    return TEMPLATES.get(template_name)


def get_template_names() -> List[str]:
    """Get all available template names."""
    return list(TEMPLATES.keys())


def get_template_descriptions() -> Dict[str, str]:
    """Get all template names with their descriptions."""
    return {name: tmpl.description for name, tmpl in TEMPLATES.items()}


def render_template(template_name: str, context: Dict) -> str:
    """Render a template with the given context."""
    from jinja2 import Environment

    template = get_template(template_name)
    if not template:
        template = TEMPLATES["standard"]

    env = Environment()

    # Sort sections by order
    sorted_sections = sorted(template.sections, key=lambda s: s.order)

    # Generate table of contents if toc section is included
    if any(s.name == "toc" for s in sorted_sections):
        toc_items = []
        for section in sorted_sections:
            if section.name != "toc" and section.name != "header" and section.title:
                anchor = section.title.lower().replace(" ", "-")
                toc_items.append(f"- [{section.title}](#{anchor})")
        context["table_of_contents"] = "\n".join(toc_items)

    # Render each section
    rendered_parts = []
    for section in sorted_sections:
        try:
            section_template = env.from_string(section.content)
            rendered = section_template.render(context)
            # Only include non-empty sections
            if rendered.strip():
                rendered_parts.append(rendered)
        except Exception:
            # Skip sections that fail to render
            pass

    return "\n".join(rendered_parts)


def get_section_names(template_name: str) -> List[str]:
    """Get the section names for a specific template."""
    template = get_template(template_name)
    if not template:
        return []
    return [s.name for s in template.sections]
