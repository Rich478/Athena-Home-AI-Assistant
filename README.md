# Athena AI Family Life Planning Assistant

An intelligent AI assistant built with LangGraph and Google Gemini 2.5 to help you plan and organize your family's life.

## Features

- 🤖 **Intelligent Conversations**: Powered by Google Gemini 2.5 for natural, helpful responses
- 🔍 **Web Search**: Real-time information retrieval using Tavily search engine
- 🏠 **Family-Focused**: Designed specifically for family life planning and organization
- 🔄 **Stateful Conversations**: Maintains context across conversation turns
- 📊 **Monitoring**: Optional LangSmith integration for debugging and performance tracking

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- Optional: Tavily Search API key for web search ([Get one here](https://tavily.com/))
- Optional: LangSmith API key for monitoring ([Sign up here](https://smith.langchain.com/))

## Installation

1. **Clone or download this project**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API keys**:
   Create a `.env` file in the project root with your API keys:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   LANGSMITH_API_KEY=your_langsmith_api_key_here
   LANGSMITH_PROJECT=athena-family-assistant
   ```

## Usage

Run the basic chatbot:
```bash
python basic_chatbot.py
```

Run the enhanced chatbot with web search:
```bash
python chatbot_with_tools.py
```

The assistant will greet you and you can start asking questions about family planning, organization, scheduling, and more!

## Example Conversations

You can ask Athena about:
- Family schedule planning
- Meal planning and grocery lists
- Household organization tips
- Family goal setting
- Budget planning
- Activity suggestions for different ages
- Current events and news (with web search enabled)
- Latest parenting trends and research
- Local events and activities
- And much more!

## Project Structure

```
├── basic_chatbot.py        # Basic chatbot implementation
├── chatbot_with_tools.py   # Enhanced chatbot with web search
├── config.py              # Configuration and environment setup
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── .env                  # Your API keys (create this file)
```

## Next Steps

This is the basic implementation following the [LangGraph tutorial](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/). Future enhancements could include:

- Adding tools for calendar integration
- Web search capabilities
- Memory for persistent family information
- Custom family profiles
- Task management features
- Budget tracking tools

## Troubleshooting

- **API Key Error**: Make sure your `GOOGLE_API_KEY` is correctly set in the `.env` file
- **Import Errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`
- **LangSmith Issues**: LangSmith is optional - the chatbot will work without it

## Contributing

Feel free to enhance this assistant with additional features specific to your family's needs!

## License

This project is for personal use and learning purposes.
