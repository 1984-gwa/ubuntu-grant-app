# Ubuntu Grant Finder

A Streamlit web app to search for grants, generate proposals, and contact the team.

## Features

- **Grant Search**: Find grants by title, summary, or source.
- **Proposal Generator**: Create and download grant proposals as PDFs.
- **Contact Form**: Send messages to the team.

## Usage

1. Clone the repository and install requirements:
    ```bash
    pip install -r requirements.txt
    ```

2. Add your `grants.csv` file in the root directory (see format below).

3. Run the app:
    ```bash
    streamlit run app.py
    ```

## `grants.csv` Format

| title | url | source | summary |
|-------|-----|--------|---------|
| Example Grant | https://example.com | Example Foundation | Funding for innovative Ubuntu projects. |

## Contribution

PRs and issues welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License