# run with command line: pytest tests\test_database.py
import pytest
import mongomock
from database import get_database

@pytest.fixture
def mock_mongo_env(monkeypatch):
    """Sets up environment variables for testing."""
    monkeypatch.setenv("MONGO_URI", "mongodb://test_uri:27017")
    monkeypatch.setenv("MONGO_DB_NAME", "test_db")

def test_get_database_success(mock_mongo_env):
    """Test successful database connection with mocked MongoClient."""
    with mongomock.patch(servers=(('test_uri', 27017),)):
        db = get_database()
        assert db is not None
        assert db.name == "test_db"

def test_get_database_missing_uri(monkeypatch):
    """Test that ValueError is raised when MONGO_URI is missing."""
    monkeypatch.delenv("MONGO_URI", raising=False)
    
    with pytest.raises(ValueError, match="MONGO_URI not found"):
        get_database()

def test_seed_venues_integration(mock_mongo_env):
    """
    Test the seeding logic with mongomock. 
    This effectively tests seed.py logic without a real DB.
    """
    # We need to import seed_venues inside the test or patch get_database in seed module
    # Because seed.py imports get_database at top level, but we want to intercept the DB it gets.
    from seed import seed_venues
    from unittest.mock import patch

    with mongomock.patch(servers=(('test_uri', 27017),)):
        # Call seed
        seed_venues()
        
        # Verify
        db = get_database()
        venues = list(db["venues"].find())
        assert len(venues) == 5
        assert venues[0]["name"] == "Tech Hub Conference Center"
