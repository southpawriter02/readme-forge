"""
readme-forge: A powerful tool to generate beautiful and effective READMEs.

This package provides CLI and TUI interfaces for generating README files
with automatic git detection, multiple templates, badge generation, and more.
"""

__version__ = "0.2.0"
__author__ = "Jules"

from .templates import (
    get_template_names,
    get_template_descriptions,
    render_template,
    get_section_names,
    Template,
    TemplateSection,
)

from .git_utils import (
    detect_git_info,
    detect_project_type,
    get_suggested_context,
    GitInfo,
)

from .badges import (
    generate_badge,
    generate_badges,
    generate_badges_from_preset,
    badges_to_markdown,
    create_custom_badge,
    get_badge_types,
    get_presets,
    Badge,
)

from .licenses import (
    get_license_names,
    get_license_info,
    generate_license_text,
    save_license_file,
    get_license_badge_name,
)

__all__ = [
    # Version
    "__version__",
    "__author__",
    # Templates
    "get_template_names",
    "get_template_descriptions",
    "render_template",
    "get_section_names",
    "Template",
    "TemplateSection",
    # Git utilities
    "detect_git_info",
    "detect_project_type",
    "get_suggested_context",
    "GitInfo",
    # Badges
    "generate_badge",
    "generate_badges",
    "generate_badges_from_preset",
    "badges_to_markdown",
    "create_custom_badge",
    "get_badge_types",
    "get_presets",
    "Badge",
    # Licenses
    "get_license_names",
    "get_license_info",
    "generate_license_text",
    "save_license_file",
    "get_license_badge_name",
]
