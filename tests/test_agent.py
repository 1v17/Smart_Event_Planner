# run with command line: python -m pytest tests\test_agent.py

from unittest.mock import MagicMock, patch
import pytest
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from agent import get_agent_graph

@pytest.fixture
def mock_llm():
    with patch("agent.get_llm") as mock_get_llm:
        mock_llm_instance = MagicMock()
        # Mock bind_tools to return the LLM itself (or a new mock) to simplify
        mock_llm_instance.bind_tools.return_value = mock_llm_instance
        mock_get_llm.return_value = mock_llm_instance
        yield mock_llm_instance

def test_agent_graph_structure(mock_llm):
    """Test that the graph compiles without errors."""
    app = get_agent_graph()
    assert app is not None

def test_agent_node_execution_no_tools(mock_llm):
    """Test that the agent node invokes the LLM and returns the response."""
    # Setup mock LLM response
    expected_response = AIMessage(content="Hello there!")
    mock_llm.invoke.return_value = expected_response
    
    app = get_agent_graph()
    
    inputs = {"messages": [HumanMessage(content="Hi")]}
    result = app.invoke(inputs)
    
    # Check that LLM was called
    mock_llm.invoke.assert_called()
    
    # Check output
    assert result["messages"][-1].content == "Hello there!"
    assert not result["messages"][-1].tool_calls

def test_agent_node_execution_with_tools(mock_llm):
    """Test that the agent handles tool calls correctly (simulated)."""
    # Setup mock LLM response to simulated tool call
    call_id = "call_123"
    tool_call = {"name": "search_venues", "args": {"location": "Boston"}, "id": call_id}
    
    msg_with_tool_call = AIMessage(content="", tool_calls=[tool_call])
    final_response = AIMessage(content="I found some venues in Boston.")
    
    mock_llm.invoke.side_effect = [msg_with_tool_call, final_response]
    
    # We mock the database underlying the tool, so the tool itself remains a valid Tool object
    # that ToolNode accepts.
    with patch("tools.get_database") as mock_get_db:
        mock_db_instance = MagicMock()
        mock_collection = MagicMock()
        mock_db_instance.__getitem__.return_value = mock_collection
        mock_get_db.return_value = mock_db_instance
        
        # Setup mock DB return for the tool execution
        mock_collection.find.return_value = [{"name": "Mock Venue", "location": "Boston"}]

        app = get_agent_graph()
        
        inputs = {"messages": [HumanMessage(content="Find venues in Boston")]}
        result = app.invoke(inputs)
        
        # Check LLM calls: Initial call -> Tool output -> Final summary
        assert mock_llm.invoke.call_count == 2
        
        # Check final result
        assert result["messages"][-1].content == "I found some venues in Boston."

