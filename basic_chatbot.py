from typing import Annotated
from typing_extensions import TypedDict

from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from config import GOOGLE_API_KEY, LANGSMITH_API_KEY, LANGSMITH_PROJECT

# Set up LangSmith for monitoring (optional)
if LANGSMITH_API_KEY:
    import os
    os.environ["LANGSMITH_API_KEY"] = LANGSMITH_API_KEY
    os.environ["LANGSMITH_PROJECT"] = LANGSMITH_PROJECT

# Set up Google API key
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
