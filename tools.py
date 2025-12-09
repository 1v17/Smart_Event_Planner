from langchain_core.tools import tool
from database import get_database
from typing import List, Dict, Optional
import re

@tool
def search_venues(query: str = "", location: Optional[str] = None, capacity: Optional[int] = None, amenities: Optional[List[str]] = None) -> List[Dict]:
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
        # We'll use $all operator, but we need to ensure case-insensitivity if possible?
        # MongoDB simple $all is exact match. For case-insensitive list matching, it's harder.
        # For simplicity in this demo, we will assume the amenities passed are somewhat normalized or we use regex for each.
        # Let's try to be robust:
        # We want venues where 'amenities' array contains items that match our requested amenities (case-insensitive)
        
        # Complex regex query for list items is tricky. Let's stick to simple regex match for each item if possible,
        # but $all with regex is not directly supported in standard simple syntax.
        # A workaround is using $and with $elemMatch for each amenity.
        
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
