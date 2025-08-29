"""
Test script to demonstrate web search functionality.
This script shows how the Tavily search tool works.
"""

import os
from langchain_tavily import TavilySearch

def test_search():
    """Test the Tavily search functionality."""
    
    # Check if Tavily API key is available
    tavily_key = os.getenv("TAVILY_API_KEY")
    if not tavily_key:
        print("❌ TAVILY_API_KEY not found in environment variables")
        print("   To test web search, add your Tavily API key to the .env file")
        print("   Get a free API key from: https://tavily.com/")
        return
    
    print("🔍 Testing Tavily web search...")
    
    # Initialize the search tool
    tool = TavilySearch(max_results=2)
    
    # Test search query
    query = "latest family meal planning trends 2024"
    print(f"Searching for: '{query}'")
    
    try:
        results = tool.invoke(query)
        print("\n✅ Search successful!")
        print(f"Found {len(results['results'])} results:")
        
        for i, result in enumerate(results['results'], 1):
            print(f"\n{i}. {result['title']}")
            print(f"   URL: {result['url']}")
            print(f"   Content: {result['content'][:200]}...")
            
    except Exception as e:
        print(f"❌ Search failed: {e}")

if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    test_search()
