from typing import Annotated
from typing_extensions import TypedDict

from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

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
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]

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
        return {"messages": [llm_with_tools.invoke(state["messages"])]}
    
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
        return {"messages": [llm.invoke(state["messages"])]}
    
    # Add the chatbot node
    graph_builder.add_node("chatbot", chatbot)

# Add entry point
graph_builder.add_edge(START, "chatbot")

# Add exit point
graph_builder.add_edge("chatbot", END)

# Compile the graph
graph = graph_builder.compile()

def stream_graph_updates(user_input: str):
    """Stream the chatbot responses for better user experience."""
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Athena:", value["messages"][-1].content)

def run_chatbot():
    """Run the interactive chatbot."""
    print("🤖 Welcome to Athena - Your Family Life Planning Assistant!")
    print("I'm here to help you plan and organize your family's life.")
    
    if TAVILY_API_KEY:
        print("🔍 Web search enabled - I can find current information for you!")
    else:
        print("⚠️  Web search disabled - Get a free Tavily API key to enable current information search")
    
    print("Type 'quit', 'exit', or 'q' to end our conversation.\n")
    
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("👋 Thank you for using Athena! Have a wonderful day!")
                break
            stream_graph_updates(user_input)
            print()  # Add spacing between exchanges
        except KeyboardInterrupt:
            print("\n👋 Goodbye! Thanks for using Athena!")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            print("Please try again or type 'quit' to exit.")

if __name__ == "__main__":
    run_chatbot()
