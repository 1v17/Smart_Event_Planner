# run with command line: python -m pytest tests/test_tools.py

from tools import search_venues
from unittest.mock import MagicMock, patch
import pytest

@pytest.fixture
def mock_db():
    with patch("tools.get_database") as mock_get_db:
        mock_db_instance = MagicMock()
        mock_collection = MagicMock()
        mock_db_instance.__getitem__.return_value = mock_collection
        mock_get_db.return_value = mock_db_instance
        yield mock_collection

def test_search_venues_no_filters(mock_db):
    # Setup
    mock_db.find.return_value = [{"name": "Venue A"}, {"name": "Venue B"}]
    
    # Execute
    results = search_venues.func(query="")
    
    # Assert
    assert len(results) == 2
    mock_db.find.assert_called_with({}, {"_id": 0})

def test_search_venues_with_location(mock_db):
    # Execute
    search_venues.func(location="Boston")
    
    # Assert
    mock_db.find.assert_called_with(
        {"location": {"$regex": "Boston", "$options": "i"}}, 
        {"_id": 0}
    )

def test_search_venues_with_capacity(mock_db):
    # Execute
    search_venues.func(capacity=100)
    
    # Assert
    mock_db.find.assert_called_with(
        {"capacity": {"$gte": 100}}, 
        {"_id": 0}
    )

def test_search_venues_with_amenities(mock_db):
    # Execute
    search_venues.func(amenities=["Wi-Fi", "Projector"])
    
    # Assert
    import re
    expected_query = {
        "$and": [
            {"amenities": {"$regex": re.escape("Wi-Fi"), "$options": "i"}},
            {"amenities": {"$regex": re.escape("Projector"), "$options": "i"}}
        ]
    }
    mock_db.find.assert_called_with(expected_query, {"_id": 0})
