from typing import Annotated
from typing_extensions import TypedDict
from datetime import datetime
import requests
import json
import uuid

from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import InMemorySaver

from config import GOOGLE_API_KEY, TAVILY_API_KEY, LANGSMITH_API_KEY, LANGSMITH_PROJECT

# Set up LangSmith for monitoring (optional)
if LANGSMITH_API_KEY:
    import os
    os.environ["LANGSMITH_API_KEY"] = LANGSMITH_API_KEY
    os.environ["LANGSMITH_PROJECT"] = LANGSMITH_PROJECT

# Set up API keys
import os
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    messages: Annotated[list, add_messages]
    # Context information that gets updated with each interaction
    context: dict

def get_current_time_and_date():
    """Get current time and date in a user-friendly format."""
    now = datetime.now()
    return {
        "current_date": now.strftime("%A, %B %d, %Y"),
        "current_time": now.strftime("%I:%M %p"),
        "timezone": "Local Time",
        "day_of_week": now.strftime("%A"),
        "month": now.strftime("%B"),
        "year": now.strftime("%Y"),
        "is_weekend": now.weekday() >= 5,
        "is_weekday": now.weekday() < 5,
        "hour": now.hour,
        "is_morning": 5 <= now.hour < 12,
        "is_afternoon": 12 <= now.hour < 17,
        "is_evening": 17 <= now.hour < 21,
        "is_night": now.hour >= 21 or now.hour < 5
    }

def get_location_context():
    """Get location information (IP-based, can be enhanced with user input)."""
    try:
        # Get location from IP address (basic implementation)
        response = requests.get('https://ipapi.co/json/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "city": data.get('city', 'Unknown'),
                "region": data.get('region', 'Unknown'),
                "country": data.get('country_name', 'Unknown'),
                "timezone": data.get('timezone', 'Unknown'),
                "latitude": data.get('latitude'),
                "longitude": data.get('longitude')
            }
    except:
        pass
    
    # Fallback if location detection fails
    return {
        "city": "Unknown",
        "region": "Unknown", 
        "country": "Unknown",
        "timezone": "Unknown",
        "latitude": None,
        "longitude": None
    }

def create_context_aware_system_prompt():
    """Create a system prompt that includes real-time context."""
    time_info = get_current_time_and_date()
    location_info = get_location_context()
    
    # Determine time-based context
    time_context = ""
    if time_info["is_morning"]:
        time_context = "It's morning - perfect for planning the day ahead!"
    elif time_info["is_afternoon"]:
        time_context = "It's afternoon - great time to check on daily progress!"
    elif time_info["is_evening"]:
        time_context = "It's evening - ideal for family dinner planning and evening activities!"
    else:
        time_context = "It's late - time to wind down and plan for tomorrow!"
    
    # Determine day-based context
    day_context = ""
    if time_info["is_weekend"]:
        day_context = "It's the weekend - perfect for family activities and relaxation!"
    else:
        day_context = "It's a weekday - time for school, work, and structured activities!"
    
    system_prompt = f"""You are Athena, an intelligent family life planning assistant. You have access to real-time context to provide more relevant and timely advice.

CURRENT CONTEXT:
- Date: {time_info['current_date']}
- Time: {time_info['current_time']} ({time_info['timezone']})
- Day: {time_info['day_of_week']}
- Location: {location_info['city']}, {location_info['region']}, {location_info['country']}
- Time Context: {time_context}
- Day Context: {day_context}

USE THIS CONTEXT TO:
1. Provide time-relevant suggestions (morning routines, evening activities, weekend plans)
2. Consider the day of the week for scheduling (weekday vs weekend activities)
3. Offer location-appropriate recommendations when possible
4. Reference the current date and time naturally in your responses
5. Suggest activities that make sense for the current time of day

EXAMPLES OF CONTEXT-AWARE RESPONSES:
- "Since it's {time_info['current_time']} on a {time_info['day_of_week']}, you might want to..."
- "Given that it's {time_info['current_date']}, here are some seasonal activities..."
- "For {location_info['city']}, you could consider..."

Always be helpful, family-focused, and use the context to provide more personalized and timely advice."""

    return system_prompt

def initialize_context():
    """Initialize the context with current time and location information."""
    time_info = get_current_time_and_date()
    location_info = get_location_context()
    
    return {
        "time": time_info,
        "location": location_info,
        "session_start": datetime.now().isoformat(),
        "last_updated": datetime.now().isoformat()
    }

def update_context(state: State):
    """Update the context with current information."""
    current_context = state.get("context", {})
    current_context["time"] = get_current_time_and_date()
    current_context["last_updated"] = datetime.now().isoformat()
    return {"context": current_context}

# Initialize the graph
graph_builder = StateGraph(State)

# Initialize Gemini 2.5 model
llm = init_chat_model("google_genai:gemini-2.0-flash")

# Set up web search tool (only if API key is available)
if TAVILY_API_KEY:
    os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY
    tool = TavilySearch(max_results=3)
    tools = [tool]
    llm_with_tools = llm.bind_tools(tools)
    
    def chatbot(state: State):
        """The main chatbot node that processes user messages and generates responses."""
        # Update context before processing
        updated_state = update_context(state)
        
        # Create context-aware system prompt
        system_prompt = create_context_aware_system_prompt()
        
        # Add system message to the beginning of the conversation if it's the first message
        messages = state["messages"]
        if not messages or not isinstance(messages[0], SystemMessage):
            messages = [SystemMessage(content=system_prompt)] + messages
        
        return {"messages": [llm_with_tools.invoke(messages)]}
    
    # Add the chatbot node
    graph_builder.add_node("chatbot", chatbot)
    
    # Add tool node for web search
    tool_node = ToolNode(tools=[tool])
    graph_builder.add_node("tools", tool_node)
    
    # Add conditional edges to route between chatbot and tools
    graph_builder.add_conditional_edges(
        "chatbot",
        tools_condition,
    )
    # Any time a tool is called, we return to the chatbot to decide the next step
    graph_builder.add_edge("tools", "chatbot")
    
else:
    # Fallback to basic chatbot without tools
    def chatbot(state: State):
        """The main chatbot node that processes user messages and generates responses."""
        # Update context before processing
        updated_state = update_context(state)
        
        # Create context-aware system prompt
        system_prompt = create_context_aware_system_prompt()
        
        # Add system message to the beginning of the conversation if it's the first message
        messages = state["messages"]
        if not messages or not isinstance(messages[0], SystemMessage):
            messages = [SystemMessage(content=system_prompt)] + messages
        
        return {"messages": [llm.invoke(messages)]}
    
    # Add the chatbot node
    graph_builder.add_node("chatbot", chatbot)

# Add entry point
graph_builder.add_edge(START, "chatbot")

# Add exit point
graph_builder.add_edge("chatbot", END)

# Create memory checkpointer for persistent conversations
memory = InMemorySaver()

# Compile the graph with memory checkpointer
graph = graph_builder.compile(checkpointer=memory)

def stream_graph_updates(user_input: str, config: dict):
    """Stream the chatbot responses for better user experience with memory support."""
    # Initialize context for new conversation if not exists
    initial_context = initialize_context()
    
    for event in graph.stream({
        "messages": [HumanMessage(content=user_input)],
        "context": initial_context
    }, config, stream_mode="values"):
        if "messages" in event and event["messages"]:
            print("Athena:", event["messages"][-1].content)

def run_chatbot():
    """Run the interactive chatbot with memory support."""
    print("🤖 Welcome to Athena - Your Family Life Planning Assistant!")
    print("I'm here to help you plan and organize your family's life.")
    print("💾 Memory enabled - I'll remember our conversation!")
    
    # Display current context
    time_info = get_current_time_and_date()
    location_info = get_location_context()
    
    print(f"📅 Current Context:")
    print(f"   Date: {time_info['current_date']}")
    print(f"   Time: {time_info['current_time']}")
    print(f"   Location: {location_info['city']}, {location_info['region']}")
    print(f"   Day: {time_info['day_of_week']}")
    
    if TAVILY_API_KEY:
        print("🔍 Web search enabled - I can find current information for you!")
    else:
        print("⚠️  Web search disabled - Get a free Tavily API key to enable current information search")
    
    print("Type 'quit', 'exit', or 'q' to end our conversation.")
    print("Type 'new' to start a fresh conversation thread.\n")
    
    # Generate a unique thread ID for this conversation session
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    print(f"🔗 Conversation Thread: {thread_id[:8]}...\n")
    
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("👋 Thank you for using Athena! Have a wonderful day!")
                break
            elif user_input.lower() == "new":
                # Start a new conversation thread
                thread_id = str(uuid.uuid4())
                config = {"configurable": {"thread_id": thread_id}}
                print(f"✨ Started new conversation thread: {thread_id[:8]}...")
                print("🔄 Fresh start - I won't remember our previous conversation in this thread.\n")
                continue
            elif user_input.lower() == "memory":
                # Show memory state for debugging
                snapshot = graph.get_state(config)
                print(f"📊 Memory State: {len(snapshot.values.get('messages', []))} messages stored")
                print(f"🆔 Thread ID: {thread_id}")
                continue
                
            stream_graph_updates(user_input, config)
            print()  # Add spacing between exchanges
        except KeyboardInterrupt:
            print("\n👋 Goodbye! Thanks for using Athena!")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            print("Please try again or type 'quit' to exit.")

if __name__ == "__main__":
    run_chatbot()
