# Document360 MCP Server

Model Context Protocol server for Document360 that enables AI assistants to search, retrieve, and interact with your knowledge base. Built with [FastMCP](https://gofastmcp.com/), this server provides seamless access to Document360 articles, categories, and project versions through a standardized MCP interface.

<a href="https://glama.ai/mcp/servers/@druellan/document360-mcp">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@druellan/document360-mcp/badge" alt="Document360 MCP server" />
</a>

## Features
- Get Category by ID
- Get Category Page Content by ID
- Get Article by ID
- Search in Project Versions
- List Project Versions

## Requirements
- Python 3.12+
- Document360 API key

## Installation
Clone or download this repository, then install dependencies:

```bash
pip install -r requirements.txt
```

or using a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate.bat`
pip install -r requirements.txt
```

or using UV
```bash
uv venv
uv pip install -r requirements.txt
```

## Configuration
Set your Document360 API key and other environment variables. You can do this in your shell or directly in the `mcp-config.json` file:

```json
{
  "mcpServers": {
    "document360": {
      "command": "uv",
      "args": [
      "--directory", "/path/to/document360-mcp/folder", "run" ,"server.py"
      ],
      "env": {
        "DOCUMENT360_API_KEY": "your_api_key_here",
        "DOCUMENT360_BASE_URL": "https://apihub.document360.io"
      }
    }
  }
}
```

Note: the default base URL is `https://apihub.document360.io`, but some accounts require to use the regional base url `https://apihub.us.document360.io`.

## Usage
Run the server directly:
```bash
python server.py
```

Or with UV:
```bash
uv run server.py
```

## Exposed MCP Tools
Although Document360 exposes more granular endpoints, these are sufficient for a simple consumption workflow: models can discover project versions, enumerate categories and pages, and retrieve full page contents.

- **get_category_page_content**
  Parameters:
  - `category_id` (UUID string): Document360 category ID
  - `page_id` (UUID string): Document360 page ID

- **get_article**
  Parameters:
  - `article_id` (UUID string): Document360 article ID

- **search_in_project**
  Parameters:
  - `project_version_id` (UUID string): Document360 project version ID
  - `query` (string, optional): Free-text phrase searched across articles/categories by the Document360 backend
  - `hits_per_page` (int, optional, default 20): Maximum number of ranked results to return (1-1000)

- **list_project_versions**
  Parameters: none

- **get_category**
  Parameters:
  - `category_id` (UUID string): Document360 category ID

## License

MIT
