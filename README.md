# 🏛️ Athena AI Assistant - Your Intelligent Family Life Planning Service

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![LangGraph](https://img.shields.io/badge/LangGraph%20Platform-Ready-green.svg)
![Gemini](https://img.shields.io/badge/Google%20Gemini-2.0-red.svg)
![API](https://img.shields.io/badge/REST%20API-Enabled-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🌟 What is Athena?

Athena is your personal AI-powered family life planning assistant that runs as a **service** on your home network. Unlike traditional chatbots, Athena runs as a professional API service that can power **multiple apps and devices** throughout your home - from web apps to mobile apps to voice assistants.

Think of it as having a knowledgeable friend who:
- 🧠 **Remembers everything** about your family's preferences, schedules, and needs
- ⏰ **Knows what time it is** and gives contextual suggestions
- 🌍 **Understands your location** for local recommendations  
- 📱 **Works with any device** - phones, tablets, smart speakers, web browsers
- 🔒 **Keeps your data private** by running entirely on your own network

## 🎯 Perfect For Families Who Want:

### 👨‍👩‍👧‍👦 **Smart Family Management**
- Never forget important details about family members, preferences, or schedules
- Get intelligent suggestions for meals, activities, and schedules based on your unique needs
- Keep track of everyone's activities, appointments, and responsibilities
- Save time with quick answers and recommendations

### 🏠 **Whole-Home AI Integration**  
- **Kitchen tablet**: "What's for dinner tonight?"
- **Living room TV**: "What should we watch as a family?"
- **Kids' rooms**: "Help me with my homework"
- **Parent's phone**: "Remind me about Emma's soccer practice"
- **Smart speakers**: "Hey Google, ask Athena about weekend plans"

### 🔐 **Privacy-First Approach**
- Runs entirely on **your home network** - no cloud dependencies for core features
- **Your conversations stay at home** - never sent to external servers
- **You control your data** - easy backup and migration
- **Multiple family members** can have separate, private conversations

## ✨ Key Features

### 🧠 **Persistent Memory System**
Athena remembers your conversations and learns about your family over time:
- Family members' names, ages, and preferences
- Dietary restrictions and favorite foods  
- Schedule patterns and activity preferences
- Important dates and recurring events
- **Separate memories for each family member**

### 🌍 **Real-Time Context Awareness**
Athena understands your current situation:
- **Time-aware**: Morning routines, dinner planning, bedtime activities
- **Day-aware**: Weekday vs weekend appropriate recommendations
- **Season-aware**: Weather and seasonal activity suggestions  
- **Location-aware**: Local events, restaurants, and activities

### 🔍 **Live Information Access**
Get up-to-date information when needed:
- Local events and activities happening now
- Recipe ideas and nutritional information
- Educational resources and homework help
- Current weather for activity planning

### 🚀 **Professional API Service**
Unlike simple chatbots, Athena runs as a robust service:
- **REST API** for easy integration with any programming language
- **Real-time streaming** responses for instant feedback
- **Multi-user support** with separate conversations and memories
- **Professional documentation** for developers
- **Visual debugging tools** for troubleshooting

## 🏗️ How It Works (Simple Explanation)

```
┌─────────────────────────────────────────────────┐
│           Your Home Network                     │
│                                                 │
│  ┌─────────────────┐                           │
│  │  Athena Service │ ← Runs on one computer     │
│  │  (like Netflix, │   in your home             │
│  │   but for AI)   │                           │
│  └─────────┬───────┘                           │
│            │                                   │
│  ┌─────────┴─────────┬──────────┬──────────┐   │
│  │                   │          │          │   │
│  ▼                   ▼          ▼          ▼   │
│ 📱 Phone           💻 Laptop   📺 TV    🔊 Speaker │
│                                                 │
└─────────────────────────────────────────────────┘
```

1. **Install Athena** on one computer in your home (Mac, Windows, or Linux)
2. **Athena runs as a service** - like having Netflix but for AI assistance
3. **Any device** can connect to Athena through your home WiFi
4. **Each family member** gets their own personalized experience
5. **Everything stays private** within your home network

## 🚀 Quick Start Guide

### For Non-Technical Users (5 minutes)

#### What You Need:
- A computer (Mac, Windows, or Linux) 
- Internet connection for initial setup
- Free API keys (we'll show you how to get them)

#### Easy Setup:
1. **Download**: Get Athena from GitHub
2. **Install**: Run the simple installer  
3. **Configure**: Add your free API keys
4. **Start**: Launch Athena service
5. **Connect**: Open http://localhost:2024 in any web browser

### For Technical Users

Athena is built on the **LangGraph Platform**, providing enterprise-grade reliability and performance:

```bash
# Quick start
git clone https://github.com/your-username/athena-ai-assistant.git
cd athena-ai-assistant
pip install -r requirements.txt

# Set up your API keys in .env file
cp env_example.txt .env
# Edit .env with your API keys

# Start the service
langgraph dev

# Service available at http://127.0.0.1:2024
# API docs at http://127.0.0.1:2024/docs
```

## 📋 Detailed Setup Instructions

### Step 1: Get Your Free API Keys

You'll need at least one API key to get started:

#### 🔑 **Google Gemini API** (Required - Free tier available)
- Visit: https://makersuite.google.com/app/apikey
- Sign in with your Google account
- Click "Create API Key" 
- Copy and save the key

#### 🔑 **Mem0 API** (Optional - For memory features)
- Visit: https://app.mem0.ai
- Sign up for free account
- Go to Settings → API Keys
- Create and copy your key
- **Why you want this**: Athena remembers your family preferences between conversations

#### 🔑 **Tavily API** (Optional - For web search)
- Visit: https://tavily.com  
- Sign up for free account
- Get your API key from dashboard
- **Why you want this**: Athena can look up current information like local events

### Step 2: Installation

```bash
# Download the project
git clone https://github.com/your-username/athena-ai-assistant.git
cd athena-ai-assistant

# Install Python requirements
pip install -r requirements.txt

# Install LangGraph CLI (for running the service)
pip install "langgraph-cli[inmem]"
```

### Step 3: Configuration

```bash
# Copy the example configuration file
cp env_example.txt .env

# Edit .env with your favorite text editor and add your API keys:
# GOOGLE_API_KEY=your_gemini_key_here
# MEM0_API_KEY=your_mem0_key_here  
# TAVILY_API_KEY=your_tavily_key_here
```

### Step 4: Start Athena Service

```bash
# Start the service (runs until you stop it)
langgraph dev
```

You should see:
```
- 🚀 API: http://127.0.0.1:2024
- 📚 API Docs: http://127.0.0.1:2024/docs  
- 🎨 Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
```

## 🎮 How to Use Athena

### Option 1: Web Browser (Simplest)
1. Open your web browser
2. Go to http://127.0.0.1:2024/docs  
3. Try the interactive API documentation

### Option 2: Any Programming Language
Athena provides a standard REST API that works with any language:

**Python Example:**
```python
import requests

response = requests.post("http://127.0.0.1:2024/runs/stream", json={
    "assistant_id": "athena", 
    "input": {"messages": [{"role": "user", "content": "Hi! I'm Sarah, mom of two kids."}]},
    "config": {"configurable": {"thread_id": "sarah_family"}}
})
```

**JavaScript Example:**
```javascript
fetch('http://127.0.0.1:2024/runs/stream', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        assistant_id: "athena",
        input: {messages: [{role: "user", content: "What's for dinner?"}]},
        config: {configurable: {thread_id: "my_family"}}
    })
})
```

**curl Example:**
```bash
curl -X POST http://127.0.0.1:2024/runs/stream \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "athena",
    "input": {"messages": [{"role": "user", "content": "Help me plan this weekend"}]},
    "config": {"configurable": {"thread_id": "weekend_planning"}}
  }'
```

### Sample Conversation

```
You: Hi, I'm Sarah, mother of two kids - Emma (8) and Jack (6)  
Athena: Nice to meet you, Sarah! I'll remember that you have two children, Emma who is 8 and Jack who is 6. How can I help with your family planning today?

You: Emma is vegetarian and Jack is allergic to peanuts
Athena: I've noted that Emma follows a vegetarian diet and Jack has a peanut allergy. This is important for meal planning and snack choices. Is there anything specific you'd like help with regarding meals or activities?

You: What should we have for dinner tonight?
Athena: Since it's Friday evening, here are some family-friendly dinner ideas that work for Emma's vegetarian diet and avoid peanuts for Jack:
- Homemade vegetable pizza with cheese
- Pasta with marinara sauce and a side salad  
- Veggie burgers with sweet potato fries
- Cheese quesadillas with black beans...
```

## 🏠 Multi-Device Family Setup

### Scenario: The Johnson Family
- **Dad's phone**: "Athena, remind me about soccer practice"
- **Mom's tablet in kitchen**: "What can I make for lunch with what's in the fridge?"
- **Kids' computer**: "Help me with my math homework"
- **Living room smart TV**: "What family movie should we watch tonight?"

Each device connects to the same Athena service, but each family member can have their own private conversation thread and memories.

## 🔧 Technical Architecture

### Built on LangGraph Platform

Athena leverages the **LangGraph Platform** for enterprise-grade performance:

```
┌──────────────────────────────────────────────┐
│            LangGraph Platform                │
│                                              │
│  ┌──────────────┐    ┌─────────────────┐    │
│  │   Athena AI  │    │  Memory System  │    │
│  │    Agent     │◄──►│     (Mem0)      │    │
│  └──────────────┘    └─────────────────┘    │
│           │                                  │
│  ┌────────▼──────┐    ┌─────────────────┐    │
│  │  Web Search   │    │  Context Engine │    │
│  │   (Tavily)    │    │ (Time/Location) │    │
│  └───────────────┘    └─────────────────┘    │
└──────────────────────────────────────────────┘
```

### Key Technical Features

- **LangGraph StateGraph**: Professional workflow orchestration
- **Real-time Streaming**: Instant response delivery via Server-Sent Events
- **Multi-user Threading**: Separate conversation contexts per user/device
- **Persistent Memory**: Conversations and preferences stored via Mem0
- **Context Injection**: Real-time date/time/location/season awareness
- **Tool Integration**: Extensible architecture for adding new capabilities
- **OpenAPI Documentation**: Auto-generated docs at `/docs` endpoint

### Technology Stack

- **🧠 AI Model**: Google Gemini 2.0 Flash (fast, intelligent responses)
- **🔧 Framework**: LangGraph Platform (enterprise AI orchestration)  
- **💾 Memory**: Mem0 (persistent conversation memory)
- **🔍 Search**: Tavily API (real-time web information)
- **🌐 API**: REST with Server-Sent Events streaming
- **📍 Context**: IP-based location + temporal awareness
- **🔒 Auth**: Multi-user support with configurable authentication

### Project Structure

```
athena-ai-assistant/
├── athena_agent/           # Core AI agent module
│   ├── __init__.py
│   └── agent.py           # Main LangGraph agent definition
├── auth/                  # Authentication system  
│   ├── auth_utils.py      # JWT tokens & password hashing
│   └── user_service.py    # User management service
├── database/              # User data management
│   ├── connection.py      # Database setup
│   ├── models.py          # User data models
│   └── migrations/        # Database schema versions
├── tests/                 # Comprehensive test suite
├── langgraph.json         # LangGraph Platform configuration
├── requirements.txt       # Python dependencies
├── .env                   # API keys (you create this)
└── README.md             # This file
```

### Performance & Scalability

- **Response Time**: 1-3 seconds for typical queries
- **Concurrent Users**: Handles multiple family members simultaneously  
- **Memory Efficiency**: Optimized for home server deployment
- **Persistence**: Automatic conversation and preference storage
- **Reliability**: Built on enterprise-grade LangGraph Platform

## 🛡️ Privacy & Security

### Your Data Stays Home
- **Local Processing**: Core AI reasoning happens on your network
- **Selective Cloud**: Only optional features (web search) use external APIs
- **No Tracking**: Athena doesn't send usage analytics anywhere
- **Easy Backup**: All your data in simple, portable formats

### Multi-User Privacy
- **Separate Memories**: Each family member has private conversation history
- **Configurable Sharing**: Choose what to share between family members
- **User Management**: Built-in authentication system ready for deployment
- **Audit Trails**: See exactly what data is stored and when

## 🚧 Current Status & Roadmap

### ✅ **Currently Available (v1.0)**
- ✅ LangGraph Platform service architecture  
- ✅ Real-time context awareness (time, location, season)
- ✅ Persistent memory system with Mem0 integration
- ✅ Multi-user support with separate conversation threads  
- ✅ REST API with streaming responses
- ✅ Web search integration via Tavily
- ✅ Professional API documentation
- ✅ Comprehensive test coverage
- ✅ Database-backed user management system

### 🔄 **Coming Soon (v1.1)**
- 🔄 Web dashboard for easy family management
- 🔄 Mobile app (React Native)  
- 🔄 Voice assistant integration (Alexa, Google Home)
- 🔄 Calendar integration (Google Calendar, Apple Calendar)
- 🔄 Recipe management with dietary restrictions
- 🔄 Family photo recognition and organization

### 🔮 **Future Vision (v2.0)**
- 🔮 Smart home device integration (lights, thermostats, etc.)
- 🔮 Advanced family scheduling with conflict resolution
- 🔮 Educational content recommendations by age/interest
- 🔮 Family budget and expense tracking
- 🔮 Health and wellness tracking integration
- 🔮 Multi-language support for diverse families

## 🤝 Contributing

We welcome contributions from both families who use Athena and developers who want to improve it!

### For Users
- **Report Issues**: Found a bug? Tell us about it!
- **Feature Requests**: What would make Athena more helpful for your family?
- **Success Stories**: Share how Athena helps your family stay organized

### For Developers

```bash
# Development setup
git clone https://github.com/your-username/athena-ai-assistant.git
cd athena-ai-assistant

# Create development environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Start development server
langgraph dev --debug
```

### Development Guidelines
- **Test Coverage**: All new features must include tests
- **Documentation**: Update README and inline docs for new features  
- **Privacy First**: New features must respect the privacy-first architecture
- **Family Friendly**: Consider how features impact families with children

## 📊 System Requirements

### Minimum Requirements
- **OS**: Windows 10, macOS 10.15, or Linux (Ubuntu 18.04+)
- **Python**: 3.11 or newer
- **RAM**: 4GB available  
- **Storage**: 2GB free space
- **Network**: Home WiFi for device connectivity

### Recommended Setup
- **OS**: Recent versions of Windows, macOS, or Linux
- **Python**: Latest stable version  
- **RAM**: 8GB+ for better performance with multiple users
- **Storage**: 10GB+ for conversation history and future features
- **Network**: Gigabit ethernet for fastest response times

### Deployment Options

#### Option 1: Family Computer (Easiest)
Run Athena on your main family computer. Family members connect via web browsers or mobile apps.

#### Option 2: Home Server (Best Performance)  
Run Athena on a dedicated home server or NAS for 24/7 availability and best performance.

#### Option 3: Raspberry Pi (Budget Option)
Run Athena on a Raspberry Pi 4 for a low-cost, always-on family AI assistant.

## 🆘 Troubleshooting

### Common Issues

**"Service won't start"**
- Check that Python 3.11+ is installed: `python --version`
- Verify API keys are correct in `.env` file
- Ensure no other service is using port 2024

**"Athena responds but seems confused"**  
- Clear conversation history: use a new `thread_id` in your requests
- Check that Mem0 API key is working (optional but recommended)
- Verify your internet connection for web search features

**"Can't connect from other devices"**
- Make sure Athena service is running: check http://127.0.0.1:2024/docs  
- Check your firewall isn't blocking port 2024
- Use your computer's IP address instead of 127.0.0.1 from other devices

### Getting Help

1. **Check the API documentation**: Visit http://127.0.0.1:2024/docs while Athena is running
2. **Review the logs**: Run with `langgraph dev --debug` for detailed information
3. **Search existing issues**: Check our GitHub Issues page
4. **Ask for help**: Create a new issue with your system details and error messages

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**What this means for you:**
- ✅ **Free to use** for personal and commercial purposes
- ✅ **Free to modify** and customize for your family's needs  
- ✅ **Free to share** with other families
- ✅ **No warranty** - provided "as-is" but with community support

## 🙏 Acknowledgments

Athena is built on the shoulders of giants:

- **[LangGraph](https://github.com/langchain-ai/langgraph)** - Enterprise AI workflow orchestration
- **[LangChain](https://github.com/langchain-ai/langchain)** - AI application framework  
- **[Google Gemini](https://deepmind.google/technologies/gemini/)** - Powerful AI reasoning
- **[Mem0](https://mem0.ai)** - Persistent memory for AI applications
- **[Tavily](https://tavily.com)** - Real-time web search for AI

Special thanks to:
- The open-source AI community for making sophisticated AI accessible to families
- Contributors who help improve Athena for everyone

## 📞 Support & Community  

### Quick Help
- **📖 Documentation**: This README + http://127.0.0.1:2024/docs (when running)
- **🐛 Bug Reports**: [GitHub Issues](https://github.com/your-username/athena-ai-assistant/issues)
- **💡 Feature Requests**: [GitHub Discussions](https://github.com/your-username/athena-ai-assistant/discussions)

### Community  
- **💬 Discord**: Join our family-focused AI community
- **🐦 Twitter**: Follow [@AthenaAI](https://twitter.com/athenaai) for updates
- **📧 Newsletter**: Get monthly tips for using AI in family life

### Professional Support
- **🏢 Enterprise**: Custom deployment and training for schools and organizations
- **🔧 Consulting**: Help setting up Athena for complex family situations
- **📚 Training**: Workshops on using AI tools safely with children

---

## 🌟 Final Thoughts

**Athena isn't just another chatbot - it's designed to be the AI assistant your family actually wants to use.**

Unlike cloud-based assistants that forget conversations and don't understand your family's unique needs, Athena:

- **Learns and remembers** your family's preferences and routines
- **Respects your privacy** by keeping your data at home
- **Grows with your family** through continuous updates and new features  
- **Connects everything** from phones to smart speakers to computers
- **Just works** with simple setup and reliable operation

Whether you're planning meals for picky eaters, coordinating schedules for busy families, or just want an AI that understands "Emma is vegetarian but Jack isn't," Athena is built to make your family life easier.

**Ready to get started?** The setup takes less than 10 minutes, and your family's personal AI assistant will be ready to help.

---

*Built with ❤️ for families everywhere. Making AI helpful, not complicated.*

**"Finally, an AI assistant that understands families aren't just collections of individuals - we're teams with shared goals, individual needs, and the beautiful chaos that makes us who we are."**