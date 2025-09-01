# Athena AI Assistant - Project Context for Claude

## Project Overview
Athena is a family life planning AI assistant built with LangGraph Platform. It provides intelligent assistance for meal planning, scheduling, and family activities.

## Key Technical Details

### Model Configuration
- **IMPORTANT**: Use `gemini-2.5-flash` model (not 2.0 or 1.5)
- Model is configured in `athena_agent/agent.py`

- **IMPORTANT** If we agree an approach and it fails do not default to a "simpler approach" before attempting to resolve the original approach.

### API Keys Required
- Google Gemini API Key (for LLM)
- Tavily API Key (for web search)
- Mem0 API Key (for persistent memory)
- All keys are stored in `.env` file

### Project Structure
```
Athena_AI_Assistant_LangGraph/
├── athena_agent/
│   └── agent.py           # Main LangGraph agent
├── .venv/                 # Virtual environment
├── .env                   # API keys
├── config.py             # Configuration loader
├── context_utils.py      # Time/date/location utilities
├── langgraph.json        # LangGraph Platform config
├── chat.html             # Simple web interface
└── start.py              # Server starter script
```

### How to Run
1. Activate virtual environment: `.\.venv\Scripts\activate`
2. Start server: `python start.py` or `langgraph dev`
3. Open `chat.html` in browser

### Current Issues & Solutions
- **Weather queries not working**: Fixed by adding explicit tool instructions in system prompt
- **Chat interface not showing responses**: Need to parse `messages/partial` events in SSE stream

### Important Notes
- Always activate the virtual environment before running commands
- The project uses LangGraph Platform (not vanilla LangChain)
- Server runs on port 2024
- Athena should use Tavily search tool for getting up to date information.

## Development Guidelines
- Keep the project structure neat and as simple as possible for easy maintenance.
- Group test scripts away from other files in a "test scripts" folder
- Keep the interface simple and accessible
- Focus on family-oriented features
- Ensure tools are properly configured and documented in system prompt
- Test with virtual environment activated