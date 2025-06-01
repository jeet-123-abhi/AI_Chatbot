from pydantic import BaseModel  # For defining data models with validation
from typing import List  # To specify that messages is a list of strings
from fastapi import FastAPI  # The FastAPI web framework
from agent_ai import run_react_agent_ai  # Import your AI agent function

# Define the request data model expected by the /chat endpoint
class request(BaseModel):
    messages: List[str]  # List of messages (strings) from the user
    allow_search: bool   # Flag to enable or disable external search

# Create the FastAPI app instance with a title
app = FastAPI(title="Agent AI Backend")

# Define a POST endpoint /chat to receive chat requests
@app.post("/chat")
def chat(request: request):
    query = " ".join(request.messages)  # Combine list of messages into one query string
    response = run_react_agent_ai(query, request.allow_search)  # Call your AI agent
    return response  # Return the AI response as HTTP response

# Entry point to run the API with Uvicorn server when running this script directly
if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI app on localhost (127.0.0.1) at port 8000
    uvicorn.run(app, host="127.0.0.1", port=8000)
