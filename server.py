from fastmcp import FastMCP, Context
from inc.config import config
from inc.document360_client import client
import inc.tools as tools
import asyncio
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(server):
    """Server lifespan context manager"""
    # Startup
    if not config.validate():
        raise ValueError("Invalid configuration: API key and base URL are required")
    
    yield
    
    # Shutdown
    await client.close()

# Initialize FastMCP server
mcp = FastMCP(
    name="Document360 MCP Server",
    instructions="""
Use this server to access Document360 projects, categories and articles. Search and retrieves categories, articles and pages.
- If no project_version_id is provided in the context, search for relevant projects using `list_project_versions`. Inform the user if no relevant projects can be found
- If not article_id is provided, use `search_in_project` to find relevant articles, their IDs and contents
- While using `search_in_project` pay attention to relevant categoryIds, use `get_category` and `get_category_page_content` if you need to do a deep research on a particular topic
- If the user mentions a specific ID, prioritize it over `search_in_project`
- Provide the links to the relevant articles as resources
    """,
    lifespan=lifespan,
    # include_tags={"document360", "api"},
    on_duplicate_tools="warn",
    on_duplicate_resources="warn", 
    on_duplicate_prompts="warn"
)

@mcp.tool
async def get_category_page_content(category_id: str, page_id: str, ctx: Context) -> dict:
    """Get category page content by ID from Document360
    
    Args:
        category_id: The Document360 category ID (e.g., 'rtt2a758-82a7-4dd0-a7c7-0a9ad04881d0')
        page_id: The Document360 page ID (e.g., 'rtt2a758-82a7-4dd0-a7c7-0a9ad04881d0')
    
    Returns:
        Full page content including HTML/text content and formatting
    """
    return await tools.get_category_page_content(category_id, page_id, ctx)

@mcp.tool
async def get_article(article_id: str, ctx: Context) -> dict:
    """Get article by ID from Document360
    
    Args:
        article_id: The Document360 article ID (e.g., 'rtt2a758-82a7-4dd0-a7c7-0a9ad04881d0')
    
    Returns:
        Article information including title, content, tags, and metadata
    """
    return await tools.get_article(article_id, ctx)

@mcp.tool
async def search_in_project(project_version_id: str, ctx: Context) -> dict:
    """Search inside a project version and return related articles/categories in Document360

    Args:
        project_version_id: The project version ID

    Returns:
        List of hits (articles/categories) from the project version search endpoint
    """
    return await tools.search_in_project(project_version_id, ctx)

@mcp.tool
async def get_category(category_id: str, ctx: Context) -> dict:
    """Get category by ID from Document360
    
    Args:
        category_id: The Document360 category ID (e.g., 'rtt2a758-82a7-4dd0-a7c7-0a9ad04881d0')
    
    Returns:
        Category information including name, description, articles, and metadata
    """
    return await tools.get_category(category_id, ctx)

@mcp.tool
async def list_project_versions(ctx: Context) -> dict:
    """List all project versions from Document360

    Args:
        ctx: MCP context for logging and error handling

    Returns:
        List of project versions
    """
    return await tools.list_project_versions(ctx)

if __name__ == "__main__":
    mcp.run()