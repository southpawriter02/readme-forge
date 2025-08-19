# Feature: Interactive CLI Tool

## 1. Summary

The Interactive Command-Line Interface (CLI) Tool is the primary method for users to interact with `readme-forge`. This tool will guide users through a series of questions about their project and use their answers to populate the `README_TEMPLATE.md`, generating a polished `README.md` file tailored to their project.

## 2. Intended Functionality

*   **Interactive Prompts:** The CLI will present a series of questions to the user in an interactive, user-friendly manner. For example: "What is the name of your project?".
*   **Template Parsing:** The tool will read the `README_TEMPLATE.md` file.
*   **Placeholder Replacement:** It will replace the placeholders (e.g., `{{PROJECT_NAME}}`) in the template with the answers provided by the user.
*   **File Generation:** The tool will generate a new `README.md` file in the current directory (or a specified output directory).
*   **Configuration File:** The tool could optionally save the user's answers to a configuration file (e.g., `readme-forge.json`) to allow for easy regeneration of the README in the future.

## 3. Requirements

*   **Technology Stack:** The initial proposal suggests Node.js or Python.
    *   **Node.js:** Use a library like `inquirer` or `prompts` for the interactive prompts.
    *   **Python:** Use a library like `click` or `questionary` for the CLI and prompts.
*   **File I/O:** The tool must be able to read the template file and write the generated README file.
*   **Cross-Platform Compatibility:** The tool should be executable on Windows, macOS, and Linux.

## 4. Limitations

*   **No GUI:** This is a command-line only tool. A graphical user interface (GUI) is out of scope for this feature.
*   **Limited Validation:** The initial version of the tool may have limited input validation. For example, it might not check if a provided URL is valid.

## 5. Dependencies

*   **Node.js:**
    *   `inquirer` (or `prompts`)
    *   `fs-extra` (for file system operations)
*   **Python:**
    *   `click` (or `argparse`)
    *   `questionary`
    *   `jinja2` (for templating)
