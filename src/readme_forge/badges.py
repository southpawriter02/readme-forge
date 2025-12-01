"""
Badge generation utilities for readme-forge.
Generates shield.io badges for various purposes.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class Badge:
    """Represents a badge/shield for the README."""
    name: str
    url: str
    link: Optional[str] = None
    alt: Optional[str] = None

    def to_markdown(self) -> str:
        """Convert badge to markdown format."""
        alt_text = self.alt or self.name
        if self.link:
            return f"[![{alt_text}]({self.url})]({self.link})"
        return f"![{alt_text}]({self.url})"


# Badge templates using shields.io
BADGE_TEMPLATES = {
    # License badges
    "license": {
        "name": "License",
        "url": "https://img.shields.io/badge/license-{license}-blue.svg",
        "link": "#license",
    },
    "license_github": {
        "name": "License",
        "url": "https://img.shields.io/github/license/{username}/{repo}",
        "link": "https://github.com/{username}/{repo}/blob/main/LICENSE",
    },

    # Version badges
    "version": {
        "name": "Version",
        "url": "https://img.shields.io/badge/version-{version}-green.svg",
    },
    "pypi_version": {
        "name": "PyPI Version",
        "url": "https://img.shields.io/pypi/v/{package}",
        "link": "https://pypi.org/project/{package}/",
    },
    "npm_version": {
        "name": "npm Version",
        "url": "https://img.shields.io/npm/v/{package}",
        "link": "https://www.npmjs.com/package/{package}",
    },

    # GitHub badges
    "github_stars": {
        "name": "GitHub Stars",
        "url": "https://img.shields.io/github/stars/{username}/{repo}",
        "link": "https://github.com/{username}/{repo}/stargazers",
    },
    "github_forks": {
        "name": "GitHub Forks",
        "url": "https://img.shields.io/github/forks/{username}/{repo}",
        "link": "https://github.com/{username}/{repo}/network/members",
    },
    "github_issues": {
        "name": "GitHub Issues",
        "url": "https://img.shields.io/github/issues/{username}/{repo}",
        "link": "https://github.com/{username}/{repo}/issues",
    },
    "github_prs": {
        "name": "GitHub Pull Requests",
        "url": "https://img.shields.io/github/issues-pr/{username}/{repo}",
        "link": "https://github.com/{username}/{repo}/pulls",
    },
    "github_last_commit": {
        "name": "Last Commit",
        "url": "https://img.shields.io/github/last-commit/{username}/{repo}",
        "link": "https://github.com/{username}/{repo}/commits",
    },
    "github_contributors": {
        "name": "Contributors",
        "url": "https://img.shields.io/github/contributors/{username}/{repo}",
        "link": "https://github.com/{username}/{repo}/graphs/contributors",
    },
    "github_release": {
        "name": "Latest Release",
        "url": "https://img.shields.io/github/v/release/{username}/{repo}",
        "link": "https://github.com/{username}/{repo}/releases/latest",
    },

    # CI/CD badges
    "github_actions": {
        "name": "GitHub Actions",
        "url": "https://img.shields.io/github/actions/workflow/status/{username}/{repo}/{workflow}",
        "link": "https://github.com/{username}/{repo}/actions",
    },
    "travis_ci": {
        "name": "Travis CI",
        "url": "https://img.shields.io/travis/com/{username}/{repo}",
        "link": "https://travis-ci.com/{username}/{repo}",
    },
    "circleci": {
        "name": "CircleCI",
        "url": "https://img.shields.io/circleci/build/github/{username}/{repo}",
        "link": "https://circleci.com/gh/{username}/{repo}",
    },

    # Code quality badges
    "codecov": {
        "name": "Code Coverage",
        "url": "https://img.shields.io/codecov/c/github/{username}/{repo}",
        "link": "https://codecov.io/gh/{username}/{repo}",
    },
    "codeclimate": {
        "name": "Code Climate",
        "url": "https://img.shields.io/codeclimate/maintainability/{username}/{repo}",
        "link": "https://codeclimate.com/github/{username}/{repo}",
    },

    # Python specific
    "python_version": {
        "name": "Python Version",
        "url": "https://img.shields.io/pypi/pyversions/{package}",
        "link": "https://pypi.org/project/{package}/",
    },
    "pypi_downloads": {
        "name": "PyPI Downloads",
        "url": "https://img.shields.io/pypi/dm/{package}",
        "link": "https://pypi.org/project/{package}/",
    },

    # Node.js specific
    "npm_downloads": {
        "name": "npm Downloads",
        "url": "https://img.shields.io/npm/dm/{package}",
        "link": "https://www.npmjs.com/package/{package}",
    },
    "node_version": {
        "name": "Node Version",
        "url": "https://img.shields.io/node/v/{package}",
    },

    # Documentation
    "docs": {
        "name": "Documentation",
        "url": "https://img.shields.io/badge/docs-{status}-blue.svg",
        "link": "{docs_url}",
    },
    "readthedocs": {
        "name": "Read the Docs",
        "url": "https://img.shields.io/readthedocs/{project}",
        "link": "https://{project}.readthedocs.io/",
    },

    # Social badges
    "twitter": {
        "name": "Twitter Follow",
        "url": "https://img.shields.io/twitter/follow/{handle}?style=social",
        "link": "https://twitter.com/{handle}",
    },
    "discord": {
        "name": "Discord",
        "url": "https://img.shields.io/discord/{server_id}",
        "link": "{invite_link}",
    },

    # Custom badges
    "custom": {
        "name": "Custom",
        "url": "https://img.shields.io/badge/{label}-{message}-{color}",
    },

    # Maintenance badges
    "maintained": {
        "name": "Maintained",
        "url": "https://img.shields.io/badge/maintained-yes-green.svg",
    },
    "maintenance_status": {
        "name": "Maintenance",
        "url": "https://img.shields.io/maintenance/{status}/{year}",
    },

    # Platform badges
    "platform": {
        "name": "Platform",
        "url": "https://img.shields.io/badge/platform-{platforms}-lightgrey",
    },

    # Made with badges
    "made_with_python": {
        "name": "Made with Python",
        "url": "https://img.shields.io/badge/Made%20with-Python-1f425f.svg",
        "link": "https://www.python.org/",
    },
    "made_with_javascript": {
        "name": "Made with JavaScript",
        "url": "https://img.shields.io/badge/Made%20with-JavaScript-f7df1e.svg",
        "link": "https://www.javascript.com/",
    },
    "made_with_typescript": {
        "name": "Made with TypeScript",
        "url": "https://img.shields.io/badge/Made%20with-TypeScript-3178c6.svg",
        "link": "https://www.typescriptlang.org/",
    },
    "made_with_rust": {
        "name": "Made with Rust",
        "url": "https://img.shields.io/badge/Made%20with-Rust-dea584.svg",
        "link": "https://www.rust-lang.org/",
    },
    "made_with_go": {
        "name": "Made with Go",
        "url": "https://img.shields.io/badge/Made%20with-Go-00add8.svg",
        "link": "https://go.dev/",
    },
}


# Badge presets for different project types
BADGE_PRESETS = {
    "minimal": ["license"],
    "python_library": [
        "license_github",
        "pypi_version",
        "python_version",
        "pypi_downloads",
        "github_actions",
        "codecov",
    ],
    "python_cli": [
        "license_github",
        "pypi_version",
        "python_version",
        "github_stars",
        "github_last_commit",
    ],
    "node_package": [
        "license_github",
        "npm_version",
        "npm_downloads",
        "node_version",
        "github_actions",
    ],
    "web_app": [
        "license_github",
        "github_stars",
        "github_issues",
        "github_last_commit",
        "github_actions",
    ],
    "api": [
        "license_github",
        "github_actions",
        "codecov",
        "github_issues",
    ],
    "github_standard": [
        "license_github",
        "github_stars",
        "github_forks",
        "github_issues",
        "github_last_commit",
    ],
}


def generate_badge(
    badge_type: str,
    **kwargs
) -> Optional[Badge]:
    """
    Generate a single badge.

    Args:
        badge_type: The type of badge to generate (key from BADGE_TEMPLATES)
        **kwargs: Parameters to fill in the badge template

    Returns:
        Badge object or None if badge_type is not found
    """
    template = BADGE_TEMPLATES.get(badge_type)
    if not template:
        return None

    try:
        url = template["url"].format(**kwargs)
        link = template.get("link", "").format(**kwargs) if template.get("link") else None
        name = template["name"]

        return Badge(name=name, url=url, link=link)
    except KeyError:
        # Missing required parameter
        return None


def generate_badges(
    badge_types: List[str],
    **kwargs
) -> List[Badge]:
    """
    Generate multiple badges.

    Args:
        badge_types: List of badge types to generate
        **kwargs: Parameters to fill in the badge templates

    Returns:
        List of Badge objects
    """
    badges = []
    for badge_type in badge_types:
        badge = generate_badge(badge_type, **kwargs)
        if badge:
            badges.append(badge)
    return badges


def generate_badges_from_preset(
    preset: str,
    **kwargs
) -> List[Badge]:
    """
    Generate badges from a preset.

    Args:
        preset: Name of the preset (key from BADGE_PRESETS)
        **kwargs: Parameters to fill in the badge templates

    Returns:
        List of Badge objects
    """
    badge_types = BADGE_PRESETS.get(preset, BADGE_PRESETS["minimal"])
    return generate_badges(badge_types, **kwargs)


def badges_to_markdown(badges: List[Badge], separator: str = " ") -> str:
    """
    Convert a list of badges to markdown string.

    Args:
        badges: List of Badge objects
        separator: Separator between badges (default: space)

    Returns:
        Markdown string of badges
    """
    return separator.join(badge.to_markdown() for badge in badges)


def get_badge_types() -> List[str]:
    """Get all available badge types."""
    return list(BADGE_TEMPLATES.keys())


def get_presets() -> Dict[str, List[str]]:
    """Get all available badge presets."""
    return BADGE_PRESETS.copy()


def create_custom_badge(
    label: str,
    message: str,
    color: str = "blue",
    link: Optional[str] = None
) -> Badge:
    """
    Create a custom badge.

    Args:
        label: Left side text of the badge
        message: Right side text of the badge
        color: Color of the right side (hex without # or color name)
        link: Optional link for the badge

    Returns:
        Badge object
    """
    # URL encode label and message
    label = label.replace(" ", "%20").replace("-", "--")
    message = message.replace(" ", "%20").replace("-", "--")

    url = f"https://img.shields.io/badge/{label}-{message}-{color}"

    return Badge(
        name=f"{label} {message}",
        url=url,
        link=link
    )
