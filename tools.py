from langchain_core.tools import tool
from database import get_database
from typing import List, Dict, Optional
import re

@tool
def search_venues(query: str = "", location: Optional[str] = None, capacity: Optional[int] = None, 
                  amenities: Optional[List[str]] = None) -> List[Dict]:
    """
    Search for venues based on location, capacity, and amenities.
    
    Args:
        query (str): General search query (unused in structured filter, but kept for compatibility).
        location (str): The desired location (e.g., "Boston"). Case-insensitive partial match.
        capacity (int): The minimum required capacity.
        amenities (List[str]): A list of required amenities (e.g., ["Wi-Fi", "Projector"]).
        
    Returns:
        List[Dict]: A list of venue documents matching the criteria.
    """
    db = get_database()
    collection = db["venues"]
    
    mongo_query = {}
    
    if location:
        mongo_query["location"] = {"$regex": location, "$options": "i"}
        
    if capacity:
        mongo_query["capacity"] = {"$gte": capacity}
        
    if amenities:
        # Match if the venue has ALL the requested amenities
        
        and_conditions = []
        for amenity in amenities:
            and_conditions.append({
                "amenities": {"$regex": re.escape(amenity), "$options": "i"}
            })
        
        if and_conditions:
            if "$and" in mongo_query:
                mongo_query["$and"].extend(and_conditions)
            else:
                mongo_query["$and"] = and_conditions

    results = list(collection.find(mongo_query, {"_id": 0})) # Exclude _id to make it serializable easily
    return results
