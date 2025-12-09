# Smart Event Planner Assistant
## Application Context
The Smart Event Planner Assistant is an AI-powered agent designed to help users find event venues through natural conversation. It allows users to query for venues based on criteria like location, capacity, amenities, and price. The system leverages:
- **LangChain & LangGraph**: For orchestrating the multi-agent workflow and managing conversation state.
- **MongoDB**: For storing and retrieving venue functionality.
- **OpenRouter API**: To access powerful LLMs for natural language understanding and generation.

The goal is to provide a seamless, chat-based interface for event planning, acting as a technical demo for an intelligent assistant architecture.

## Execution Plan

### Part 1
- [x] **Project Initialization**:
    - [x] Virtual environment already setup using miniconda.
    - [x] Create `.env` file for `OPENROUTER_API_KEY` and `MONGO_URI`.
    - [x] Verify in `main.py` that the openrouter api key is valid.
- [x] **Database Implementation**:
    - [x] Setup local MongoDB instance.
    - [x] Implement `database.py` to handle connections.
    - [x] Create a seeding script (`seed.py`) to populate the `venues` collection with dummy data (Names, Locations, Capacities, Amenities).
    - [x] Added unit tests (`tests/test_database.py`) and updated `requirements.txt` with `pytest` and `mongomock`.

### Part 2
1.  **Tool Creation**:
    -   Implement `tools.py` with functions like `search_venues(location, capacity, ...)` using MongoDB queries.
    -   Wrap these functions as LangChain `Tools`.
2.  **LLM Setup**:
    -   Configure `ChatOpenAI` creating a client pointing to OpenRouter base URL.
    -   Test basic connectivity with a simple prompt.

### Part 3

1.  **State Definition**:
    -   Define `AgentState` in `agent.py` to track conversation history and tool outputs.
2.  **Graph Construction**:
    -   Define nodes: `agent` (calls LLM), `tools` (executes tools).
    -   Define edges: Logic to switch between agent and tools based on LLM output.
    -   Compile the graph.

### Part 4
1.  **Interface**:
    -   Build a simple CLI loop in `main.py` to accept user input and stream graph events.
    -   Alternatively, build a simple generic implementation using Streamlit if time permits (optional).
2.  **Testing & Refinement**:
    -   Verify the agent can handle:
        -   "I need a venue in Boston for 50 people." (Extraction & Tool Call)
        -   "What amenities does it have?" (Context retention)
    -   Refine system prompts for better persona and accuracy.
    -   Final code cleanup and documentation.

## Deliverables
- Source code in Python.
- `requirements.txt`.
- `README.md` with setup instructions.
- A functional agent capable of querying the database.
