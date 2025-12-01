"""
TUI (Text User Interface) for readme-forge using Textual.
Provides an interactive terminal-based GUI for generating README files.
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import (
    Header,
    Footer,
    Static,
    Button,
    Input,
    Select,
    TextArea,
    Label,
    TabbedContent,
    TabPane,
    Markdown,
    ListView,
    ListItem,
    Checkbox,
    Rule,
    LoadingIndicator,
)
from textual.binding import Binding
from textual.screen import Screen, ModalScreen
from textual.message import Message
from textual import on
from textual.reactive import reactive

import json
import os
from typing import Dict, Any, Optional, List

from .templates import get_template_names, get_template_descriptions, render_template
from .git_utils import detect_git_info, detect_project_type, get_suggested_context
from .badges import generate_badges_from_preset, badges_to_markdown, BADGE_PRESETS
from .licenses import get_license_names, save_license_file, get_license_badge_name


class PreviewScreen(ModalScreen):
    """Modal screen for previewing the README."""

    BINDINGS = [
        Binding("escape", "dismiss", "Close"),
        Binding("s", "save", "Save"),
    ]

    def __init__(self, content: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.content = content

    def compose(self) -> ComposeResult:
        yield Container(
            Static("README Preview", id="preview-title"),
            ScrollableContainer(
                Markdown(self.content, id="preview-content"),
                id="preview-scroll"
            ),
            Horizontal(
                Button("Save", id="save-btn", variant="success"),
                Button("Close", id="close-btn", variant="default"),
                id="preview-buttons"
            ),
            id="preview-container"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save-btn":
            self.dismiss(True)
        else:
            self.dismiss(False)

    def action_dismiss(self) -> None:
        self.dismiss(False)

    def action_save(self) -> None:
        self.dismiss(True)


class FeatureInput(Static):
    """Widget for inputting features."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.features: List[str] = []

    def compose(self) -> ComposeResult:
        yield Label("Features (one per line):")
        yield TextArea(id="features-input")

    def get_features(self) -> List[str]:
        text_area = self.query_one("#features-input", TextArea)
        text = text_area.text
        return [f.strip() for f in text.split("\n") if f.strip()]


class ProjectInfoForm(Static):
    """Form for project information."""

    def compose(self) -> ComposeResult:
        yield Label("Project Name:", classes="form-label")
        yield Input(placeholder="my-awesome-project", id="project-name")

        yield Label("Description:", classes="form-label")
        yield TextArea(id="project-description")

        yield Label("GitHub Username:", classes="form-label")
        yield Input(placeholder="username", id="github-username")

        yield Label("Author Name:", classes="form-label")
        yield Input(placeholder="Your Name", id="author-name")

        yield Label("Author Email (optional):", classes="form-label")
        yield Input(placeholder="email@example.com", id="author-email")

        yield Label("License:", classes="form-label")
        yield Select(
            [(name, name) for name in get_license_names() + ["None"]],
            id="license-select",
            value="MIT"
        )

    def get_data(self) -> Dict[str, str]:
        return {
            "project_name": self.query_one("#project-name", Input).value,
            "project_description": self.query_one("#project-description", TextArea).text,
            "github_username": self.query_one("#github-username", Input).value,
            "author_name": self.query_one("#author-name", Input).value,
            "author_email": self.query_one("#author-email", Input).value,
            "license": self.query_one("#license-select", Select).value,
        }

    def set_data(self, data: Dict[str, Any]) -> None:
        if data.get("project_name"):
            self.query_one("#project-name", Input).value = data["project_name"]
        if data.get("project_description"):
            self.query_one("#project-description", TextArea).text = data["project_description"]
        if data.get("github_username"):
            self.query_one("#github-username", Input).value = data["github_username"]
        if data.get("author_name"):
            self.query_one("#author-name", Input).value = data["author_name"]
        if data.get("author_email"):
            self.query_one("#author-email", Input).value = data["author_email"]


class InstallationForm(Static):
    """Form for installation and usage information."""

    def compose(self) -> ComposeResult:
        yield Label("Installation Command:", classes="form-label")
        yield Input(placeholder="pip install my-package", id="install-cmd")

        yield Label("Usage Instructions:", classes="form-label")
        yield TextArea(id="usage-instructions")

        yield Label("Code Language:", classes="form-label")
        yield Select(
            [
                ("Python", "python"),
                ("Bash", "bash"),
                ("JavaScript", "javascript"),
                ("TypeScript", "typescript"),
                ("Go", "go"),
                ("Rust", "rust"),
                ("Java", "java"),
            ],
            id="code-language",
            value="python"
        )

    def get_data(self) -> Dict[str, str]:
        return {
            "installation_instructions": self.query_one("#install-cmd", Input).value,
            "usage_instructions": self.query_one("#usage-instructions", TextArea).text,
            "code_language": self.query_one("#code-language", Select).value,
        }

    def set_data(self, data: Dict[str, Any]) -> None:
        if data.get("installation_instructions"):
            self.query_one("#install-cmd", Input).value = data["installation_instructions"]
        if data.get("usage_instructions"):
            self.query_one("#usage-instructions", TextArea).text = data["usage_instructions"]


class TemplateSelector(Static):
    """Widget for selecting a template."""

    def compose(self) -> ComposeResult:
        yield Label("Template:", classes="form-label")
        templates = get_template_descriptions()
        yield Select(
            [(f"{name} - {desc}", name) for name, desc in templates.items()],
            id="template-select",
            value="standard"
        )

        yield Label("Badge Preset:", classes="form-label")
        presets = ["none"] + list(BADGE_PRESETS.keys())
        yield Select(
            [(p, p) for p in presets],
            id="badge-preset",
            value="github_standard"
        )

    def get_template(self) -> str:
        return self.query_one("#template-select", Select).value

    def get_badge_preset(self) -> str:
        return self.query_one("#badge-preset", Select).value


class StatusBar(Static):
    """Status bar widget."""

    status = reactive("Ready")

    def render(self) -> str:
        return f"Status: {self.status}"


class ReadmeForgeApp(App):
    """The main readme-forge TUI application."""

    CSS = """
    Screen {
        background: $surface;
    }

    #main-container {
        width: 100%;
        height: 100%;
    }

    #sidebar {
        width: 30;
        background: $panel;
        border-right: solid $primary;
        padding: 1;
    }

    #content {
        width: 1fr;
        padding: 1;
    }

    #preview-pane {
        width: 1fr;
        background: $panel;
        border-left: solid $primary;
        padding: 1;
    }

    .form-label {
        margin-top: 1;
        color: $text;
    }

    Input, TextArea, Select {
        margin-bottom: 1;
    }

    TextArea {
        height: 5;
    }

    #features-input {
        height: 8;
    }

    #preview-content {
        background: $surface;
        padding: 1;
    }

    #button-bar {
        dock: bottom;
        height: 3;
        background: $panel;
        padding: 0 1;
    }

    #button-bar Button {
        margin-right: 1;
    }

    #status-bar {
        dock: bottom;
        height: 1;
        background: $primary-darken-3;
        color: $text;
        padding: 0 1;
    }

    #git-info {
        background: $panel;
        padding: 1;
        margin-bottom: 1;
        border: solid $primary;
    }

    #git-info-title {
        text-style: bold;
        margin-bottom: 1;
    }

    TabPane {
        padding: 1;
    }

    /* Preview Modal Styles */
    PreviewScreen {
        align: center middle;
    }

    #preview-container {
        width: 90%;
        height: 90%;
        background: $surface;
        border: thick $primary;
        padding: 1;
    }

    #preview-title {
        text-style: bold;
        text-align: center;
        margin-bottom: 1;
    }

    #preview-scroll {
        height: 1fr;
        border: solid $primary;
        background: $panel;
    }

    #preview-buttons {
        margin-top: 1;
        align: center middle;
    }

    #preview-buttons Button {
        margin: 0 1;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("g", "generate", "Generate"),
        Binding("p", "preview", "Preview"),
        Binding("s", "save_config", "Save Config"),
        Binding("l", "load_config", "Load Config"),
        Binding("d", "detect_git", "Detect Git"),
        Binding("f1", "help", "Help"),
    ]

    TITLE = "readme-forge"
    SUB_TITLE = "Generate beautiful READMEs"

    def __init__(self):
        super().__init__()
        self.context: Dict[str, Any] = {}
        self.git_info = None
        self.preview_content = ""

    def compose(self) -> ComposeResult:
        yield Header()

        with Horizontal(id="main-container"):
            with Vertical(id="sidebar"):
                yield Static("Quick Actions", classes="section-title")
                yield Button("Detect Git Info", id="detect-git-btn", variant="primary")
                yield Button("Load Config", id="load-config-btn")
                yield Button("Save Config", id="save-config-btn")
                yield Rule()
                yield Static("Generation", classes="section-title")
                yield Button("Preview", id="preview-btn", variant="warning")
                yield Button("Generate README", id="generate-btn", variant="success")
                yield Button("Generate License", id="license-btn")

            with ScrollableContainer(id="content"):
                yield Static("", id="git-info")

                with TabbedContent():
                    with TabPane("Project Info", id="tab-project"):
                        yield ProjectInfoForm(id="project-form")

                    with TabPane("Install & Usage", id="tab-install"):
                        yield InstallationForm(id="install-form")

                    with TabPane("Features", id="tab-features"):
                        yield FeatureInput(id="feature-form")

                    with TabPane("Template", id="tab-template"):
                        yield TemplateSelector(id="template-form")

        yield StatusBar(id="status-bar")
        yield Footer()

    def on_mount(self) -> None:
        """Initialize the app on mount."""
        self.update_status("Ready - Press 'd' to detect git info or start filling in the form")
        # Auto-detect git info on startup
        self.detect_git_info()

    def update_status(self, message: str) -> None:
        """Update the status bar."""
        status_bar = self.query_one("#status-bar", StatusBar)
        status_bar.status = message

    def detect_git_info(self) -> None:
        """Detect and display git information."""
        self.update_status("Detecting git information...")

        self.git_info = detect_git_info()
        project_type = detect_project_type()

        git_info_widget = self.query_one("#git-info", Static)

        if self.git_info.is_git_repo:
            info_text = "[bold]Detected Git Information[/bold]\n\n"
            if self.git_info.project_name:
                info_text += f"Project: {self.git_info.project_name}\n"
            if self.git_info.github_username:
                info_text += f"GitHub User: {self.git_info.github_username}\n"
            if self.git_info.license_type:
                info_text += f"License: {self.git_info.license_type}\n"
            if self.git_info.languages:
                info_text += f"Languages: {', '.join(self.git_info.languages)}\n"
            info_text += f"Project Type: {project_type}"

            git_info_widget.update(info_text)

            # Pre-fill forms with detected info
            suggested = get_suggested_context(self.git_info, project_type)
            self.prefill_forms(suggested)

            self.update_status("Git info detected - Forms pre-filled with detected values")
        else:
            git_info_widget.update("[yellow]Not a git repository[/yellow]")
            self.update_status("Not a git repository - Please fill in the form manually")

    def prefill_forms(self, data: Dict[str, Any]) -> None:
        """Pre-fill forms with data."""
        project_form = self.query_one("#project-form", ProjectInfoForm)
        project_form.set_data(data)

        install_form = self.query_one("#install-form", InstallationForm)
        install_form.set_data(data)

    def collect_all_data(self) -> Dict[str, Any]:
        """Collect all data from forms."""
        project_form = self.query_one("#project-form", ProjectInfoForm)
        install_form = self.query_one("#install-form", InstallationForm)
        feature_form = self.query_one("#feature-form", FeatureInput)
        template_form = self.query_one("#template-form", TemplateSelector)

        context = {}
        context.update(project_form.get_data())
        context.update(install_form.get_data())

        features = feature_form.get_features()
        if features:
            context["features"] = features

        # Generate badges
        badge_preset = template_form.get_badge_preset()
        if badge_preset != "none":
            badges = generate_badges_from_preset(
                badge_preset,
                username=context.get("github_username", ""),
                repo=context.get("project_name", ""),
                package=context.get("project_name", ""),
                license=get_license_badge_name(context.get("license", "MIT")),
            )
            context["badges"] = badges_to_markdown(badges)

        return context

    def generate_preview(self) -> str:
        """Generate README preview."""
        context = self.collect_all_data()
        template_form = self.query_one("#template-form", TemplateSelector)
        template = template_form.get_template()

        return render_template(template, context)

    async def action_preview(self) -> None:
        """Show preview of README."""
        self.update_status("Generating preview...")
        content = self.generate_preview()

        result = await self.push_screen(PreviewScreen(content), wait_for_dismiss=True)
        if result:
            self.save_readme(content)

    async def action_generate(self) -> None:
        """Generate the README file."""
        self.update_status("Generating README...")
        content = self.generate_preview()
        self.save_readme(content)

    def save_readme(self, content: str) -> None:
        """Save README to file."""
        try:
            with open("README.md", "w") as f:
                f.write(content)
            self.update_status("README.md generated successfully!")
            self.notify("README.md generated!", title="Success", severity="information")
        except Exception as e:
            self.update_status(f"Error: {e}")
            self.notify(f"Error: {e}", title="Error", severity="error")

    def action_save_config(self) -> None:
        """Save current configuration."""
        context = self.collect_all_data()

        # Remove non-serializable items
        serializable = {k: v for k, v in context.items()
                       if isinstance(v, (str, int, float, bool, list, dict))}

        try:
            with open("readme-forge.json", "w") as f:
                json.dump(serializable, f, indent=2)
            self.update_status("Configuration saved to readme-forge.json")
            self.notify("Configuration saved!", title="Success", severity="information")
        except Exception as e:
            self.update_status(f"Error saving config: {e}")
            self.notify(f"Error: {e}", title="Error", severity="error")

    def action_load_config(self) -> None:
        """Load configuration from file."""
        if not os.path.exists("readme-forge.json"):
            self.update_status("No configuration file found")
            self.notify("No readme-forge.json found", title="Warning", severity="warning")
            return

        try:
            with open("readme-forge.json", "r") as f:
                data = json.load(f)

            self.prefill_forms(data)
            self.update_status("Configuration loaded from readme-forge.json")
            self.notify("Configuration loaded!", title="Success", severity="information")
        except Exception as e:
            self.update_status(f"Error loading config: {e}")
            self.notify(f"Error: {e}", title="Error", severity="error")

    def action_detect_git(self) -> None:
        """Trigger git detection."""
        self.detect_git_info()

    def action_help(self) -> None:
        """Show help."""
        self.notify(
            "Keyboard shortcuts:\n"
            "g - Generate README\n"
            "p - Preview README\n"
            "s - Save config\n"
            "l - Load config\n"
            "d - Detect git info\n"
            "q - Quit",
            title="Help",
            severity="information"
        )

    @on(Button.Pressed, "#detect-git-btn")
    def handle_detect_git(self) -> None:
        self.detect_git_info()

    @on(Button.Pressed, "#load-config-btn")
    def handle_load_config(self) -> None:
        self.action_load_config()

    @on(Button.Pressed, "#save-config-btn")
    def handle_save_config(self) -> None:
        self.action_save_config()

    @on(Button.Pressed, "#preview-btn")
    async def handle_preview(self) -> None:
        await self.action_preview()

    @on(Button.Pressed, "#generate-btn")
    async def handle_generate(self) -> None:
        await self.action_generate()

    @on(Button.Pressed, "#license-btn")
    def handle_license(self) -> None:
        """Generate license file."""
        context = self.collect_all_data()
        license_id = context.get("license", "MIT")

        if license_id == "None":
            self.notify("No license selected", title="Warning", severity="warning")
            return

        author = context.get("author_name", context.get("github_username", ""))

        if save_license_file(license_id, author):
            self.update_status(f"LICENSE file generated ({license_id})")
            self.notify("LICENSE file generated!", title="Success", severity="information")
        else:
            self.update_status("Failed to generate LICENSE file")
            self.notify("Failed to generate LICENSE", title="Error", severity="error")


def main():
    """Run the TUI application."""
    app = ReadmeForgeApp()
    app.run()


if __name__ == "__main__":
    main()
