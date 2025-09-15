from fastmcp import Context
from typing import Dict, Any
from inc.document360_client import client, Document360APIError

async def get_category_page_content(category_id: str, page_id: str, ctx: Context) -> Dict[str, Any]:
    """Get category page content by ID from Document360
    
    Args:
        category_id: The Document360 category ID
        page_id: The Document360 page ID
        ctx: MCP context for logging and error handling
        
    Returns:
        Page content data from Document360 API
    """
    try:
        await ctx.info(f"Fetching content for page {page_id} from category {category_id}")
        
        result = await client.get_category_page_content(category_id, page_id)
        
        await ctx.info("Successfully retrieved page content")
        return result
        
    except Document360APIError as e:
        await ctx.error(f"Document360 API error: {e.message}")
        if e.status_code == 404:
            await ctx.warning(f"Page content {page_id} in category {category_id} not found")
        elif e.status_code == 401:
            await ctx.error("Invalid API key - check configuration")
        raise e
    except Exception as e:
        await ctx.error(f"Unexpected error fetching page content: {str(e)}")
        raise e

async def get_article(article_id: str, ctx: Context) -> Dict[str, Any]:
    """Get article by ID from Document360
    
    Args:
        article_id: The Document360 article ID
        ctx: MCP context for logging and error handling
        
    Returns:
        Article data from Document360 API
    """
    try:
        await ctx.info(f"Fetching article with ID: {article_id}")
        
        result = await client.get_article(article_id)
        
        await ctx.info(f"Successfully retrieved article: {result.get('data', {}).get('title', 'Unknown')}")
        return result
        
    except Document360APIError as e:
        await ctx.error(f"Document360 API error: {e.message}")
        if e.status_code == 404:
            await ctx.warning(f"Article {article_id} not found")
        elif e.status_code == 401:
            await ctx.error("Invalid API key - check configuration")
        raise e
    except Exception as e:
        await ctx.error(f"Unexpected error fetching article: {str(e)}")
        raise e


async def search_in_project(project_version_id: str, ctx: Context) -> Dict[str, Any]:
    """Search inside a project version and return hits

    Args:
        project_version_id: The project version ID to search in
        ctx: MCP context for logging

    Returns:
        The raw response from /v2/ProjectVersions/{projectVersionId}/{langCode}, typically contains 'data.hits'
    """
    try:
        await ctx.info(f"Searching in project version: {project_version_id}")

        result = await client.search_project_version(project_version_id)

        hits = result.get('data', {}).get('hits', [])

        await ctx.info(f"Found {len(hits)} hits in project version {project_version_id}")
        return {'data': hits, 'success': True}

    except Document360APIError as e:
        await ctx.error(f"Document360 API error during project search: {e.message}")
        raise e
    except Exception as e:
        await ctx.error(f"Unexpected error during project search: {str(e)}")
        raise e
        
async def get_category(category_id: str, ctx: Context) -> Dict[str, Any]:
    """Get category by ID from Document360
    
    Args:
        category_id: The Document360 category ID
        ctx: MCP context for logging and error handling
        
    Returns:
        Category data from Document360 API
    """
    try:
        await ctx.info(f"Fetching category with ID: {category_id}")
        
        result = await client.get_category(category_id)
        
        await ctx.info("Successfully retrieved category")
        return result
        
    except Document360APIError as e:
        await ctx.error(f"Document360 API error: {e.message}")
        if e.status_code == 404:
            await ctx.warning(f"Category {category_id} not found")
        elif e.status_code == 401:
            await ctx.error("Invalid API key - check configuration")
        raise e
    except Exception as e:
        await ctx.error(f"Unexpected error fetching category: {str(e)}")
        raise e

async def list_project_versions(ctx: Context) -> Dict[str, Any]:
	try:
		await ctx.info("Listing all project versions")
		result = await client.list_project_versions()
		await ctx.info(f"Found {len(result.get('data', []))} project versions")
		return result
	except Document360APIError as e:
		await ctx.error(f"Document360 API error: {e.message}")
		raise e
	except Exception as e:
		await ctx.error(f"Unexpected error listing project versions: {str(e)}")
		raise e
