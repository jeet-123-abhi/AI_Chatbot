import os  # For accessing environment variables and operating system functions
from dotenv import load_dotenv  # To load environment variables from a .env file

# Load environment variables from .env file
load_dotenv()  
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")  # Tavily API key for search tool authentication
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # OpenAI API key for ChatGPT access

from langchain_openai import ChatOpenAI  # LangChain wrapper for OpenAI chat models
from langchain_community.tools.tavily_search import TavilySearchResults  # Tavily search tool for external info retrieval
from langgraph.prebuilt import create_react_agent  # Utility to create a React-style LangChain agent

def run_react_agent_ai(query, allow_search):
    # Initialize search tool only if allow_search is True
    tools = [TavilySearchResults(max_results=2, tavily_api_key=TAVILY_API_KEY)] if allow_search else []
    
    # Initialize the OpenAI chat model
    openai_model = ChatOpenAI(model="gpt-4", openai_api_key=OPENAI_API_KEY)
    
    # Create the agent with the model and tools
    agent = create_react_agent(openai_model, tools)
    
    # Prepare the initial message state for the agent
    state = {"messages": [("user", query)]}
    
    # Invoke the agent and get the response
    result = agent.invoke(state)
    
    # Return the content of the last message from the agent's response
    return result["messages"][-1].content
