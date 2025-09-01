"""
Athena Agent - LangGraph Platform Implementation
This module defines the main graph that will be served by LangGraph Platform.
"""

from typing import Annotated, Optional, Dict, Any
from typing_extensions import TypedDict
from datetime import datetime
import os
import json
import warnings

from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

# Import our custom modules
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from config import GOOGLE_API_KEY, TAVILY_API_KEY, MEM0_API_KEY
from context_utils import get_current_time_and_date, get_location_context

# Set up API keys
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Initialize Mem0 client if available
mem0_client = None
if MEM0_API_KEY:
    try:
        from mem0 import MemoryClient
        warnings.filterwarnings("ignore", category=DeprecationWarning, module="mem0")
        mem0_client = MemoryClient(api_key=MEM0_API_KEY)
        print("[INFO] Mem0 memory system initialized")
    except ImportError:
        print("[WARNING] Mem0 library not installed")
    except Exception as e:
        print(f"[WARNING] Failed to initialize Mem0: {e}")


class State(TypedDict):
    """
    The state of the conversation.
    This is what gets passed between nodes in the graph.
    """
    messages: Annotated[list, add_messages]
    context: Dict[str, Any]
    user_id: Optional[str]  # User identifier for multi-user support
    
    
# Note: Multi-user support will be added back in the next phase


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
    
    # Check if tools are available
    tools_available = ""
    if TAVILY_API_KEY:
        tools_available = """
AVAILABLE TOOLS:
- Web Search: You have access to web search via the TavilySearch tool. Use this to:
  • Look up current weather forecasts and conditions
  • Search for local events and activities
  • Find recipes and meal ideas
  • Get current news and information
  • Research any topic the family needs help with
  
IMPORTANT: When asked about weather, news, events, or any current information, USE THE SEARCH TOOL to get accurate, up-to-date information.
"""
    
    system_prompt = f"""You are Athena, an intelligent family life planning assistant. You have access to real-time context to provide more relevant and timely advice.

CURRENT CONTEXT:
- Date: {time_info['current_date']}
- Time: {time_info['current_time']} ({time_info['timezone']})
- Day: {time_info['day_of_week']}
- Location: {location_info['city']}, {location_info['region']}, {location_info['country']}
- Time Context: {time_context}
- Day Context: {day_context}
{tools_available}
USE THIS CONTEXT TO:
1. Provide time-relevant suggestions (morning routines, evening activities, weekend plans)
2. Consider the day of the week for scheduling (weekday vs weekend activities)
3. Offer location-appropriate recommendations when possible
4. Reference the current date and time naturally in your responses
5. Suggest activities that make sense for the current time of day
6. USE YOUR SEARCH TOOL when asked about weather, news, events, or current information

Always be helpful, family-focused, and use the context to provide more personalized and timely advice. When asked about weather or any current information, remember to use your search capabilities."""

    return system_prompt


def create_memory_enhanced_system_prompt(user_id: str, base_prompt: str, user_message: str = None):
    """Create a system prompt enhanced with relevant memories from Mem0."""
    if not mem0_client or not user_id:
        return base_prompt
    
    try:
        # Get user-specific memories
        all_memories = mem0_client.get_all(user_id=user_id)
        
        memory_context = ""
        if all_memories:
            memories_list = None
            if isinstance(all_memories, dict):
                if 'results' in all_memories:
                    memories_list = all_memories['results']
                elif 'memories' in all_memories:
                    memories_list = all_memories['memories']
            elif isinstance(all_memories, list):
                memories_list = all_memories
            
            if memories_list:
                memory_context = "\n\nSTORED FAMILY INFORMATION:\n"
                for memory in memories_list[:10]:
                    memory_text = memory.get('memory', memory.get('text', str(memory)))
                    memory_context += f"• {memory_text}\n"
                memory_context += "\nIMPORTANT: Use this information to personalize your responses."
        
        # Also search for relevant memories if user message provided
        if user_message and mem0_client:
            search_results = mem0_client.search(user_message, user_id=user_id)
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
                        memory_context += f"• {result_text}\n"
        
        return base_prompt + memory_context
    except Exception as e:
        print(f"[WARNING] Memory retrieval failed: {e}")
        return base_prompt


def store_interaction_in_memory(user_id: str, user_message: str, assistant_response: str):
    """Store the interaction in Mem0 for future reference."""
    if not mem0_client or not user_id:
        return
    
    try:
        messages = [
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": assistant_response}
        ]
        mem0_client.add(messages, user_id=user_id)
    except Exception as e:
        print(f"[WARNING] Failed to store memory: {e}")


# Initialize the LLM
llm = init_chat_model("google_genai:gemini-2.5-flash")

# Set up tools if available
tools = []
if TAVILY_API_KEY:
    os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY
    tool = TavilySearch(max_results=3)
    tools = [tool]
    llm_with_tools = llm.bind_tools(tools)
else:
    llm_with_tools = llm


def chatbot(state: State, config: RunnableConfig) -> dict:
    """
    The main chatbot node that processes user messages and generates responses.
    This is the core of Athena's intelligence.
    """
    # Extract user_id from config - this enables multi-user support!
    configurable = config.get("configurable", {})
    metadata = configurable.get("metadata", {})
    user_id = metadata.get("user_id", "default_user")
    
    # If no user_id in metadata, try to extract from thread_id
    if user_id == "default_user":
        thread_id = configurable.get("thread_id", "")
        # Extract user info from thread if it contains user info
        if "user_" in thread_id:
            parts = thread_id.split("_")
            if len(parts) >= 2:
                user_id = f"user_{parts[1]}"
    
    # Update context with current time/location
    context = state.get("context", {})
    context.update({
        "time": get_current_time_and_date(),
        "location": get_location_context(),
        "last_updated": datetime.now().isoformat()
    })
    
    # Create context-aware system prompt
    base_system_prompt = create_context_aware_system_prompt()
    
    # Get the current user message for context-aware memory search
    messages = state["messages"]
    current_user_message = ""
    if messages and isinstance(messages[-1], HumanMessage):
        current_user_message = messages[-1].content
    
    # Enhance with user-specific memories
    system_prompt = create_memory_enhanced_system_prompt(
        user_id, 
        base_system_prompt, 
        current_user_message
    )
    
    # Prepare messages with system prompt
    if messages and isinstance(messages[0], SystemMessage):
        messages[0] = SystemMessage(content=system_prompt)
    else:
        messages = [SystemMessage(content=system_prompt)] + messages
    
    # Generate response
    response = llm_with_tools.invoke(messages)
    
    # Store interaction in memory for this user
    if current_user_message and isinstance(response.content, str):
        store_interaction_in_memory(user_id, current_user_message, response.content)
    
    return {
        "messages": [response],
        "context": context,
        "user_id": user_id
    }


# Build the graph
graph_builder = StateGraph(State)

# Add the chatbot node
graph_builder.add_node("chatbot", chatbot)

# Add tool node if tools are available
if tools:
    tool_node = ToolNode(tools=tools)
    graph_builder.add_node("tools", tool_node)
    
    # Add conditional edges to route between chatbot and tools
    graph_builder.add_conditional_edges(
        "chatbot",
        tools_condition,
    )
    # Any time a tool is called, we return to the chatbot
    graph_builder.add_edge("tools", "chatbot")
    graph_builder.add_edge(START, "chatbot")
else:
    # Direct connection without tools
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_edge("chatbot", END)

# Compile the graph - LangGraph Platform handles persistence automatically
graph = graph_builder.compile()

# Export the graph for LangGraph Platform
__all__ = ['graph']