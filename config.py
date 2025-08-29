import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Google Gemini API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Tavily Search API Key (for web search capabilities)
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# LangSmith configuration (optional)
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "athena-family-assistant")

# Validate required API keys
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable is required. Please set it in your .env file.")

if not TAVILY_API_KEY:
    print("⚠️  Warning: TAVILY_API_KEY not found. Web search capabilities will be disabled.")
    print("   Get your free API key from: https://tavily.com/")
