from database import get_database

def seed_venues():
    """
    Populates the 'venues' collection with dummy data.
    Clears existing data before inserting.
    """
    try:
        db = get_database()
        venues_collection = db["venues"]

        # Dummy venue data
        venues = [
            {
                "name": "Tech Hub Conference Center",
                "location": "Downtown Innovation District",
                "capacity": 500,
                "amenities": ["Wi-Fi", "Projector", "Video Conferencing", "Catering"],
                "price_per_hour": 150
            },
            {
                "name": "Green Garden Pavilion",
                "location": "City Park",
                "capacity": 100,
                "amenities": ["Outdoor Seating", "Garden View", "Tables and Chairs"],
                "price_per_hour": 75
            },
            {
                "name": "Historic Grand Hall",
                "location": "Old Town",
                "capacity": 300,
                "amenities": ["Stage", "Sound System", "Lighting", "Bar"],
                "price_per_hour": 250
            },
            {
                "name": "Cozy Community Room",
                "location": "Westside",
                "capacity": 50,
                "amenities": ["Whiteboard", "Kitchenette", "TV"],
                "price_per_hour": 40
            },
             {
                "name": "Skyline Rooftop Lounge",
                "location": "Financial District",
                "capacity": 120,
                "amenities": ["Bar", "City View", "DJ Booth", "Lounge Furniture"],
                "price_per_hour": 200
            }
        ]

        # Clear existing data
        delete_result = venues_collection.delete_many({})
        print(f"Cleared {delete_result.deleted_count} existing venues.")

        # Insert new data
        insert_result = venues_collection.insert_many(venues)
        print(f"Successfully seeded {len(insert_result.inserted_ids)} venues.")

    except Exception as e:
        print(f"An error occurred during seeding: {e}")

if __name__ == "__main__":
    seed_venues()
