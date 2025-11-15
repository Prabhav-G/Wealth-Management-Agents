"""
Linkup Client for Web Searching
Used to find investment strategies and market information
"""
import os
import requests
from typing import Dict, List, Optional
import json

_linkup_client = None
_linkup_initialized = False

def _initialize_linkup():
    """Initialize Linkup client (called lazily on first use)."""
    global _linkup_client, _linkup_initialized
    
    if _linkup_initialized:
        return
    
    LINKUP_API_KEY = os.getenv("LINKUP_API_KEY")
    LINKUP_BASE_URL = os.getenv("LINKUP_BASE_URL", "https://api.linkup.com/v1")
    
    if not LINKUP_API_KEY:
        raise ValueError(
            "FATAL: LINKUP_API_KEY not found in environment variables.\n"
            "Make sure to:\n"
            "1. Create a .env file with: LINKUP_API_KEY=your_key_here\n"
            "2. Optionally set LINKUP_BASE_URL if using a custom endpoint"
        )
    
    try:
        _linkup_client = {
            "api_key": LINKUP_API_KEY,
            "base_url": LINKUP_BASE_URL,
            "headers": {
                "Authorization": f"Bearer {LINKUP_API_KEY}",
                "Content-Type": "application/json"
            }
        }
        _linkup_initialized = True
        print("✓ Linkup client initialized successfully.")
    except Exception as e:
        print(f"✗ FATAL: Failed to initialize Linkup client. Error: {e}")
        raise

def get_linkup_client():
    """Get the Linkup client configuration (initializes on first call)."""
    if not _linkup_initialized:
        _initialize_linkup()
    return _linkup_client

class LinkupSearchClient:
    """Client for web searching investment strategies and market data."""
    
    def __init__(self):
        self.client = get_linkup_client()
        self.base_url = self.client["base_url"]
        self.headers = self.client["headers"]
    
    def search(self, query: str, max_results: int = 10, filters: Optional[Dict] = None) -> List[Dict]:
        """
        Search the web for investment strategies and information.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            filters: Optional filters (e.g., {"domain": "finance", "date_range": "2024"})
        
        Returns:
            List of search results with title, url, snippet, etc.
        """
        endpoint = f"{self.base_url}/search"
        
        payload = {
            "query": query,
            "max_results": max_results
        }
        
        if filters:
            payload["filters"] = filters
        
        try:
            response = requests.post(
                endpoint,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            return data.get("results", [])
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Linkup search error: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"  Response: {e.response.text}")
            # Return empty results on error rather than crashing
            return []
    
    def search_investment_strategies(self, risk_tolerance: str, investment_timeline: str, portfolio_value: float) -> List[Dict]:
        """
        Search for investment strategies based on user profile.
        
        Args:
            risk_tolerance: User's risk tolerance (conservative, moderate, aggressive)
            investment_timeline: Investment timeline (e.g., "15 years")
            portfolio_value: Current portfolio value
        
        Returns:
            List of relevant investment strategy results
        """
        query = f"investment strategies for {risk_tolerance} risk tolerance {investment_timeline} timeline portfolio value ${portfolio_value:,.0f}"
        
        filters = {
            "category": "investment_strategy",
            "risk_level": risk_tolerance.lower()
        }
        
        return self.search(query, max_results=10, filters=filters)
    
    def search_market_trends(self, sector: Optional[str] = None) -> List[Dict]:
        """
        Search for current market trends and analysis.
        
        Args:
            sector: Optional sector to focus on (e.g., "technology", "healthcare")
        
        Returns:
            List of market trend results
        """
        query = "current market trends investment analysis 2024"
        if sector:
            query += f" {sector} sector"
        
        filters = {
            "category": "market_analysis",
            "date_range": "2024"
        }
        
        return self.search(query, max_results=10, filters=filters)
    
    def search_tax_strategies(self, tax_bracket: str, state: Optional[str] = None) -> List[Dict]:
        """
        Search for tax optimization strategies.
        
        Args:
            tax_bracket: User's tax bracket (e.g., "24%")
            state: Optional state for state-specific strategies
        
        Returns:
            List of tax strategy results
        """
        query = f"tax optimization strategies {tax_bracket} tax bracket"
        if state:
            query += f" {state}"
        
        filters = {
            "category": "tax_strategy"
        }
        
        return self.search(query, max_results=10, filters=filters)

def get_linkup_search_client():
    """Get a Linkup search client instance."""
    return LinkupSearchClient()

