import httpx
from typing import Dict, Any, Optional
from inc.config import config

# https://apihub.us.document360.io/v2/Articles/eff2a758-82a7-4dd0-a7c7-0a9ad04881d0/en?isForDisplay=false&isPublished=false&appendSASToken=true

class Document360APIError(Exception):
    """Custom exception for Document360 API errors"""
    def __init__(self, message: str, status_code: int = None, error_code: str = None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.message)

class Document360Client:
    """Async HTTP client for Document360 API"""
    
    def __init__(self):
        self.client = httpx.AsyncClient(
            timeout=config.timeout,
            headers=config.headers
        )
    
    async def _request(self, method: str, endpoint: str) -> Dict[str, Any]:
        """Make HTTP request to Document360 API using v2 by default."""
        url = f"{config.base_url}/v2{endpoint}"
        
        try:
            response = await self.client.request(method, url)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                raise Document360APIError("Unauthorized: Invalid API key", 401, "UNAUTHORIZED")
            elif response.status_code == 404:
                raise Document360APIError("Resource not found", 404, "NOT_FOUND")
            elif response.status_code == 429:
                raise Document360APIError("Rate limit exceeded", 429, "RATE_LIMIT")
            else:
                try:
                    error_data = response.json()
                    error_message = error_data.get("message", "Unknown error")
                    error_code = error_data.get("errorCode", "UNKNOWN")
                    raise Document360APIError(error_message, response.status_code, error_code)
                except Exception:
                    raise Document360APIError(
                        f"HTTP {response.status_code}: {response.text}", 
                        response.status_code
                    )
                    
        except httpx.RequestError as e:
            raise Document360APIError(f"Request failed: {str(e)}")
    
    async def get_category(self, category_id: str) -> Dict[str, Any]:
        """Get category by ID"""
        return await self._request("GET", f"/categories/{category_id}")
    
    async def get_category_page_content(self, category_id: str, page_id: str) -> Dict[str, Any]:
        """Get category page content by ID"""
        return await self._request("GET", f"/categories/{category_id}/pages/{page_id}/content")
    
    async def get_article(self, article_id: str) -> Dict[str, Any]:
        """Get article by ID"""
        return await self._request("GET", f"/Articles/{article_id}/{config.langcode}?isForDisplay=false&isPublished={config.only_published}")
    
    async def list_project_versions(self) -> Dict[str, Any]:
        """Get list of all project versions"""
        return await self._request("GET", "/ProjectVersions")
    
    # async def list_categories_in_project_version(self, project_version_id: str) -> Dict[str, Any]:
    #     """Get list of categories within a project version"""
    #     return await self._request("GET", f"/ProjectVersions/{project_version_id}/categories")
    
    # async def list_articles_in_project_version(self, project_version_id: str) -> Dict[str, Any]:
    #     """Get list of articles within a project version"""
    #     return await self._request("GET", f"/ProjectVersions/{project_version_id}/articles?langCode={config.langcode}")

    async def search_project_version(self, project_version_id: str) -> Dict[str, Any]:
        """Search inside a project version (returns hits and metadata)

        Uses the /v2/ProjectVersions/{projectVersionId}/{langCode} endpoint which returns
        search hits (articles/categories) for the given project version.
        """
        return await self._request("GET", f"/ProjectVersions/{project_version_id}/{config.langcode}")
    
    # async def list_articles_in_category(self, project_version_id: str, category_slug_or_id: str) -> Dict[str, Any]:
    #     """Get list of articles within a specific category
        
    #     Args:
    #         project_version_id: The project version ID
    #         category_slug_or_id: Category slug or ID to filter by
            
    #     Returns:
    #         Filtered list of articles in the specified category
    #     """
    #     # Get all articles in project version
    #     articles_response = await self.list_articles_in_project_version(project_version_id)
    #     articles = articles_response.get('data', [])
        
    #     # Get categories to map slug to ID if needed
    #     categories_response = await self.list_categories_in_project_version(project_version_id)
    #     categories = categories_response.get('data', [])
        
    #     # Find category ID if slug was provided
    #     target_category_id = category_slug_or_id
    #     for category in categories:
    #         if category.get('slug', '').lower() == category_slug_or_id.lower():
    #             target_category_id = category.get('id')
    #             break
        
    #     # Filter articles by category
    #     filtered_articles = [
    #         article for article in articles 
    #         if article.get('category_id') == target_category_id
    #     ]
        
    #     return {
    #         'data': filtered_articles,
    #         'success': True,
    #         'category_id': target_category_id
    #     }
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()

# Global client instance
client = Document360Client()