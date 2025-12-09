# Part 1 Implementation Report

## Summary of Changes
- **Dependencies**: Added `pytest` and `mongomock` to `requirements.txt`.
- **Database Module**: Created `database.py` to handle MongoDB connections using `pymongo`. It retrieves configuration from `.env`.
- **Seeding Script**: Created `seed.py` to populate the `venues` collection with dummy data. It clears existing data before insertion.
- **Testing**: Added `tests/test_database.py` with unit tests for the database connection and seeding logic, using `mongomock` to avoid requiring a running database for tests.
- **Package Structure**: Added `__init__.py` to root and `tests/` directories to support imports.

## Local MongoDB Setup Instructions (Windows)

To set up a local MongoDB instance:

1.  **Download**:
    - Go to the [MongoDB Community Server Download Page](https://www.mongodb.com/try/download/community).
    - Select "Windows" as the platform and download the MSI package.

2.  **Install**:
    - Run the installer.
    - Choose "Complete" setup.
    - **Important**: Select "Install MongoDB as a Service" (this is usually checked by default). This runs MongoDB automatically in the background.
    - You can uncheck "Install MongoDB Compass" if you prefer to install it separately or use a different client, but it is recommended for viewing your data.

3.  **Verify Service**:
    - Open "Services" app in Windows.
    - Look for "MongoDB Server".
    - It should be "Running".

4.  **Verification**:
    - Open a terminal (PowerShell or Command Prompt).
    - If you added MongoDB to your PATH during installation (or manually), you can run:
      ```powershell
      mongosh
      ```
      (Note: `mongo` shell is deprecated in newer versions, replaced by `mongosh`).
    - If `mongosh` connects, your database is running at `mongodb://localhost:27017`.

## Execution Instructions

### 1. Install Dependencies
Ensure you are in your configured environment (e.g., `miniconda`):
```bash
pip install -r requirements.txt
```

### 2. Run Tests
**IMPORTANT:** Run tests from the project root using `python -m pytest` or just `pytest` to ensure imports work correctly.
```bash
python -m pytest
```

### 3. Seed the Database
Ensure your MongoDB instance is running, then populate it with test data:
```bash
python seed.py
```
*Expected Output:*
```
Cleared X existing venues.
Successfully seeded 5 venues.
```

### 4. Verify Data
You can verify the data using MongoDB Compass or `mongosh`:
```bash
mongosh --eval "use smart_event_planner; db.venues.find().pretty()"
```
