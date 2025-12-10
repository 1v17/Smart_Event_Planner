import os
from pymongo import MongoClient, errors
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_database():
    """
    Establishes a connection to the MongoDB database.
    
    Returns:
        Database: The MongoDB database instance.
    """
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise ValueError("MONGO_URI not found in environment variables")

    try:
        client = MongoClient(mongo_uri)
        # Return the specific database. 
        db_name = os.getenv("MONGO_DB_NAME", "smart_event_planner")
        return client[db_name]
    except errors.ConnectionFailure as e:
        print(f"MongoDB connection failed: {e}")
        raise
    except errors.ConfigurationError as e:
        print(f"MongoDB configuration error: {e}")
        raise
