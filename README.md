# Document360 MCP Server
A very simple Model Context Protocol (MCP) server for accessing Document360 knowledge base content via GET operations. Built with [FastMCP](https://gofastmcp.com/).
This MCP is intended to be the bare minimun required to be able to find and read pages in Document360's knowledge base.

## Features
- Get Category by ID
- Get Category Page Content by ID
- Get Article by ID
- Search in Project Versions
- List Project Versions

## Requirements
- Python 3.8+
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
        "PRODUCTIVE_ORGANIZATION": "https://apihub.document360.io"
      }
    }
  }
}
```

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
While there are more specific endpoints in the Document360 API, models seems to behave well with only these: they are able to discover project versions, categories and pages; and to read the page contents.

- **get_category_page_content**  
  Parameters: `category_id`, `page_id`

- **get_article**  
  Parameters: `article_id`

- **search_in_project**  
  Parameters: `project_version_id`

- **list_project_versions**
  Parameters: none

- **get_category**
  Parameters: `category_id`