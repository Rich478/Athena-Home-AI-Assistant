# 🏛️ Athena AI Assistant - Your Intelligent Family Life Planning Companion

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2.0+-green.svg)
![Gemini](https://img.shields.io/badge/Google%20Gemini-2.0-red.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🌟 What is Athena?

Athena is your personal AI-powered family life planning assistant that helps you organize, plan, and enhance your family's daily life. Think of it as having a knowledgeable friend who remembers everything about your family's preferences, schedules, and needs - available 24/7 to help with planning, advice, and suggestions.

### 👨‍👩‍👧‍👦 Perfect For Families Who Want To:
- **Remember Everything**: Never forget important details about family members, preferences, or schedules
- **Plan Smarter**: Get intelligent suggestions for meals, activities, and schedules based on your family's unique needs
- **Stay Organized**: Keep track of everyone's activities, appointments, and responsibilities
- **Save Time**: Get quick answers and recommendations without searching through notes or calendars
- **Adapt and Learn**: The more you interact with Athena, the better she understands your family

## ✨ Key Features

### 🧠 **Persistent Memory**
Athena remembers your conversations and learns about your family over time:
- Family members' names, ages, and preferences
- Dietary restrictions and favorite foods
- Schedule patterns and activity preferences
- Important dates and recurring events

### 🌍 **Context-Aware Responses**
Athena understands your current situation:
- **Time-aware**: Provides relevant suggestions based on time of day (morning routines, dinner planning, bedtime activities)
- **Day-aware**: Differentiates between weekdays and weekends for appropriate recommendations
- **Location-aware**: Considers your location for local activity suggestions

### 🔍 **Web Search Integration**
Get up-to-date information for:
- Local events and activities
- Recipe ideas and nutritional information
- Educational resources
- Weather-appropriate suggestions

### 💬 **Natural Conversations**
Chat naturally with Athena like you would with a helpful friend:
- Ask questions in your own words
- Get personalized responses based on your family's context
- Receive proactive suggestions and reminders

## 🚀 Getting Started (Non-Technical Guide)

### What You'll Need:
1. **A Computer** with Windows, Mac, or Linux
2. **Python** installed (version 3.8 or newer)
3. **Internet Connection** for AI features
4. **API Keys** (like passwords for AI services) - we'll help you get these!

### Simple Setup Steps:

#### Step 1: Download Athena
```bash
# Download the project to your computer
git clone https://github.com/RichPM478/athena-ai-assistant.git
cd athena-ai-assistant
```

#### Step 2: Install Requirements
```bash
# Install Python if you haven't already (visit python.org)
# Then install Athena's requirements:
pip install -r requirements.txt
```

#### Step 3: Get Your API Keys (Free Options Available!)

You'll need at least one API key. Think of these as passwords that let Athena talk to AI services:

1. **Google Gemini API** (Required - Free tier available)
   - Visit: https://makersuite.google.com/app/apikey
   - Click "Create API Key"
   - Copy the key for later

2. **Mem0 API** (Optional - For memory features)
   - Visit: https://app.mem0.ai
   - Sign up for free account
   - Go to Settings → API Keys
   - Create and copy your key

3. **Tavily API** (Optional - For web search)
   - Visit: https://tavily.com
   - Sign up for free account
   - Get your API key from dashboard

#### Step 4: Set Up Your Keys
```bash
# Copy the example configuration
cp env_example.txt .env

# Edit .env file with your favorite text editor
# Add your API keys where indicated
```

#### Step 5: Run Athena!
```bash
python athena_chatbot.py
```

## 🎮 How to Use Athena

### Starting a Conversation
When you run Athena, you'll see a welcome message. Just start typing naturally:

```
You: Hi, I'm Sarah, mother of two kids - Emma (8) and Jack (6)
Athena: Nice to meet you, Sarah! I'll remember that you have two children...

You: Emma is vegetarian and Jack is allergic to peanuts
Athena: I've noted Emma's vegetarian diet and Jack's peanut allergy...

You: What should we have for dinner tonight?
Athena: Since it's Friday evening, here are some family-friendly dinner ideas that work for Emma's vegetarian diet and avoid peanuts for Jack...
```

### Special Commands
- **`memory`** - See what Athena remembers about your family
- **`new`** - Start a fresh conversation thread
- **`debug`** - (Technical) Show detailed system information
- **`quit`** or **`exit`** - End the conversation

### Pro Tips for Families
1. **Be Specific**: The more details you share, the better Athena can help
2. **Regular Updates**: Tell Athena about changes in schedules or preferences
3. **Ask Anything**: From meal planning to activity ideas to homework help
4. **Use Context**: "What should we do this weekend?" gets contextual suggestions

## 🔧 Technical Details (For Engineers)

### Architecture Overview

Athena is built using modern AI orchestration patterns with LangGraph, implementing a stateful conversation flow with tool integration:

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│   User      │────▶│   LangGraph  │────▶│   Gemini     │
│   Input     │     │   StateGraph │     │   LLM        │
└─────────────┘     └──────────────┘     └──────────────┘
                            │
                    ┌───────┴────────┐
                    │                 │
              ┌─────▼──────┐  ┌──────▼──────┐
              │   Mem0     │  │   Tavily    │
              │   Memory   │  │   Search    │
              └────────────┘  └─────────────┘
```

### Technology Stack

- **LLM Framework**: LangGraph 0.2.0+ with LangChain
- **Primary Model**: Google Gemini 2.0 Flash
- **Memory System**: Mem0 for persistent user memory
- **Search Integration**: Tavily API for web search
- **State Management**: InMemorySaver with thread-based sessions
- **Context Enhancement**: Real-time temporal and location context injection

### Key Components

1. **State Management** (`State` TypedDict)
   - Messages with annotation-based updates
   - Context dictionary for session metadata
   - User ID for memory persistence

2. **Memory System**
   - Mem0 integration for cross-session persistence
   - Context-aware memory retrieval
   - Automatic memory formation from conversations

3. **Tool Integration**
   - Conditional routing via `tools_condition`
   - ToolNode for web search execution
   - Extensible tool architecture

4. **Context Enhancement**
   - Real-time temporal context (time, day, date)
   - Location awareness via IP geolocation
   - Dynamic system prompt generation

### Advanced Configuration

#### Debug Mode
```bash
python athena_chatbot.py --debug
```
Enables verbose logging for memory operations, LLM interactions, and system prompt generation.

#### Environment Variables
```python
GOOGLE_API_KEY=your_gemini_key        # Required
MEM0_API_KEY=your_mem0_key           # Optional - enables persistent memory
TAVILY_API_KEY=your_tavily_key       # Optional - enables web search
LANGSMITH_API_KEY=your_langsmith_key # Optional - enables tracing
LANGSMITH_PROJECT=your_project_name  # Optional - LangSmith project
```

### API Response Handling

The memory system handles multiple Mem0 response formats:
```python
# List format (current)
[{"memory": "text", "user_id": "...", ...}]

# Dict with results (legacy)
{"results": [{"memory": "text", ...}]}
```

### Extending Athena

#### Adding New Tools
```python
from langchain.tools import Tool

new_tool = Tool(
    name="calendar",
    func=calendar_function,
    description="Manage family calendar"
)
tools.append(new_tool)
```

#### Custom Memory Strategies
Override `create_memory_enhanced_system_prompt()` to implement custom memory retrieval strategies or scoring algorithms.

## 📊 Performance Considerations

- **Memory Retrieval**: Limited to 10 most recent memories + 3 contextual matches
- **Context Window**: ~1500 chars for system prompt including memories
- **Response Time**: ~1-3 seconds depending on memory retrieval and tool use
- **Session Persistence**: In-memory storage cleared on restart

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Clone repository
git clone https://github.com/RichPM478/athena-ai-assistant.git
cd athena-ai-assistant

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -r requirements.txt
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph) and [LangChain](https://github.com/langchain-ai/langchain)
- Powered by [Google Gemini](https://deepmind.google/technologies/gemini/)
- Memory persistence by [Mem0](https://mem0.ai)
- Web search by [Tavily](https://tavily.com)

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/RichPM478/athena-ai-assistant/issues)
- **Discussions**: [GitHub Discussions](https://github.com/RichPM478/athena-ai-assistant/discussions)
- **Email**: [Contact Form](https://github.com/RichPM478)

---

*Built with ❤️ for families everywhere. Making AI helpful, not complicated.*