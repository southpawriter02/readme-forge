# readme-forge

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Version](https://img.shields.io/badge/version-0.2.0-green.svg)](https://github.com/southpawriter02/readme-forge)

A powerful tool to generate beautiful and effective READMEs with an interactive CLI and TUI interface.

## Features

- **Interactive CLI** - Rich, colorful command-line interface with intuitive prompts
- **Modern TUI** - Full-featured text user interface built with Textual
- **Git Integration** - Automatic detection of project information from git repositories
- **Multiple Templates** - Choose from various templates (standard, minimal, CLI tool, web app, API, Python library)
- **Badge Generation** - Automatic generation of shields.io badges with presets
- **License Generation** - Generate LICENSE files for various open source licenses
- **Live Preview** - Preview your README before saving
- **Configuration Persistence** - Save and load your configuration for future use
- **Project Type Detection** - Automatically detects project type based on files present

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [CLI Mode](#cli-mode)
  - [TUI Mode](#tui-mode)
- [Templates](#templates)
- [Commands](#commands)
- [Configuration](#configuration)
- [Development](#development)
- [License](#license)

## Installation

```bash
pip install readme-forge
```

Or install from source:

```bash
git clone https://github.com/southpawriter02/readme-forge.git
cd readme-forge
pip install -e .
```

## Usage

### CLI Mode

Generate a README interactively:

```bash
readme-forge generate
```

Options:
- `-o, --output` - Output file path (default: README.md)
- `-t, --template` - Template to use
- `-c, --config` - Configuration file path
- `--no-git` - Skip git detection
- `-p, --preview` - Preview before saving

### TUI Mode

Launch the interactive TUI:

```bash
readme-forge tui
```

The TUI provides:
- Form-based input for all project information
- Real-time git information display
- Template and badge preset selection
- Live preview with markdown rendering
- Configuration save/load functionality

**Keyboard Shortcuts:**
- `g` - Generate README
- `p` - Preview README
- `s` - Save configuration
- `l` - Load configuration
- `d` - Detect git info
- `q` - Quit

### Quick Commands

```bash
# List available templates
readme-forge templates

# Show sections for a template
readme-forge sections standard

# List available licenses
readme-forge licenses

# Generate a LICENSE file
readme-forge license MIT --author "Your Name"

# Show detected project info
readme-forge info
```

## Templates

| Template | Description |
|----------|-------------|
| `standard` | Standard README suitable for most projects |
| `minimal` | Minimal README with essential sections only |
| `python_library` | Optimized for Python libraries and packages |
| `cli_tool` | For command-line interface tools |
| `web_app` | For web applications |
| `api` | For REST APIs and backend services |

## Commands

| Command | Description |
|---------|-------------|
| `generate` | Generate a README file interactively |
| `tui` | Launch the interactive TUI interface |
| `templates` | List available templates |
| `sections` | Show sections for a template |
| `licenses` | List available licenses |
| `license` | Generate a LICENSE file |
| `info` | Show detected project information |

## Configuration

Configuration is stored in `readme-forge.json`:

```json
{
  "project_name": "my-project",
  "project_description": "A description of my project",
  "github_username": "username",
  "author_name": "Your Name",
  "license": "MIT",
  "installation_instructions": "pip install my-project",
  "usage_instructions": "my-project --help"
}
```

## Badge Presets

Available badge presets:
- `minimal` - License badge only
- `python_library` - License, PyPI version, Python version, downloads, CI, coverage
- `python_cli` - License, PyPI version, Python version, stars, last commit
- `node_package` - License, npm version, downloads, node version, CI
- `web_app` - License, stars, issues, last commit, CI
- `api` - License, CI, coverage, issues
- `github_standard` - License, stars, forks, issues, last commit

## Development

### Prerequisites

- Python 3.8+
- Poetry

### Setup

```bash
# Clone the repository
git clone https://github.com/southpawriter02/readme-forge.git
cd readme-forge

# Install dependencies
poetry install

# Run the CLI
poetry run readme-forge --help

# Run the TUI
poetry run readme-forge tui
```

### Project Structure

```
readme-forge/
├── src/readme_forge/
│   ├── __init__.py      # Package exports
│   ├── main.py          # CLI implementation
│   ├── tui.py           # TUI implementation
│   ├── templates.py     # Template management
│   ├── git_utils.py     # Git integration
│   ├── badges.py        # Badge generation
│   └── licenses.py      # License generation
├── roadmap/             # Feature roadmap
├── pyproject.toml       # Project configuration
└── README.md            # This file
```

## Roadmap

- [x] Interactive CLI with rich output
- [x] TUI interface with Textual
- [x] Git integration
- [x] Multiple templates
- [x] Badge generation
- [x] License file generation
- [ ] GitHub API integration for enhanced project info
- [ ] VS Code extension
- [ ] Custom template support
- [ ] CONTRIBUTING.md generation
- [ ] CHANGELOG generation

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Rich](https://github.com/Textualize/rich) - Beautiful terminal formatting
- [Textual](https://github.com/Textualize/textual) - TUI framework
- [Click](https://click.palletsprojects.com/) - CLI framework
- [Jinja2](https://jinja.palletsprojects.com/) - Template engine
- [GitPython](https://gitpython.readthedocs.io/) - Git integration
