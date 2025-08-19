# Feature: License Generation

## 1. Summary

This feature integrates automatic license text generation into the CLI tool. It will allow users to select a standard open-source license, and the tool will automatically fetch the correct text and add it to the `README.md` and/or a separate `LICENSE` file.

## 2. Intended Functionality

*   **License Selection Prompt:** The CLI tool will prompt the user to choose a license from a list of common open-source licenses (e.g., MIT, GPLv3, Apache 2.0).
*   **License Text Fetching:** The tool will use a library or an API to fetch the full text of the selected license.
*   **File Generation:**
    *   A `LICENSE` file will be created in the project's root directory containing the full license text.
    *   A "License" section will be added to the `README.md` with a brief summary and a link to the `LICENSE` file. For example: "This project is licensed under the MIT License - see the `LICENSE` file for details."
*   **Author/Year Placeholders:** The tool will automatically replace placeholders like `[year]` and `[fullname]` in the license text with the current year and the author's name (as provided in an earlier prompt).

## 3. Requirements

*   **License Data Source:** The tool needs a reliable source for license texts. This could be:
    *   A local database of license texts.
    *   An API like the GitHub API for licenses.
    *   A dedicated library like `spdx-license-list` (for license metadata) or `license` (for full texts).
*   **File I/O:** The tool must be able to create the `LICENSE` file and write the license text to it.

## 4. Limitations

*   **Limited License Selection:** The tool will not support every possible license in the world. It will be limited to a curated list of the most popular and widely used licenses.
*   **No Legal Advice:** The tool will not provide legal advice. It is up to the user to understand the implications of the license they choose. A disclaimer to this effect should be included in the tool's output.

## 5. Dependencies

*   **Node.js:**
    *   `spdx-license-list`: To get a list of valid SPDX license identifiers.
    *   `node-fetch` or `axios`: To fetch license texts from an API.
*   **Python:**
    *   `requests`: To fetch license texts from an API.
    *   A suitable library for license data, or a custom implementation.
