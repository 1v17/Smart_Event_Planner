import os
from pymongo import MongoClient
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
        # Verify connection by attempting to print server info (optional, helps debugging)
        # client.server_info() 
        
        # Return the specific database. 
        # If the URI doesn't skip the db name, we could use get_default_database()
        # But for this project, we'll enforce a specific DB name or allow it to be configured.
        db_name = os.getenv("MONGO_DB_NAME", "smart_event_planner")
        return client[db_name]
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise
