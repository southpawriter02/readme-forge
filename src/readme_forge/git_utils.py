"""
Git integration utilities for readme-forge.
Provides automatic detection of project information from git repositories.
"""

import os
import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class GitInfo:
    """Information extracted from a git repository."""
    is_git_repo: bool = False
    project_name: Optional[str] = None
    remote_url: Optional[str] = None
    github_username: Optional[str] = None
    repo_name: Optional[str] = None
    default_branch: Optional[str] = None
    description: Optional[str] = None
    contributors: List[str] = None
    recent_commits: List[str] = None
    has_license: bool = False
    license_type: Optional[str] = None
    has_readme: bool = False
    languages: List[str] = None

    def __post_init__(self):
        if self.contributors is None:
            self.contributors = []
        if self.recent_commits is None:
            self.recent_commits = []
        if self.languages is None:
            self.languages = []


def detect_git_info(path: str = ".") -> GitInfo:
    """
    Detect git repository information from the given path.

    Args:
        path: The path to the git repository (default: current directory)

    Returns:
        GitInfo object with detected information
    """
    info = GitInfo()

    try:
        import git

        try:
            repo = git.Repo(path, search_parent_directories=True)
            info.is_git_repo = True
        except git.InvalidGitRepositoryError:
            return info
        except git.NoSuchPathError:
            return info

        # Get project name from directory
        repo_path = repo.working_dir
        info.project_name = os.path.basename(repo_path)

        # Get remote URL and parse GitHub info
        try:
            if repo.remotes:
                remote = repo.remotes.origin
                info.remote_url = remote.url

                # Parse GitHub username and repo from URL
                github_match = re.search(
                    r'github\.com[:/]([^/]+)/([^/.]+)',
                    info.remote_url
                )
                if github_match:
                    info.github_username = github_match.group(1)
                    info.repo_name = github_match.group(2)
        except Exception:
            pass

        # Get default branch
        try:
            info.default_branch = repo.active_branch.name
        except Exception:
            info.default_branch = "main"

        # Get contributors from git log
        try:
            contributors = set()
            for commit in repo.iter_commits(max_count=100):
                contributors.add(commit.author.name)
            info.contributors = list(contributors)[:10]  # Limit to top 10
        except Exception:
            pass

        # Get recent commits
        try:
            recent = []
            for commit in repo.iter_commits(max_count=5):
                recent.append(commit.message.split('\n')[0][:80])
            info.recent_commits = recent
        except Exception:
            pass

        # Check for LICENSE file
        for license_name in ['LICENSE', 'LICENSE.md', 'LICENSE.txt', 'LICENCE']:
            license_path = os.path.join(repo_path, license_name)
            if os.path.exists(license_path):
                info.has_license = True
                info.license_type = _detect_license_type(license_path)
                break

        # Check for README
        for readme_name in ['README.md', 'README.rst', 'README.txt', 'README']:
            if os.path.exists(os.path.join(repo_path, readme_name)):
                info.has_readme = True
                break

        # Detect languages
        info.languages = _detect_languages(repo_path)

        # Try to get description from GitHub API (if remote is GitHub)
        if info.github_username and info.repo_name:
            info.description = _fetch_github_description(
                info.github_username,
                info.repo_name
            )

    except ImportError:
        # GitPython not installed, try basic detection
        info = _basic_git_detection(path)

    return info


def _basic_git_detection(path: str) -> GitInfo:
    """Basic git detection without GitPython."""
    info = GitInfo()

    git_dir = os.path.join(path, '.git')
    if not os.path.isdir(git_dir):
        return info

    info.is_git_repo = True
    info.project_name = os.path.basename(os.path.abspath(path))

    # Try to read remote from config
    config_path = os.path.join(git_dir, 'config')
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                content = f.read()
                url_match = re.search(r'url\s*=\s*(.+)', content)
                if url_match:
                    info.remote_url = url_match.group(1).strip()

                    github_match = re.search(
                        r'github\.com[:/]([^/]+)/([^/.]+)',
                        info.remote_url
                    )
                    if github_match:
                        info.github_username = github_match.group(1)
                        info.repo_name = github_match.group(2)
        except Exception:
            pass

    return info


def _detect_license_type(license_path: str) -> Optional[str]:
    """Try to detect the license type from the license file content."""
    try:
        with open(license_path, 'r') as f:
            content = f.read().lower()[:1000]

        if 'mit license' in content or 'permission is hereby granted, free of charge' in content:
            return 'MIT'
        elif 'apache license' in content and 'version 2.0' in content:
            return 'Apache-2.0'
        elif 'gnu general public license' in content:
            if 'version 3' in content:
                return 'GPL-3.0'
            elif 'version 2' in content:
                return 'GPL-2.0'
            return 'GPL'
        elif 'bsd' in content:
            if '3-clause' in content or 'three clause' in content:
                return 'BSD-3-Clause'
            elif '2-clause' in content or 'two clause' in content:
                return 'BSD-2-Clause'
            return 'BSD'
        elif 'isc license' in content:
            return 'ISC'
        elif 'mozilla public license' in content:
            return 'MPL-2.0'
        elif 'unlicense' in content:
            return 'Unlicense'
    except Exception:
        pass

    return None


def _detect_languages(repo_path: str) -> List[str]:
    """Detect programming languages used in the repository."""
    languages = set()

    extension_map = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.jsx': 'JavaScript',
        '.tsx': 'TypeScript',
        '.java': 'Java',
        '.go': 'Go',
        '.rs': 'Rust',
        '.rb': 'Ruby',
        '.php': 'PHP',
        '.cs': 'C#',
        '.cpp': 'C++',
        '.c': 'C',
        '.h': 'C/C++',
        '.swift': 'Swift',
        '.kt': 'Kotlin',
        '.scala': 'Scala',
        '.r': 'R',
        '.R': 'R',
        '.sh': 'Shell',
        '.bash': 'Shell',
        '.ps1': 'PowerShell',
        '.lua': 'Lua',
        '.pl': 'Perl',
        '.ex': 'Elixir',
        '.exs': 'Elixir',
        '.clj': 'Clojure',
        '.hs': 'Haskell',
        '.ml': 'OCaml',
        '.dart': 'Dart',
        '.vue': 'Vue',
        '.svelte': 'Svelte',
    }

    # Walk through the repository
    for root, dirs, files in os.walk(repo_path):
        # Skip hidden directories and common non-source directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in [
            'node_modules', 'venv', 'env', '.venv', '__pycache__',
            'dist', 'build', 'target', 'vendor', '.git'
        ]]

        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in extension_map:
                languages.add(extension_map[ext])

        # Limit depth to avoid too deep traversal
        if root.count(os.sep) - repo_path.count(os.sep) > 3:
            break

    return sorted(list(languages))


def _fetch_github_description(username: str, repo: str) -> Optional[str]:
    """Fetch repository description from GitHub API."""
    try:
        import requests

        url = f"https://api.github.com/repos/{username}/{repo}"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            return data.get('description')
    except Exception:
        pass

    return None


def detect_project_type(path: str = ".") -> str:
    """
    Detect the type of project based on files present.

    Returns one of: python_library, cli_tool, web_app, api, standard
    """
    path = os.path.abspath(path)

    # Check for specific files that indicate project type
    files = set(os.listdir(path))

    # Check for package.json (Node.js)
    if 'package.json' in files:
        try:
            import json
            with open(os.path.join(path, 'package.json'), 'r') as f:
                pkg = json.load(f)
                if 'bin' in pkg:
                    return 'cli_tool'
                if any(dep in pkg.get('dependencies', {}) for dep in
                       ['express', 'fastify', 'koa', 'hapi', 'nest']):
                    return 'api'
                if any(dep in pkg.get('dependencies', {}) for dep in
                       ['react', 'vue', 'angular', 'svelte', 'next', 'nuxt']):
                    return 'web_app'
        except Exception:
            pass

    # Check for Python project indicators
    if 'pyproject.toml' in files or 'setup.py' in files:
        try:
            if 'pyproject.toml' in files:
                with open(os.path.join(path, 'pyproject.toml'), 'r') as f:
                    content = f.read()
                    if '[tool.poetry.scripts]' in content or 'console_scripts' in content:
                        return 'cli_tool'
            if 'setup.py' in files:
                with open(os.path.join(path, 'setup.py'), 'r') as f:
                    content = f.read()
                    if 'entry_points' in content or 'console_scripts' in content:
                        return 'cli_tool'
        except Exception:
            pass

        # Check for web frameworks
        requirements_files = ['requirements.txt', 'Pipfile', 'pyproject.toml']
        for req_file in requirements_files:
            if req_file in files:
                try:
                    with open(os.path.join(path, req_file), 'r') as f:
                        content = f.read().lower()
                        if any(fw in content for fw in ['django', 'flask', 'fastapi', 'starlette']):
                            if any(api in content for api in ['fastapi', 'drf', 'rest_framework']):
                                return 'api'
                            return 'web_app'
                except Exception:
                    pass

        return 'python_library'

    # Check for Go
    if 'go.mod' in files:
        try:
            with open(os.path.join(path, 'go.mod'), 'r') as f:
                content = f.read()
            # Check for main package with cobra/cli indicators
            if os.path.exists(os.path.join(path, 'cmd')):
                return 'cli_tool'
        except Exception:
            pass

    # Check for Rust
    if 'Cargo.toml' in files:
        try:
            with open(os.path.join(path, 'Cargo.toml'), 'r') as f:
                content = f.read()
                if '[[bin]]' in content or 'clap' in content:
                    return 'cli_tool'
        except Exception:
            pass

    # Check for Dockerfile/docker-compose (might be API/web service)
    if 'Dockerfile' in files or 'docker-compose.yml' in files:
        return 'api'

    return 'standard'


def get_suggested_context(git_info: GitInfo, project_type: str) -> Dict[str, Any]:
    """
    Generate suggested context for README generation based on git info.
    """
    context = {}

    if git_info.project_name:
        context['project_name'] = git_info.project_name

    if git_info.github_username:
        context['github_username'] = git_info.github_username

    if git_info.description:
        context['project_description'] = git_info.description

    if git_info.license_type:
        context['license'] = git_info.license_type

    if git_info.contributors:
        context['acknowledgments'] = [f"@{c}" for c in git_info.contributors[:5]]

    if git_info.languages:
        context['languages'] = git_info.languages

    return context
