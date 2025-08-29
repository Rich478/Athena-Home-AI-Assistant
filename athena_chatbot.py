from typing import Annotated
from typing_extensions import TypedDict
from datetime import datetime
import requests
import json
import uuid
import argparse

from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import InMemorySaver

from config import GOOGLE_API_KEY, TAVILY_API_KEY, MEM0_API_KEY, LANGSMITH_API_KEY, LANGSMITH_PROJECT

# Set up command-line arguments
parser = argparse.ArgumentParser(description='Athena - Your Family Life Planning Assistant')
parser.add_argument('-debug', '--debug', action='store_true', help='Enable debug mode for troubleshooting')
args = parser.parse_args()
DEBUG_MODE = args.debug

# Set up LangSmith for monitoring (optional)
if LANGSMITH_API_KEY:
    import os
    os.environ["LANGSMITH_API_KEY"] = LANGSMITH_API_KEY
    os.environ["LANGSMITH_PROJECT"] = LANGSMITH_PROJECT

# Set up API keys
import os
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Initialize Mem0 client if API key is available
mem0_client = None
if MEM0_API_KEY:
    try:
        from mem0 import MemoryClient
        import warnings
        # Suppress the specific mem0 deprecation warning
        warnings.filterwarnings("ignore", category=DeprecationWarning, module="mem0")
        mem0_client = MemoryClient(api_key=MEM0_API_KEY)
        print("✅ Mem0 memory system initialized successfully!")
    except ImportError:
        print("⚠️  Mem0 library not installed. Run: pip install mem0ai")
        mem0_client = None
    except Exception as e:
        print(f"⚠️  Failed to initialize Mem0: {e}")
        mem0_client = None

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    messages: Annotated[list, add_messages]
    # Context information that gets updated with each interaction
    context: dict
    # Mem0 user ID for persistent memory
    mem0_user_id: str

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

def create_memory_enhanced_system_prompt(user_id: str, base_prompt: str, user_message: str = None):
    """Create a system prompt enhanced with relevant memories from Mem0."""
    if not mem0_client:
        if DEBUG_MODE:
            print("[DEBUG] No mem0_client available")
        return base_prompt
    
    try:
        # First, get ALL memories for this user
        if DEBUG_MODE:
            print(f"[DEBUG] Fetching all memories for user: {user_id}")
        all_memories = mem0_client.get_all(user_id=user_id)
        if DEBUG_MODE:
            print(f"[DEBUG] Raw all_memories response: {all_memories}")
        
        memory_context = ""
        if all_memories:
            # Check different possible response structures
            memories_list = None
            if isinstance(all_memories, dict):
                if 'results' in all_memories:
                    memories_list = all_memories['results']
                elif 'memories' in all_memories:
                    memories_list = all_memories['memories']
                else:
                    if DEBUG_MODE:
                        print(f"[DEBUG] Unexpected memory structure. Keys: {all_memories.keys()}")
            elif isinstance(all_memories, list):
                memories_list = all_memories
            
            if memories_list:
                if DEBUG_MODE:
                    print(f"[DEBUG] Found {len(memories_list)} memories")
                memory_context = "\n\nSTORED FAMILY INFORMATION:\n"
                for i, memory in enumerate(memories_list[:10]):
                    memory_text = memory.get('memory', memory.get('text', str(memory)))
                    if DEBUG_MODE:
                        print(f"[DEBUG] Memory {i+1}: {memory_text}")
                    memory_context += f"• {memory_text}\n"
                memory_context += "\nIMPORTANT: Use this information to answer questions about the family. When asked about age, name, or other personal details, refer to these memories."
        
        # Also try context-aware search if user message is provided
        if user_message:
            if DEBUG_MODE:
                print(f"[DEBUG] Searching memories for: {user_message}")
            search_results = mem0_client.search(user_message, user_id=user_id)
            if DEBUG_MODE:
                print(f"[DEBUG] Raw search_results: {search_results}")
            
            if search_results:
                results_list = None
                if isinstance(search_results, dict) and 'results' in search_results:
                    results_list = search_results['results']
                elif isinstance(search_results, list):
                    results_list = search_results
                
                if results_list:
                    memory_context += "\n\nRELEVANT CONTEXT FOR THIS QUERY:\n"
                    for result in results_list[:3]:
                        result_text = result.get('memory', result.get('text', str(result)))
                        if DEBUG_MODE:
                            print(f"[DEBUG] Search result: {result_text}")
                        memory_context += f"• {result_text}\n"
        
        final_prompt = base_prompt + memory_context
        if DEBUG_MODE:
            print(f"[DEBUG] Memory context added: {len(memory_context)} chars")
            print(f"[DEBUG] Final prompt length: {len(final_prompt)} chars")
        return final_prompt
    except Exception as e:
        print(f"⚠️  Memory retrieval failed: {e}")
        if DEBUG_MODE:
            import traceback
            print(f"[DEBUG] Traceback: {traceback.format_exc()}")
        return base_prompt

def store_interaction_in_memory(user_id: str, user_message: str, assistant_response: str):
    """Store the interaction in Mem0 for future reference."""
    if not mem0_client:
        return
    
    try:
        # Store the interaction in the correct format for Mem0 API v1.1
        # The add method expects messages as a list of dicts with role and content
        messages = [
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": assistant_response}
        ]
        mem0_client.add(messages, user_id=user_id)
    except Exception as e:
        print(f"⚠️  Failed to store memory: {e}")

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
        base_system_prompt = create_context_aware_system_prompt()
        
        # Get the current user message for context-aware memory search
        messages = state["messages"]
        current_user_message = ""
        if messages and isinstance(messages[-1], HumanMessage):
            current_user_message = messages[-1].content
        
        # Enhance with memories if Mem0 is available
        user_id = state.get("mem0_user_id", "default_user")
        system_prompt = create_memory_enhanced_system_prompt(user_id, base_system_prompt, current_user_message)
        
        if DEBUG_MODE:
            print(f"[DEBUG] System prompt enhanced. Length: {len(system_prompt)} chars")
            print(f"[DEBUG] First 200 chars of system prompt: {system_prompt[:200]}...")
        
        # Always update the system message with the latest memories
        if messages and isinstance(messages[0], SystemMessage):
            messages[0] = SystemMessage(content=system_prompt)
        else:
            messages = [SystemMessage(content=system_prompt)] + messages
        
        if DEBUG_MODE:
            print(f"[DEBUG] Sending {len(messages)} messages to LLM")
            print(f"[DEBUG] First message type: {type(messages[0]).__name__}")
        
        # Generate response
        response = llm_with_tools.invoke(messages)
        
        # Store interaction in memory
        if current_user_message:
            store_interaction_in_memory(user_id, current_user_message, response.content)
        
        return {"messages": [response]}
    
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
        base_system_prompt = create_context_aware_system_prompt()
        
        # Get the current user message for context-aware memory search
        messages = state["messages"]
        current_user_message = ""
        if messages and isinstance(messages[-1], HumanMessage):
            current_user_message = messages[-1].content
        
        # Enhance with memories if Mem0 is available
        user_id = state.get("mem0_user_id", "default_user")
        system_prompt = create_memory_enhanced_system_prompt(user_id, base_system_prompt, current_user_message)
        
        if DEBUG_MODE:
            print(f"[DEBUG] System prompt enhanced. Length: {len(system_prompt)} chars")
            print(f"[DEBUG] First 200 chars of system prompt: {system_prompt[:200]}...")
        
        # Always update the system message with the latest memories
        if messages and isinstance(messages[0], SystemMessage):
            messages[0] = SystemMessage(content=system_prompt)
        else:
            messages = [SystemMessage(content=system_prompt)] + messages
        
        if DEBUG_MODE:
            print(f"[DEBUG] Sending {len(messages)} messages to LLM")
            print(f"[DEBUG] First message type: {type(messages[0]).__name__}")
        
        # Generate response
        response = llm.invoke(messages)
        
        # Store interaction in memory
        if current_user_message:
            store_interaction_in_memory(user_id, current_user_message, response.content)
        
        return {"messages": [response]}
    
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

def stream_graph_updates(user_input: str, config: dict, user_id: str):
    """Stream the chatbot responses for better user experience with memory support."""
    # Initialize context for new conversation if not exists
    initial_context = initialize_context()
    
    for event in graph.stream({
        "messages": [HumanMessage(content=user_input)],
        "context": initial_context,
        "mem0_user_id": user_id
    }, config, stream_mode="values"):
        if "messages" in event and event["messages"]:
            # Only print assistant messages, not user messages
            last_message = event["messages"][-1]
            if hasattr(last_message, 'content') and not isinstance(last_message, HumanMessage):
                print("Athena:", last_message.content)

def run_chatbot():
    """Run the interactive chatbot with memory support."""
    print("🤖 Welcome to Athena - Your Family Life Planning Assistant!")
    print("I'm here to help you plan and organize your family's life.")
    
    if DEBUG_MODE:
        print("🔧 DEBUG MODE ENABLED - Verbose output for troubleshooting")
    
    if mem0_client:
        print("🧠 Persistent memory enabled - I'll learn and remember things about your family!")
    else:
        print("💾 Session memory only - Get a Mem0 API key for persistent learning across sessions")
    
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
    print("Type 'new' to start a fresh conversation thread.")
    print("Type 'memory' to see your stored memories.")
    print("Type 'debug' to see debug information.\n")
    
    # Generate a unique user ID for this family (you can customize this)
    user_id = "athena_family_001"  # You can make this configurable
    print(f"👧‍👦 Family ID: {user_id}")
    
    # Generate a unique thread ID for this conversation session
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    print(f"🔗 Conversation Thread: {thread_id[:8]}...\n")
    
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("👋 Thank you for using Athena! I'll remember our conversation for next time!")
                break
            elif user_input.lower() == "new":
                # Start a new conversation thread
                thread_id = str(uuid.uuid4())
                config = {"configurable": {"thread_id": thread_id}}
                print(f"✨ Started new conversation thread: {thread_id[:8]}...")
                print("🔄 Fresh start - but I'll still remember your family preferences!")
                continue
            elif user_input.lower() == "memory":
                # Show memory state for debugging
                snapshot = graph.get_state(config)
                print(f"📊 Session Memory: {len(snapshot.values.get('messages', []))} messages stored")
                print(f"🆔 Thread ID: {thread_id}")
                if mem0_client:
                    try:
                        memories = mem0_client.get_all(user_id=user_id)
                        if DEBUG_MODE:
                            print(f"[DEBUG] Raw memory response: {memories}")
                        if memories:
                            if isinstance(memories, dict) and 'results' in memories:
                                mem_list = memories['results']
                            elif isinstance(memories, list):
                                mem_list = memories
                            else:
                                mem_list = []
                            
                            if mem_list:
                                print(f"🧠 Persistent Memories: {len(mem_list)} stored")
                                print("All memories:")
                                for i, memory in enumerate(mem_list):
                                    memory_text = memory.get('memory', memory.get('text', str(memory)))
                                    print(f"  {i+1}. {memory_text}")
                            else:
                                print("🧠 No persistent memories stored yet.")
                        else:
                            print("🧠 No persistent memories stored yet.")
                    except Exception as e:
                        print(f"⚠️  Could not retrieve memories: {e}")
                        if DEBUG_MODE:
                            import traceback
                            print(f"[DEBUG] Traceback: {traceback.format_exc()}")
                continue
            elif user_input.lower() == "debug":
                # Show debug information
                print("\n=== DEBUG INFORMATION ===")
                print(f"User ID: {user_id}")
                print(f"Thread ID: {thread_id}")
                
                # Show current system prompt
                base_prompt = create_context_aware_system_prompt()
                enhanced_prompt = create_memory_enhanced_system_prompt(user_id, base_prompt, "test query")
                print(f"\n[DEBUG] System Prompt Preview (first 500 chars):")
                print(enhanced_prompt[:500])
                print(f"\n[DEBUG] Total System Prompt Length: {len(enhanced_prompt)} chars")
                
                # Show message structure
                snapshot = graph.get_state(config)
                messages = snapshot.values.get('messages', [])
                print(f"\n[DEBUG] Message Structure:")
                for i, msg in enumerate(messages[:3]):
                    msg_type = type(msg).__name__
                    content_preview = str(msg.content)[:100] if hasattr(msg, 'content') else 'No content'
                    print(f"  {i+1}. {msg_type}: {content_preview}...")
                print("========================\n")
                continue
                
            stream_graph_updates(user_input, config, user_id)
            print()  # Add spacing between exchanges
        except KeyboardInterrupt:
            print("\n👋 Goodbye! Thanks for using Athena!")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            print("Please try again or type 'quit' to exit.")

if __name__ == "__main__":
    # Show usage hint if debug mode is not enabled
    if not DEBUG_MODE:
        print("💡 Tip: Run with -debug flag for troubleshooting (python athena_chatbot.py -debug)")
    run_chatbot()
